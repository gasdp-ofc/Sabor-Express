
# Rota Inteligente: Otimização de Entregas com Algoritmos de IA

Projeto acadêmico para a **Sabor Express** (delivery de alimentos) focado em **redução de tempo e custo** nas rotas durante horários de pico.

## 🎯 Objetivos
- Modelar a cidade como **grafo** (nós = interseções/bairros; arestas = ruas com pesos de tempo/distância).
- Encontrar **menores caminhos** entre múltiplas entregas por entregador.
- **Agrupar entregas** próximas (zonas) via **K-Means** para balancear a carga entre entregadores.
- Gerar **rotas por zona** usando **A\*** (heurística euclidiana) entre paradas, com ordenação gulosa (vizinho mais próximo).
- Avaliar a solução por **métricas de custo total**, custo por cluster e número de paradas.

## 🧠 Abordagem (Visão Geral)
1. **Grafo urbano**: malha reticulada sintética (12x12) em `data/city_nodes.csv` e `data/city_edges.csv`.
2. **Clustering (K-Means)**: agrupa pontos de entrega em `k` zonas (nº de entregadores).
3. **Planejamento de rota por zona**:
   - Ordem gulosa (vizinho mais próximo) das paradas a partir do **depósito** (node 0).
   - Entre cada par de paradas, calculamos o **menor caminho** com **A\*** sobre o grafo (custo = tempo/ distância).
   - Rota retorna ao depósito ao final.
4. **Visualizações**: 
   - `outputs/graph.png` — grafo da cidade.
   - `outputs/clusters.png` — entregas por cluster e centróides.
5. **Métricas**: `outputs/metrics.json` com custo total, custo por cluster e médias.

> Observação: incluímos BFS/DFS como referência algorítmica no contexto de busca em grafos, embora **A\*** seja o núcleo para menor caminho com heurística consistente.

## 🗂 Estrutura do Repositório
```
sabor-express-route-optimization/
├── data/
│   ├── city_nodes.csv
│   ├── city_edges.csv
│   └── deliveries.csv
├── docs/
│   └── pitch_script.md
├── outputs/                # gerado em runtime
│   ├── clusters.png
│   ├── graph.png
│   └── metrics.json
├── src/
│   ├── astar.py
│   ├── graph.py
│   ├── kmeans.py
│   ├── routing.py
│   ├── utils.py
│   └── main.py
└── README.md
```

## ▶️ Como Executar
Pré-requisitos: **Python 3.10+** com `numpy` e `matplotlib`. (Opcional: `pandas` não é necessário.)

```bash
# dentro da raiz do projeto
python -m src.main --k 3 --seed 42 --depot 0
# parâmetros úteis:
#   --k      número de entregadores (clusters)
#   --seed   reprodutibilidade da clusterização
#   --depot  id do nó do depósito (padrão: 0)
```

Saídas esperadas:
- **Console**: custo total, custo por cluster, número de paradas.
- **Arquivos**: `outputs/metrics.json`, `outputs/graph.png`, `outputs/clusters.png`.

## 🔬 Algoritmos Utilizados
- **A\***: `f(n) = g(n) + h(n)`, com `h(n)` = distância euclidiana na malha (admissível).
- **K-Means (implementação própria)**: clusterização das coordenadas (x,y) dos nós de entrega.
- **Heurística gulosa (vizinho mais próximo)** para ordenar paradas dentro do cluster.
- **BFS/DFS**: referências conceituais para varredura; úteis em diagnósticos ou verificação de conexidade.

## 📈 Métricas e Avaliação
- **Custo total de rota** (soma dos menores caminhos por segmento A\*).
- **Custo por cluster** e **média por cluster** (balanceamento de carga).
- **Nº de entregas por cluster** (distribuição de demanda).
- **Ideias de evolução**: `silhouette score` para qualidade da clusterização; `2-opt`/`3-opt` para refinar ordem das paradas; capacidade por veículo; janelas de tempo (VRPTW).

## ⚠️ Limitações
- O ordenamento interno é guloso (não garante TSP ótimo).
- Sem restrições de capacidade/tempo.
- Tráfego apenas estático (fator multiplicativo nos pesos).

## 🚀 Próximos Passos (Roadmap)
- **Tempo real**: pesos dinâmicos por API de trânsito.
- **MILP / Metaheurísticas**: VRP com capacidade (CVRP), janelas de tempo (VRPTW).
- **Atribuição ótima**: Hungarian / Min‑Cost Flow para alocar clusters a entregadores.
- **Rotas multi‑depósito** e reequilíbrio dinâmico (inserções on‑the‑fly).

## 🖼 Diagrama do Grafo
As figuras são geradas automaticamente em `outputs/graph.png` e `outputs/clusters.png` após a execução do comando acima.

---
