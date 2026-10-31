"""Qualidade e consistência dos dados de entrada."""
import numpy as np


def test_tabelas_sem_nulos_nem_duplicados(nb):
    for tabela in (nb["locations"], nb["fleet"], nb["orders"]):
        assert tabela.isnull().sum().sum() == 0
        assert tabela.duplicated().sum() == 0
    assert nb["orders"]["order_id"].is_unique


def test_pedidos_apontam_para_locais_existentes(nb):
    assert set(nb["orders"]["location_id"]) <= set(nb["locations"]["location_id"])


def test_peso_igual_quantidade_vezes_peso_unitario(nb):
    orders = nb["orders"]
    esperado = (orders["quantity"] * orders["unit_weight_kg"]).round(1)
    assert np.allclose(orders["weight_kg"], esperado)


def test_consolidacao_uma_entrega_por_local_e_dia(nb):
    deliveries = nb["deliveries"]
    assert not deliveries.duplicated(["date", "location_id"]).any()
    assert len(deliveries) == 112


def test_entrega_herda_a_prioridade_mais_alta_e_o_frio(nb):
    orders, deliveries = nb["orders"], nb["deliveries"]
    rank = nb["PRIORITY_RANK"]
    for row in deliveries.itertuples():
        itens = orders[(orders["date"] == row.date) & (orders["location_id"] == row.location_id)]
        assert row.priority == min(itens["priority"], key=rank.get)
        assert row.refrigerated == itens["refrigerated"].any()
