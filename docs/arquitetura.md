# Diagrama de Arquitetura

A solução foi estruturada como um pipeline de dados e otimização logística, com integração de inteligência artificial para geração de instruções e relatórios.

```mermaid
flowchart LR
    subgraph Fonte[Fontes de Dados]
        A1["delivery_locations.csv<br/>Locais, coordenadas e tempos"]
        A2["delivery_fleet.csv<br/>Frota, capacidade e refrigeração"]
        A3["delivery_orders.csv<br/>Pedidos, priorização e restrições"]
    end

    subgraph ETL[Camada de Preparação]
        B1[Validação e limpeza de dados]
        B2[Normalização de rotas e atributos]
        B3[Cálculo de distâncias e tempos]
    end

    subgraph Core[Motor de Otimização]
        C1[Algoritmo Genético]
        C2[Função de fitness]
        C3["Restrições operacionais<br/>capacidade, jornada, frio, prazo"]
        C4[Seleção, crossover e mutação]
    end

    subgraph SA[Serviços de Apoio]
        D1["Mapas interativos<br/>Folium"]
        D2["Gráficos e métricas<br/>Matplotlib / Seaborn"]
        D3[LLM - Google Gemini]
        D4[Fallback offline]
    end

    subgraph Output[Resultados e Entregáveis]
        E1[Plano de rota otimizado]
        E2[Instruções para motoristas]
        E3[Relatórios executivos]
        E4[Indicadores de eficiência]
        E5[Visualização geoespacial]
    end

    subgraph Users[Usuários e Operação]
        F1[Operação logística]
        F2[Gestão hospitalar]
        F3[Coordenadores / motoristas]
    end

    A1 --> B1
    A2 --> B1
    A3 --> B1
    B1 --> B2
    B2 --> B3
    B3 --> C1
    C1 --> C2
    C2 --> C3
    C3 --> C4
    C4 --> E1

    E1 --> D1
    E1 --> D2
    E1 --> D3
    D3 --> E2
    D3 --> E3
    D2 --> E4
    D1 --> E5

    E1 --> F1
    E2 --> F3
    E3 --> F2
    E4 --> F2
    E5 --> F1

    D3 -. informa contexto e dados .-> C1
    D4 -. fallback seguro .-> D3
```

## Visão Conceitual

- A camada de dados recebe os arquivos CSV com informações dos locais, frota e pedidos.
- A etapa de preparação transforma esses dados em entradas válidas para o problema de roteamento.
- O núcleo do sistema é o algoritmo genético, responsável por otimizar a sequência de entregas respeitando capacidades, prazos e restrições logísticas.
- Os módulos de apoio geram mapas, gráficos e relatórios, além de integrar uma LLM para transformar os resultados em linguagem natural.
- O produto final fornece decisões operacionais acionáveis para gestão, atendimento e execução de entregas.

## Componentes Chave

- Data layer: arquivos de logística e operação hospitalar.
- Optimization engine: lógica de busca e otimização.
- Visualization layer: mapas e dashboards executivos.
- AI layer: geração de instruções e relatórios com Gemini.
- Delivery outputs: rota recomendada, instruções, indicadores e suporte de decisão.
