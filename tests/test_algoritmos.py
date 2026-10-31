"""Heurísticas de comparação e o algoritmo genético."""


def _todas_uma_vez(problem, rotas):
    return sorted(no for rota in rotas for no in rota) == list(range(1, problem.n))


def test_vizinho_mais_proximo_atende_todas_e_e_viavel(nb):
    problem = nb["problem"]
    for rotas in nb["heuristic_solutions"](problem).values():
        assert _todas_uma_vez(problem, rotas)
        assert nb["evaluate_solution"](problem, rotas)["feasible"]


def test_vizinho_mais_proximo_respeita_cadeia_de_frio(nb):
    problem = nb["problem"]
    for k, rota in enumerate(nb["greedy_routes"](problem)):
        if not problem.vehicle_cold[k]:
            assert not any(problem.cold[no] for no in rota)


def test_2opt_nunca_aumenta_a_distancia(nb):
    problem = nb["problem"]
    for rota in nb["greedy_routes"](problem):
        antes = nb["simulate_route"](problem, rota, 0)[1]
        depois = nb["simulate_route"](problem, nb["two_opt"](problem, rota), 0)[1]
        assert depois <= antes + 1e-9


def test_ag_curto_encontra_solucao_viavel(nb):
    problem = nb["problem"]
    config = nb["GAConfig"]("teste", population_size=80, generations=150)
    run = nb["run_ga"](problem, config, seed=42)
    assert _todas_uma_vez(problem, run["routes"])
    assert nb["evaluate_solution"](problem, run["routes"])["feasible"]


def test_ag_com_elitismo_nunca_piora(nb):
    config = nb["GAConfig"]("teste", population_size=60, generations=100)
    historico = nb["run_ga"](nb["problem"], config, seed=7)["best_history"]
    assert all(b <= a + 1e-9 for a, b in zip(historico, historico[1:]))


def test_ag_e_reprodutivel_com_a_mesma_semente(nb):
    config = nb["GAConfig"]("teste", population_size=40, generations=50)
    a = nb["run_ga"](nb["problem"], config, seed=123)
    b = nb["run_ga"](nb["problem"], config, seed=123)
    assert a["chromosome"] == b["chromosome"]


def test_ag_supera_o_vizinho_mais_proximo(nb):
    problem = nb["problem"]
    config = nb["GAConfig"]("teste", population_size=150, generations=300)
    custo_ag = nb["run_ga"](problem, config, seed=42)["cost"]
    custo_vmp = nb["evaluate_solution"](problem, nb["greedy_routes"](problem))["cost"]
    assert custo_ag < custo_vmp
