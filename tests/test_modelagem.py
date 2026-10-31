"""Representação do cromossomo, distâncias e função fitness."""
import math
import random


def test_matriz_de_distancias_simetrica_e_diagonal_zero(nb):
    dist = nb["problem"].dist
    n = len(dist)
    for i in range(n):
        assert dist[i][i] == 0
        for j in range(n):
            assert math.isclose(dist[i][j], dist[j][i])


def test_haversine_distancia_conhecida(nb):
    # Praça da Sé -> Av. Paulista (MASP): cerca de 2,9 km em linha reta
    km = nb["haversine_matrix_km"]([-23.5503, -23.5614], [-46.6340, -46.6559])[0][1]
    assert 2.5 < km < 3.2


def test_decode_encode_ida_e_volta(nb):
    rotas = [[5, 2], [7, 1], [3, 6, 4]]
    cromossomo = nb["encode"](rotas)
    assert cromossomo == [5, 2, -1, 7, 1, -2, 3, 6, 4]
    assert nb["decode"](cromossomo, 3) == rotas


def test_decode_aceita_veiculo_vazio(nb):
    assert nb["decode"]([-1, -2, 4, 2], 3) == [[], [], [4, 2]]


def test_fitness_rapida_igual_a_simulacao_detalhada(nb):
    problem, rng = nb["problem"], random.Random(0)
    for _ in range(200):
        cromossomo = rng.sample(nb["all_genes"], len(nb["all_genes"]))
        rotas = nb["decode"](cromossomo, problem.n_vehicles)
        rapida = nb["chromosome_cost"](problem, cromossomo)
        detalhada = nb["evaluate_solution"](problem, rotas)["cost"]
        assert math.isclose(rapida, detalhada, rel_tol=1e-9)


def test_cadeia_de_frio_e_penalizada(nb):
    problem = nb["problem"]
    fria = next(i for i in range(1, problem.n) if problem.cold[i])
    seco = problem.vehicle_cold.index(False)
    refrigerado = problem.vehicle_cold.index(True)
    custo_seco = nb["route_cost"](problem, [fria], seco)
    custo_refrigerado = nb["route_cost"](problem, [fria], refrigerado)
    assert custo_seco - custo_refrigerado >= nb["PENALTY_COLD_CHAIN"] - 1


def test_excesso_de_carga_vira_violacao(nb):
    problem = nb["problem"]
    todas = list(range(1, problem.n))
    rotas = [[] for _ in range(problem.n_vehicles)]
    rotas[problem.capacity.index(min(problem.capacity))] = todas
    avaliacao = nb["evaluate_solution"](problem, rotas)
    assert avaliacao["capacity_excess_kg"] > 0
    assert not avaliacao["feasible"]
