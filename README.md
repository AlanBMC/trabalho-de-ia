
**Relatório do Trabalho Prático - Inteligência Artificial**

**Projeto: A Travessia das 12 Casas - Salvando Atena**

**Grupo:** Alan Bruno Moraes Costa, Enzo Bondan, Ricardo Meneses Freire dos Santos

**Data:** 04 de Maio de 2025

**1. Introdução**

Este relatório descreve a implementação de um agente de Inteligência Artificial desenvolvido como parte do trabalho prático da disciplina de Inteligência Artificial. O problema proposto é baseado no universo de "Os Cavaleiros do Zodíaco", onde os Cavaleiros de Bronze (Seiya, Shiryu, Hyoga, Shun e Ikki) precisam atravessar as 12 Casas do Zodíaco, cada uma protegida por um Cavaleiro de Ouro, para salvar a deusa Atena (Saori Kido). Atena foi atingida por uma flecha dourada e os cavaleiros têm um prazo limite de 12 horas (720 minutos) para chegar à sala do Grande Mestre, o único capaz de salvá-la.

O objetivo do trabalho foi desenvolver um agente autônomo capaz de planejar e executar a jornada, determinando o melhor caminho físico através do Santuário e gerenciando as batalhas contra os Cavaleiros de Ouro, considerando o tempo gasto, o poder cósmico e a energia limitada dos Cavaleiros de Bronze.

**2. Método Utilizado**

**2.1. Linguagem e Bibliotecas:**

* A solução foi implementada na linguagem **Python 3**.
* A biblioteca **Pygame** foi utilizada para a criação da interface gráfica e visualização em tempo real da simulação.
* Bibliotecas padrão como `csv`, `sys`, `os`, `heapq`, `math`, `copy`, `random` e `itertools.combinations` foram usadas para manipulação de arquivos, estruturas de dados (fila de prioridade para A*), cálculos e geração de combinações.

**2.2. Abordagem Geral: Estratégia em Duas Fases**

Conforme sugerido nas dicas do trabalho [cite: 44] e validado por tentativas iniciais que mostraram alta complexidade computacional ao tentar resolver o problema de forma unificada, optou-se por uma **abordagem em duas fases**:

1.  **Fase 1: Determinação do Caminho Físico Ótimo:** Encontrar o caminho através do mapa que minimiza o tempo gasto com deslocamento (custo de terreno), garantindo a passagem pelas localizações das 12 casas na ordem correta.
2.  **Fase 2: Simulação e Planejamento Tático das Batalhas:** Simular o percurso encontrado na Fase 1, e ao chegar em cada casa, decidir qual equipe de Cavaleiros de Bronze enfrentará o Cavaleiro de Ouro local, utilizando uma estratégia definida para balancear tempo e energia.

**Motivo da Escolha:** A separação do problema reduz drasticamente a complexidade computacional. O planejamento simultâneo de caminho e todas as possíveis combinações de batalha em cada casa gera um espaço de estados excessivamente grande para algoritmos de busca como o A* explorarem em tempo hábil. A abordagem em duas fases permite encontrar uma solução completa e eficiente, mesmo que a estratégia de batalha local (Fase 2) não garanta a otimalidade global do tempo total combinado (viagem + batalhas).

**2.3. Fase 1: Busca de Caminho Físico (A*)**

* **Algoritmo:** Foi implementado o algoritmo **A* (A-Estrela)** na classe `BuscaAEstrelaCaminho`.
* **Objetivo:** Encontrar a sequência de coordenadas `(x, y)` desde a entrada do Santuário (`VALOR_MAPA_ENTRADA = 0`) até a casa do Grande Mestre (`VALOR_MAPA_OBJETIVO = 1`), passando obrigatoriamente pelas coordenadas de cada uma das 12 casas (obtidas do mapa) em sua ordem sequencial.
* **Estado:** Representado por `(posicao_atual, indice_proximo_waypoint)`, onde `posicao_atual` é a coordenada `(x, y)` e `indice_proximo_waypoint` indica qual ponto obrigatório (entrada, casas 1-12, objetivo) o agente está buscando alcançar.
* **Custo `g(n)`:** O custo acumulado para chegar a um estado, calculado como a soma dos custos de terreno das células percorridas. Os custos definidos são: Plano = 1 min, Rochoso = 5 min, Montanhoso = 200 min[cite: 16]. O movimento é restrito à horizontal e vertical[cite: 33]. Isso é gerenciado pela função `MapaAereo._obter_custo_terreno`.
* **Heurística `h(n)`:** Utilizou-se a **Distância de Manhattan** entre a posição atual e a coordenada do próximo waypoint obrigatório. Essa heurística é admissível (nunca superestima o custo real, pois o custo mínimo de movimento é 1) e consistente para movimentos em grade. Calculada em `BuscaAEstrelaCaminho._calcular_heuristica_caminho`.
* **Resultado:** A função `BuscaAEstrelaCaminho.buscar()` retorna uma lista de coordenadas representando o caminho físico de menor custo de terreno.

**2.4. Fase 2: Simulação e Batalhas (Estratégia Greedy)**

* **Processo:** A função `simular_caminho_e_lutas_com_visualizacao` recebe o caminho de coordenadas da Fase 1 e simula o percurso passo a passo.
* **Acumulação de Tempo:** O tempo total é iniciado em zero e incrementado pelo custo de terreno a cada passo e pelo tempo de batalha ao encontrar uma casa.
* **Escolha da Equipe:** Ao chegar às coordenadas de uma casa do zodíaco pela primeira vez, a função `escolher_equipe_greedy_final` é chamada para determinar qual(is) Cavaleiro(s) de Bronze lutará(ão).
    * **Lógica "Greedy" Implementada:** A estratégia atual busca a equipe, considerando um tamanho máximo pré-definido (e.g., `max_tam_equipe_greedy = 2`), que resulta no **menor tempo de batalha** possível para aquela casa específica, dadas as energias atuais dos cavaleiros vivos. Se nenhuma equipe dentro do limite de tamanho for viável, um fallback tenta usar todos os cavaleiros vivos. Essa lógica visa um equilíbrio entre vencer rapidamente a batalha local e preservar um pouco a energia, evitando o esgotamento rápido observado em estratégias mais simples.
* **Cálculo Tempo Batalha:** Utiliza a fórmula `Tempo = Dificuldade_Casa / Soma_Poder_Cosmico_Equipe`[cite: 27], implementada na função estática `Luta.calcular_tempo_batalha`.
* **Gerenciamento de Energia:** Cada cavaleiro na equipe escolhida perde 1 ponto de energia[cite: 28]. Se a energia chegar a 0, o cavaleiro não pode mais lutar[cite: 29]. A simulação falha se todos os cavaleiros ficarem sem energia.
* **Visualização em Tempo Real:** Esta função também é responsável por atualizar a janela do Pygame a cada passo da simulação, movendo os sprites dos cavaleiros de bronze, exibindo informações sobre a posição, tempo acumulado e detalhes das batalhas conforme ocorrem.

**3. Configuração e Representação**

* **Mapa:** O ambiente do Santuário é carregado a partir do arquivo `coordernadasmapaco.csv`. A classe `MapaAereo` lê este arquivo e o representa internamente como uma lista de listas (matriz). O tamanho lido foi de 43x43 células, atendendo ao requisito de 42x42 [cite: 30] (a diferença pode ser devido a linhas/colunas extras no CSV). Os valores no CSV definem os tipos de terreno (14, 15, 16), as casas (valores de 1 a 12 ou 2 a 13 - ajustado no código para o intervalo correto encontrado no CSV), a entrada (Valor 0, Vermelho) [cite: 31] e o objetivo (Valor 1, Verde)[cite: 32]. A estrutura do `TERRENOS_INFO` permite fácil modificação das cores e custos associados a cada tipo de terreno[cite: 37].
* **Cavaleiros:** As informações (nome, poder cósmico, energia inicial, caminho do sprite) dos Cavaleiros de Bronze e de Ouro (incluindo dificuldade das casas) são definidas em listas de dicionários (`CAVALEIROS_BRONZE_INFO`, `CAVALEIROS_OURO_INFO`) no início do código, permitindo fácil edição[cite: 39].

### **4 Utilização do Aplicativo**

* **Arquivos:** É necessário ter o script Python (`seu_arquivo.py`) ou o arquivo executável e o arquivo `coordernadasmapaco.csv` no mesmo diretório e a estrutura de pastas com os sprites dos cavaleiros acessível pelo caminho definido na constante `CAMINHO_SPRITE`.

* **Funcionamento:** O programa iniciará, carregará o mapa e os dados. A Fase 1 (Busca A*) será executada (logs no console indicarão o progresso). Se um caminho for encontrado, a Fase 2 (Simulação com Visualização) começará. Uma janela Pygame aparecerá, mostrando o mapa e os cavaleiros. A animação mostrará os cavaleiros de bronze se movendo pelo caminho encontrado, com informações de tempo e batalhas sendo exibidas na tela e no console. A simulação termina quando o objetivo é alcançado, todos os cavaleiros morrem, ou a janela é fechada.
* **Saída:** Ao final da execução (ou interrupção), o console exibirá um resumo final com o status (Sucesso/Falha), o tempo total gasto, um log detalhado das batalhas (casa, equipe, tempo) e as energias finais dos cavaleiros.

**4.1 Com código fonte**

* **Pré-requisitos:** Python 3 e a biblioteca Pygame (`pip install pygame`).
* **Execução:** Abra um terminal ou prompt de comando, navegue até o diretório do projeto e execute: `python seu_arquivo.py`.

**4.1 Com o arquivo binário (Windows 11)**

* **Execução:** Apenas execute o arquivo `main.exe` e o programa executará automaticamente e salvará o log de eventos na pasta `logs`.

**5. Resultados Obtidos**

*(Nota: Preencha esta seção com os resultados REAIS da última execução bem-sucedida do SEU código)*

* **Caminho Percorrido:** O algoritmo A* da Fase 1 encontrou um caminho físico com [Número] passos e um custo total de terreno de [Custo G do A*] minutos. A visualização em tempo real mostra este caminho sendo percorrido.
* **Custo Total Final:** A simulação completa (Fase 1 + Fase 2) resultou em um tempo total de **[Tempo Total Final] minutos**.
* **Status:** [Indicar se foi SUCESSO (tempo <= 720) ou FALHA (tempo > 720 ou outra causa)]
* **Log das Batalhas:**
    * Casa 1 (Mu): Equipe: `[Lista de Nomes]`, Tempo: `X.X` min
    * Casa 2 (Aldebaran): Equipe: `[Lista de Nomes]`, Tempo: `X.X` min
    * Casa 3 (Saga): Equipe: `[Lista de Nomes]`, Tempo: `X.X` min
    * Casa 4 (Máscara da Morte): Equipe: `[Lista de Nomes]`, Tempo: `X.X` min
    * Casa 5 (Aiolia): Equipe: `[Lista de Nomes]`, Tempo: `X.X` min
    * Casa 6 (Shaka): Equipe: `[Lista de Nomes]`, Tempo: `X.X` min
    * Casa 7 (Dohko): Equipe: `[Lista de Nomes]`, Tempo: `X.X` min
    * Casa 8 (Milo): Equipe: `[Lista de Nomes]`, Tempo: `X.X` min
    * Casa 9 (Aiolos): Equipe: `[Lista de Nomes]`, Tempo: `X.X` min
    * Casa 10 (Shura): Equipe: `[Lista de Nomes]`, Tempo: `X.X` min
    * Casa 11 (Camus): Equipe: `[Lista de Nomes]`, Tempo: `X.X` min
    * Casa 12 (Afrodite): Equipe: `[Lista de Nomes]`, Tempo: `X.X` min
* **Energias Finais:** `[Lista de Energias Finais]`

**6. Conclusão**

A solução implementada utiliza uma abordagem híbrida em duas fases para resolver o problema da Travessia das 12 Casas. A Fase 1 emprega o algoritmo A* para determinar o caminho ótimo em termos de custo de terreno, enquanto a Fase 2 simula este caminho e utiliza uma estratégia greedy local para o planejamento das batalhas, balanceando tempo e energia. A visualização em tempo real com Pygame permite acompanhar o progresso do agente.

Esta abordagem demonstrou ser computacionalmente viável, ao contrário de tentativas de resolver ambos os subproblemas simultaneamente com um único A*. A separação permite obter uma solução completa que atende aos requisitos funcionais do trabalho, embora a estratégia greedy para as batalhas não garanta a otimalidade global do tempo total. O sistema é configurável através de arquivos CSV e constantes no código, e apresenta os resultados de forma clara no console e visualmente. Consideramos que o método escolhido é apropriado para a complexidade do problema proposto.

