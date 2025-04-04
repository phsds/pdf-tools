import os
import subprocess
import sys

def activate_virtualenv():
    venv_dir = ".\\execution\\Scripts\\activate.bat"
    
    if os.path.exists(venv_dir):
        print("Ativando o ambiente virtual 'execution'...")
        try:
            # Executa o script .bat diretamente no cmd
            subprocess.call(f'cmd.exe /k "{venv_dir}"', shell=True)
            print("Ambiente virtual ativado com sucesso.")
        except Exception as e:
            print(f"Erro ao ativar o ambiente virtual: {e}")
            sys.exit(1)
    else:
        print("Erro: O ambiente virtual 'execution' não foi encontrado.")
        sys.exit(1)

if __name__ == "__main__":
    activate_virtualenv()