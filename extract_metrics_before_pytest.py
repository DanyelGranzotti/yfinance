import os
import subprocess
import sys
from pathlib import Path

# Configuracao, ajuste apenas se necessario.

# Diretorio raiz do projeto clonado, os testes vai comecar a execucao a petir dele.
PROJETO = "."

# Diretorio dos testes detectado automaticamente, mas pode forcar manualmente
# Exemplos: TESTES = "./tests"  ou  TESTES = "./test"
TESTES = None

# Pasta onde os relatorios serao salvos (nao altere)
PASTA = "metrics-before-pytest"

# Deteccao automatica do diretorio de testes
CANDIDATOS = ["tests", "test", "src/tests", "src/test"]

if TESTES is None:
    for candidato in CANDIDATOS:
        if Path(candidato).exists():
            TESTES = candidato
            break

if TESTES is None:
    print("Erro: diretorio de testes nao encontrado.")
    print(f"Procurado em: {CANDIDATOS}")
    print("Defina manualmente a variavel TESTES no script.")
    sys.exit(1)

# Execucao
os.makedirs(PASTA, exist_ok=True)

print(f"Projeto : {os.path.abspath(PROJETO)}")
print(f"Testes  : {TESTES}")
print(f"Relatorios em: {PASTA}/")
print()

resultado = subprocess.run(
    [
        sys.executable, "-m", "pytest", TESTES,
        "-v",
        f"--junit-xml={os.path.join(PASTA, 'pytest_antes.xml')}",
        f"--html={os.path.join(PASTA, 'pytest_antes.html')}",
        "--self-contained-html",
        f"--cov={PROJETO}",
        "--cov-branch",
        f"--cov-report=xml:{os.path.join(PASTA, 'coverage_antes.xml')}",
        f"--cov-report=json:{os.path.join(PASTA, 'coverage_antes.json')}",
        f"--cov-report=html:{os.path.join(PASTA, 'coverage_antes_html')}",
        "--cov-report=term-missing",
    ],
    cwd=PROJETO,
    text=True,
    encoding="utf-8",
)

print(f"\nExit code: {resultado.returncode}")
print(f"\nArquivos gerados em '{PASTA}':")
print("  pytest_antes.xml      -> resultados dos testes em XML")
print("  pytest_antes.html     -> relatorio visual dos testes")
print("  coverage_antes.xml    -> cobertura de codigo em XML")
print("  coverage_antes.json   -> cobertura de codigo em JSON")
print("  coverage_antes_html/  -> relatorio visual de cobertura")
print("\nConcluido.")
