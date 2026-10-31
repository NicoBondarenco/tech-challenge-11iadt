"""Operadores genéticos: devem sempre gerar cromossomos válidos."""
import random

import pytest


def _valido(nb, cromossomo):
    return sorted(cromossomo) == sorted(nb["all_genes"])


def test_order_crossover_gera_permutacao_valida(nb):
    rng = random.Random(1)
    genes = nb["all_genes"]
    for _ in range(500):
        pai1, pai2 = rng.sample(genes, len(genes)), rng.sample(genes, len(genes))
        filho = nb["crossover_ox"](pai1, pai2, rng)
        assert _valido(nb, filho)


def test_order_crossover_preserva_um_trecho_do_pai1(nb):
    rng = random.Random(2)
    genes = nb["all_genes"]
    pai1, pai2 = rng.sample(genes, len(genes)), rng.sample(genes, len(genes))
    filho = nb["crossover_ox"](pai1, pai2, rng)
    # Algum trecho contíguo de tamanho >= 1 do pai 1 aparece na mesma posição
    assert any(filho[i] == pai1[i] for i in range(len(genes)))


def test_order_crossover_do_codigo_base_usa_os_dois_pais(nb):
    # O código base da FIAP chamava order_crossover(parent1, parent1); aqui o filho precisa ser válido
    random.seed(3)
    cidades = list(range(nb["problem"].n))
    pai1, pai2 = random.sample(cidades, len(cidades)), random.sample(cidades, len(cidades))
    filho = nb["order_crossover"](pai1, pai2)
    assert sorted(filho) == cidades


@pytest.mark.parametrize("operador", ["adjacent_swap", "swap", "inversion", "insertion"])
def test_mutacoes_geram_permutacao_valida(nb, operador):
    rng = random.Random(4)
    genes = nb["all_genes"]
    for _ in range(300):
        cromossomo = rng.sample(genes, len(genes))
        mutado = nb["mutate_routes"](cromossomo, 1.0, (operador,), rng)
        assert _valido(nb, mutado)


def test_mutacao_com_taxa_zero_nao_altera(nb):
    rng = random.Random(5)
    cromossomo = rng.sample(nb["all_genes"], len(nb["all_genes"]))
    assert nb["mutate_routes"](cromossomo, 0.0, ("swap",), rng) == cromossomo
