"""Carrega as funções do notebook para os testes.

Executa as células de código do notebook, em ordem, até a célula que define os
experimentos do AG (GA_EXPERIMENTS). Assim os testes usam exatamente o código do
notebook, sem copiar funções para outro arquivo.
"""
import json
import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # sem janelas de gráfico durante os testes

import matplotlib.pyplot as plt
import pytest

RAIZ = Path(__file__).resolve().parents[1]
NOTEBOOK = RAIZ / "notebooks" / "tech_challenge_fase2.ipynb"
DADOS = RAIZ / "data"
PARAR_EM = "GA_EXPERIMENTS = ["  # a partir daqui vêm os experimentos lentos e a LLM


def _celulas_de_codigo():
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    for celula in notebook["cells"]:
        if celula["cell_type"] != "code":
            continue
        fonte = "".join(celula["source"])
        if PARAR_EM in fonte:
            return
        # Linhas de shell (!pip) e magics (%) não são Python puro
        linhas = [l for l in fonte.splitlines() if not l.lstrip().startswith(("!", "%"))]
        yield "\n".join(linhas)


@pytest.fixture(scope="session")
def nb():
    """Namespace com tudo o que o notebook definiu (problem, decode, run_ga, ...)."""
    os.environ["LLM_MODE"] = "offline"
    namespace = {"__name__": "notebook"}
    pasta_original = os.getcwd()
    os.chdir(DADOS)  # o notebook lê os CSVs da pasta atual
    try:
        for codigo in _celulas_de_codigo():
            exec(compile(codigo, str(NOTEBOOK), "exec"), namespace)
            plt.close("all")
    finally:
        os.chdir(pasta_original)
    return namespace
