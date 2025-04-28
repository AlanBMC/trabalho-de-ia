Universidade Federal de Mato Grosso 
Instituto de Computação 
TRABALHO PRÁTICO 
INTELIGÊNCIA ARTIFICIAL 
Instruções: 
• Prazo para entrega: 07/05/2025. 
• Para entregar (via AVA até 13:00 horas, horário local): 
o Relatório: 
▪ descrevendo o método utilizado e o motivo de tal escolha; 
▪ indicando a linguagem utilizada; 
▪ explicando como utilizar o aplicativo; 
▪ expondo os resultados obtidos (caminho percorrido; custo do 
caminho percorrido pelo agente). 
o Código fonte e executável. 
o Link para o vídeo de apresentação. O vídeo deve estar acessível. 
• O trabalho deve ser feito em grupos de no máximo 3 alunos. 
• O programa deve ser apresentado durante a aula por todos os membros do grupo: 
o O membro do grupo que não comparecer poderá receber nota zero; 
o Cada membro do grupo deve saber explicar o trabalho. 
Descrição: 
“Durante o torneio da Guerra Galáctica, os Cavaleiros de Bronze descobrem que Saori é 
a reencarnação de Atena e que o Grande Mestre tentou matá-la ainda bebê. Decididos a 
apoiar Saori, os Cavaleiros de Bronze partem para o Santuário para enfrentar o Grande 
Mestre. 
Ao chegar ao Santuário, Saori e os Cavaleiros são recepcionados por Tremy, um 
Cavaleiro de Prata, que ataca o grupo e atinge Saori com uma flecha mortal. 
Para salvar Atena, os Cavaleiros devem percorrer um caminho composto pelas 12 Casas 
do Zodíaco, cada uma protegida por um Cavaleiro de Ouro, e chegar à casa do Grande 
Mestre, o único capaz de remover a flecha do peito de Saori. Para complicar ainda mais, 
os Cavaleiros têm um prazo máximo de 12 horas para realizar essa tarefa! 
O seu objetivo é ajudar Seiya, Shiryu, Hyoga, Shun e Ikki a passar pelas 12 Casas do 
Zodíaco, derrotando todos os Cavaleiros de Ouro e salvando Atena o mais rápido 
possível!”. 
Figura 1. Os Cavaleiros de Bronze. 
Figura 2. As 12 Casas do Zodíaco. 
O Trabalho consiste em implementar um agente capaz de guiar autonomamente Seiya, 
Shiryu, Hyoga, Shun e Ikki pelas 12 Casas do Zodíaco, planejando a melhor forma de 
derrotar os 12 Cavaleiros de Ouro e salvar Atena.  
Para isso, você deve utilizar um dos algoritmos de solução de problemas estudados na 
disciplina de inteligência artificial. 
O agente deve ser capaz de calcular automaticamente a rota para percorrer as 12 Casas 
do Zodíaco e derrotar os 12 Cavaleiros de Ouro. 
O mapa das 12 Casas do Zodíaco é mostrado na Figura 3. 
Figura 3. Mapa das 12 Casas do Zodíaco. 
No caminho das 12 Casas do Zodíaco existem 3 tipos de terrenos: montanhoso (região 
cinza escuro), plano (região cinza) e rochoso (região cinza claro). 
Para passar por cada tipo de terreno, os Cavaleiros gastam uma determinada quantidade 
de tempo: 
• Montanhoso: +200 minutos 
• Plano: +1 minuto 
• Rochoso: +5 minutos 
Os Cavaleiros de Bronze iniciam a sua jornada na entrada do santuário (região em 
vermelho no mapa) e terminam ao chegar à casa do Grande Mestre (região verde no 
mapa). 
Ao chegar a uma Casa do Zodíaco, o agente deve decidir quais Cavaleiros vão lutar contra 
o Cavaleiro de Ouro que protege a casa. Cada Cavaleiro de Ouro apresenta um nível de 
dificuldade diferente. Este nível determina o tempo gasto pelos Cavaleiros de Bronze para 
poder vencê-lo e avançar para a próxima Casa. 
A Tabela 1 mostra os níveis de dificuldade das 12 Casas do Zodíaco. 
Casa 
1° 
Dificuldade 
Casa de Áries 
2° 
50 
Casa de Touro 
3° 
55 
Casa de Gêmeos 
4° 
60 
Casa de Câncer 
5° 
70 
Casa de Leão 
6° 
75 
Casa de Virgem 
7° 
80 
Casa de Libra 
8° 
85 
Casa de Escorpião 
9° 
90 
Casa de Sagitário 
95 
10° Casa de Capricórnio 100 
11° Casa de Aquário 
12° Casa de Peixes 
110 
120 
Tabela 1. Níveis de dificuldade das 12 Casas do Zodíaco. 
O número de Cavaleiros de Bronze participando das batalhas contra os Cavaleiros de 
Ouro influência o tempo gasto na batalha. Além disso, cada Cavaleiro possui um 
determinado nível de poder cósmico que também influencia no tempo gasto nas batalhas. 
Quanto mais Cavaleiros lutando, mais rápido o Cavaleiro de Ouro será derrotado. 
A Tabela 2 mostra o poder cósmico dos Cavaleiros de Bronze. 
Cavaleiro 
Seiya 
Poder Cósmico 
Shiryu 
1.5 
1.4 
Hyoga 
Shun 
1.3 
1.2 
Ikki 
Tabela 2. Poder cósmico dos Cavaleiros de Bronze. 
1.1 
O tempo gasto nas batalhas contra os Cavaleiros de Ouro é dado por: 
�
�𝑒𝑚𝑝𝑜 =
 𝐷𝑖𝑓𝑖𝑐𝑢𝑙𝑑𝑎𝑑𝑒 𝑑𝑎 𝐶𝑎𝑠𝑎
 ∑𝑃𝑜𝑑𝑒𝑟 𝐶𝑜𝑠𝑚𝑖𝑐𝑜 𝑑𝑜𝑠 𝐶𝑎𝑣𝑎𝑙𝑒𝑖𝑟𝑜𝑠 𝑃𝑎𝑡𝑖𝑐𝑖𝑝𝑎𝑛𝑑𝑜 𝑑𝑎 𝐵𝑎𝑡𝑎𝑙ℎ𝑎
 Além do poder cósmico, cada Cavaleiro de Bronze também possui 5 pontos de energia. 
Ao participar de uma batalha, o Cavaleiro perde 1 ponto de energia. Se o Cavaleiro perder 
todos os pontos de energia, ele morre. 
Informações Adicionais: 
• O mapa principal deve ser representado por uma matriz 42 x 42. 
• O agente sempre inicia a jornada na entrada do santuário (região em vermelho no 
mapa).  
• O agente sempre termina a sua jornada ao chegar à casa do Grande Mestre (região 
verde no mapa). 
• O agente não pode andar na diagonal, somente na vertical e na horizontal. 
• O agente obrigatoriamente deve utilizar um algoritmo de busca para encontrar o 
melhor caminho e planejar as batalhas. 
• Deve existir uma maneira de visualizar os movimentos do agente, mesmo que a 
interface seja bem simples. Podendo até mesmo ser uma matriz desenhada e 
atualizada no console. 
• Os mapas devem ser configuráveis, ou seja, deve ser possível modificar o tipo de 
terreno em cada local. O mapa pode ser lido de um arquivo de texto ou deve ser 
facilmente editável no código. 
• A dificuldade das casas e o poder cósmico dos Cavaleiros de Bronze devem ser 
configuráveis e facilmente editáveis. 
• O programa deve apresentar o caminho percorrido. 
• O programa deve exibir o custo do caminho percorrido pelo agente ao terminar a 
execução. 
• O programa deve apresentar as equipes para lutar contra os Cavaleiros de Bronze 
em cada uma das 12 Casas do Zodíaco, bem como o tempo gasto nas batalhas. 
• O programa pode ser implementado em qualquer linguagem. 
Dicas: 
• Neste trabalho existem dois problemas distintos: 
o Encontrar o caminho para passar pelas 12 Casa do Zodíaco e chegar até a 
Casa do Grande Mestre; 
o Encontrar a ordem de equipes para lutar contra os Cavaleiros de Bronze. 
• Os dois problemas podem ser resolvidos individualmente ou tratando ambos em 
um único problema. O grupo deve definir a melhor maneira de estruturar a sua 
solução. 
Apresentação Oral: 
Os alunos devem apresentar oralmente seu trabalho por meio de um vídeo do tipo pitch. 
Nessa apresentação, os alunos devem resumir os principais pontos do projeto e destacar 
os resultados obtidos. Aqui estão algumas diretrizes para a criação desse vídeo: 
• Apresentação: Comece o vídeo apresentando-se. 
• Contextualização do Problema: Forneça um contexto para o problema, explicando 
sua importância e relevância. 
• Solução Proposta: Descreva brevemente a solução que foi desenvolvida para resolver 
o problema. Destaque as principais etapas do processo e as técnicas ou algoritmos 
utilizados. 
• Demonstração: Apresente uma demonstração prática da solução em ação. Isso pode 
envolver a exibição de exemplos de entrada e saída, gráficos ou visualizações dos 
resultados. 
• Conclusão: Agradeça pela oportunidade de apresentar e informe que o trabalho foi 
desenvolvido na disciplina de processamento de imagens. 
• Duração e Formato: Mantenha o vídeo conciso e direto ao ponto, com duração entre 
30 segundos a 5 minutos. Utilize recursos visuais, como gráficos, imagens ou 
animações, para tornar a apresentação mais interessante e envolvente. 
Forma de Avaliação: 
Será avaliado se: 
(1) O trabalho atendeu a todos os requisitos especificados anteriormente; 
(2) Os algoritmos foram implementados e aplicados de forma correta; 
(3) O código foi devidamente organizado; 
(4) O trabalho foi apresentado corretamente; 
(4) O método escolhido é apropriado para o problema. 
Bônus: 
(1) A interface gráfica não é o objetivo desse trabalho, mas quem implementar uma “boa” 
interface gráfica (2D ou 3D) para representar o ambiente e o agente receberá até 1 ponto 
extra na nota. 
(2) O trabalho que conseguir encontrar a melhor solução no menor tempo de execução do 
algoritmo de busca, receberá 1.0 ponto extra na nota.  