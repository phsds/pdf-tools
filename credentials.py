"""
Read and write protected credentials.

Preference: DPAPI (Windows) -> Fernet (fallback).

Functions:
- get_credentials() -> (email, password) or raises RuntimeError
- save_credentials(email, password) -> path of the saved file

Note: do not commit the `credentials.dpapi` or `credentials.enc` files.
"""
import os
import sys

try:
    from ctypes import windll, create_string_buffer, byref, c_void_p, c_wchar_p
    import ctypes
    from ctypes import wintypes

    class DATA_BLOB(ctypes.Structure):
        _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_byte))]

    def _dpapi_encrypt(data: bytes) -> bytes:
        crypt32 = windll.crypt32
        kernel32 = windll.kernel32
        blob_in = DATA_BLOB(len(data), ctypes.cast(ctypes.create_string_buffer(data), ctypes.POINTER(ctypes.c_byte)))
        blob_out = DATA_BLOB()
        if crypt32.CryptProtectData(byref(blob_in), None, None, None, None, 0, byref(blob_out)):
            buf = ctypes.string_at(blob_out.pbData, blob_out.cbData)
            kernel32.LocalFree(blob_out.pbData)
            return buf
        raise ctypes.WinError()

    def _dpapi_decrypt(data: bytes) -> bytes:
        crypt32 = windll.crypt32
        kernel32 = windll.kernel32
        blob_in = DATA_BLOB(len(data), ctypes.cast(ctypes.create_string_buffer(data), ctypes.POINTER(ctypes.c_byte)))
        blob_out = DATA_BLOB()
        if crypt32.CryptUnprotectData(byref(blob_in), None, None, None, None, 0, byref(blob_out)):
            buf = ctypes.string_at(blob_out.pbData, blob_out.cbData)
            kernel32.LocalFree(blob_out.pbData)
            return buf
        raise ctypes.WinError()

    _HAS_DPAPI = True
except Exception:
    _HAS_DPAPI = False

try:
    from cryptography.fernet import Fernet
except Exception:
    Fernet = None


def get_credentials():
    """Return (email, password) if a protected credentials file exists, otherwise raise RuntimeError."""
    # Use the executable directory when frozen (PyInstaller), otherwise use the script directory
    if getattr(sys, "frozen", False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))

    # DPAPI file
    if _HAS_DPAPI:
        dpapi_path = os.path.join(base, "credentials.dpapi")
        if os.path.exists(dpapi_path):
            try:
                token = open(dpapi_path, "rb").read()
                data = _dpapi_decrypt(token)
                email, password = data.decode().split("\n", 1)
                return email.strip(), password.strip()
            except Exception:
                pass

    # Fernet fallback
    enc_path = os.path.join(base, "credentials.enc")
    key = os.environ.get("PDF_TOOLS_FERNET_KEY")
    if Fernet and key and os.path.exists(enc_path):
        try:
            f = Fernet(key.encode())
            token = open(enc_path, "rb").read()
            data = f.decrypt(token)
            email, password = data.decode().split("\n", 1)
            return email.strip(), password.strip()
        except Exception:
            pass

    raise RuntimeError("Credentials file not found.")


def save_credentials(email: str, password: str) -> str:
    """Save protected credentials. Return the path of the saved file."""
    # Use the executable directory when frozen (PyInstaller), otherwise use the script directory
    if getattr(sys, "frozen", False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    data = (email + "\n" + password).encode()

    if _HAS_DPAPI:
        out = os.path.join(base, "credentials.dpapi")
        token = _dpapi_encrypt(data)
        with open(out, "wb") as fh:
            fh.write(token)
        return out

    # Fernet fallback (generate a key and print it for the operator)
    if Fernet is None:
        raise RuntimeError("Nenhum método de proteção disponível (instale cryptography ou use Windows).")

    key = Fernet.generate_key().decode()
    f = Fernet(key.encode())
    token = f.encrypt(data)
    out = os.path.join(base, "credentials.enc")
    with open(out, "wb") as fh:
        fh.write(token)
    # inform the key to the operator
    print("File created:", out)
    print("Fernet key (store securely):", key)
    return out
