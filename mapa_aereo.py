import pygame
import csv
import sys
import os # Adicionado para manipulação de caminhos
import time # Adicionado para o temporizador de animação

# Constantes
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
COR_PLANO = (210, 180, 140)
COR_ROCHOSO = (160, 160, 160)
COR_MONTANHOSO = (105, 105, 105)
COR_INICIO = (0, 255, 0)
COR_FIM = (255, 0, 0)
COR_CASAS = (65, 105, 225)
TAMANHO_BLOCO = 15
NOME_ARQUIVO = 'coordernadasmapaco.csv'
# Caminho para a sprite sheet (ajuste se necessário)
CAMINHO_SPRITE = r'/home/alan-moraes/Downloads/' # AJUSTE AQUI O CAMINHO PARA O SPRITES NO SEU COMPUTADOR
CASA_INICIO_PLAYER = 0

# Dados dos Cavaleiros de Bronze
CAVALEIROS_DATA = [
    {"nome": "Seiya/", "sprite_sheet": f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Bronze/Saint Seya Chara - 0001.png', "poder": 1.5},
    {"nome": "Shiryu", "sprite_sheet": f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Bronze/Saint Seya Chara - 0002.png', "poder": 1.4},
    {"nome": "Hyoga", "sprite_sheet": f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Bronze/Saint Seya Chara - 0003.png', "poder": 1.3},
    {"nome": "Shun", "sprite_sheet": f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Bronze/Saint Seya Chara - 0004.png', "poder": 1.2},
    {"nome": "Ikki", "sprite_sheet": f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Bronze/Saint Seya Chara - 0005.png', "poder": 1.1},
]

# Dados dos Cavaleiros de Ouro
GOLD_SAINTS_DATA = [
    {"casa": 1, "nome": "Áries", "sprite_sheet": f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Ouro/_Afrodite.png', "dificuldade": 50, "map_value": 2},
    {"casa": 2, "nome": "Touro", "sprite_sheet": f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Ouro/_Athena_Aioria.png', "dificuldade": 55, "map_value": 3},
    {"casa": 3, "nome": "Gêmeos", "sprite_sheet": f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Ouro/_Athena_Mdm.png', "dificuldade": 60, "map_value": 4},
    {"casa": 4, "nome": "Câncer", "sprite_sheet": f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Ouro/_Athena_Milo.png', "dificuldade": 70, "map_value": 5},
    {"casa": 5, "nome": "Leão", "sprite_sheet": f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Ouro/_Athena_Shaka.png', "dificuldade": 75, "map_value": 6},
    {"casa": 6, "nome": "Virgem", "sprite_sheet": f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Ouro/_Athena_Shura.png', "dificuldade": 80, "map_value": 7},
    {"casa": 7, "nome": "Libra", "sprite_sheet": f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Ouro/#Aldebaran (Taurus).png', "dificuldade": 85, "map_value": 8},
    {"casa": 8, "nome": "Escorpião", "sprite_sheet": f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Ouro/#Athena_Aldebaran.png', "dificuldade": 90, "map_value": 9},
    {"casa": 9, "nome": "Sagitário", "sprite_sheet": f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Ouro/#Athena_Dohko.png', "dificuldade": 95, "map_value": 10},
    {"casa": 10, "nome": "Capricórnio", "sprite_sheet": f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Ouro/KAMUS.png', "dificuldade": 100, "map_value": 11},
    {"casa": 11, "nome": "Aquário", "sprite_sheet": f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Ouro/MU.png', "dificuldade": 110, "map_value": 12},
    {"casa": 12, "nome": "Peixes", "sprite_sheet": f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Ouro/SAGA.png', "dificuldade": 120, "map_value": 13},
]

class GoldSaint(pygame.sprite.Sprite):
    def __init__(self, x_mapa, y_mapa, sprite_path, nome, dificuldade):
        super().__init__()
        self.nome = nome
        self.dificuldade = dificuldade # Mantém a dificuldade para Cavaleiros de Ouro
        self.sprites = {'down': [], 'left': [], 'right': [], 'up': []}
        self.direcao = 'down' # Direção inicial padrão
        self.indice_frame = 0

        # Fallback inicial
        self.image = pygame.Surface((TAMANHO_BLOCO, TAMANHO_BLOCO))
        self.image.fill(BRANCO)
        pygame.draw.circle(self.image, (255, 215, 0), (TAMANHO_BLOCO // 2, TAMANHO_BLOCO // 2), TAMANHO_BLOCO // 2 - 2) # Círculo dourado fallback
        self.rect = self.image.get_rect(topleft=(x_mapa * TAMANHO_BLOCO, y_mapa * TAMANHO_BLOCO))

        # Carrega os sprites da sheet (ou imagem única se for o caso)
        self._load_sprites(sprite_path)

        # Define imagem inicial após carregar
        if self.sprites[self.direcao]:
            self.image = self.sprites[self.direcao][self.indice_frame]
            # Reajusta rect para o tamanho real do sprite carregado/redimensionado
            self.rect = self.image.get_rect(topleft=(x_mapa * TAMANHO_BLOCO, y_mapa * TAMANHO_BLOCO))

        # Controle de Animação
        self.tempo_ultima_animacao = pygame.time.get_ticks()
        # Delay pode ser diferente para os de Ouro, se desejado
        self.delay_animacao = 180 # Milissegundos entre frames

    def _load_sprites(self, sprite_path):
        # Similar ao Player._load_sprites, adaptado para GoldSaint
        if not os.path.exists(sprite_path):
             print(f"Erro: Arquivo de sprite para {self.nome} não encontrado em '{sprite_path}'")
             fallback_sprite = self.image
             for direction in self.sprites.keys():
                 self.sprites[direction] = [fallback_sprite] * 4
             return

        try:
            sheet = pygame.image.load(sprite_path).convert_alpha()
        except pygame.error as e:
            print(f"Erro ao carregar a imagem da sprite sheet para {self.nome}: {e}")
            fallback_sprite = self.image
            for direction in self.sprites.keys():
                 self.sprites[direction] = [fallback_sprite] * 4
            return

        sheet_width, sheet_height = sheet.get_size()

        # Tenta detectar se é uma sprite sheet 4x4 ou uma imagem única
        # Isso é uma heurística, pode precisar de ajuste
        if sheet_width >= TAMANHO_BLOCO * 4 and sheet_height >= TAMANHO_BLOCO * 4:
            # Assume formato 4x4 (como os de bronze)
            sprite_width = sheet_width // 4
            sprite_height = sheet_height // 4
            direcoes_na_sheet = ['down', 'left', 'right', 'up']

            for i, direcao in enumerate(direcoes_na_sheet):
                if direcao in self.sprites:
                    for j in range(4):
                        rect = pygame.Rect(j * sprite_width, i * sprite_height, sprite_width, sprite_height)
                        sprite = pygame.Surface(rect.size, pygame.SRCALPHA)
                        sprite.blit(sheet, (0, 0), rect)
                        sprite = pygame.transform.scale(sprite, (TAMANHO_BLOCO, TAMANHO_BLOCO))
                        self.sprites[direcao].append(sprite)
                else:
                     print(f"Aviso: Direção '{direcao}' inesperada para {self.nome}.")

            # Verifica se carregou algo, senão usa fallback
            if not self.sprites['down']:
                 print(f"Aviso: Falha ao extrair sprites da sheet para {self.nome}. Usando fallback.")
                 fallback_sprite = self.image
                 for direction in self.sprites.keys():
                      self.sprites[direction] = [fallback_sprite] * 4

        else:
            # Assume imagem única, usa para todas as direções/frames
            print(f"Aviso: Sprite para {self.nome} parece ser imagem única. Animação não ocorrerá.")
            sprite = pygame.transform.scale(sheet, (TAMANHO_BLOCO, TAMANHO_BLOCO))
            for direcao in self.sprites.keys():
                self.sprites[direcao] = [sprite] * 4 # Repete a mesma imagem

    def update(self):
        # Similar ao Player.update
        agora = pygame.time.get_ticks()
        # Só anima se houver mais de um frame na direção atual
        if len(self.sprites[self.direcao]) > 1 and agora - self.tempo_ultima_animacao > self.delay_animacao:
            self.tempo_ultima_animacao = agora
            self.indice_frame = (self.indice_frame + 1) % len(self.sprites[self.direcao])
            self.image = self.sprites[self.direcao][self.indice_frame]

class Player(pygame.sprite.Sprite):
    def __init__(self, x_mapa, y_mapa, sprite_sheet_path, nome, poder): # Adicionado nome e poder
        super().__init__()
        self.nome = nome # Adicionado
        self.poder_cosmico = poder # Adicionado
        self.sprites = {'down': [], 'left': [], 'right': [], 'up': []}

        # Define a direção e o frame ANTES de carregar os sprites
        self.direcao = 'down'
        self.indice_frame = 0

        # Inicializa image e rect com um valor padrão antes de carregar
        self.image = pygame.Surface((TAMANHO_BLOCO, TAMANHO_BLOCO))
        self.image.fill(BRANCO) # Cor de fallback inicial
        self.rect = self.image.get_rect(topleft=(x_mapa * TAMANHO_BLOCO, y_mapa * TAMANHO_BLOCO))

        # Agora carrega os sprites
        self._load_sprites(sprite_sheet_path)

        # Define a imagem inicial correta APÓS carregar os sprites (se bem-sucedido)
        if self.sprites[self.direcao]: # Verifica se há sprites para a direção inicial
            self.image = self.sprites[self.direcao][self.indice_frame]
            # Reajusta o rect caso o tamanho do sprite carregado seja diferente (embora redimensionemos)
            # Ajuste para posicionamento inicial ligeiramente diferente
            self.rect = self.image.get_rect(topleft=(x_mapa * TAMANHO_BLOCO, y_mapa * TAMANHO_BLOCO))
        # else: mantém a imagem de fallback definida anteriormente

        self.energia = 5

        # Controle de Animação
        self.tempo_ultima_animacao = pygame.time.get_ticks()
        self.delay_animacao = 150 # Milissegundos entre frames (ajuste para velocidade desejada)

    def _load_sprites(self, sprite_sheet_path):
        """Carrega os sprites da sprite sheet."""
        if not os.path.exists(sprite_sheet_path):
             print(f"Erro: Arquivo de sprite para {self.nome} não encontrado em '{sprite_sheet_path}'") # Nome adicionado
             # A imagem fallback já foi definida no __init__
             # Adiciona esta imagem fallback a todas as direções para evitar erros posteriores
             fallback_sprite = self.image
             for direction in self.sprites.keys():
                 self.sprites[direction] = [fallback_sprite] * 4
             return

        try:
            sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        except pygame.error as e:
            print(f"Erro ao carregar a imagem da sprite sheet para {self.nome}: {e}") # Nome adicionado
            # A imagem fallback já foi definida no __init__
            fallback_sprite = self.image
            for direction in self.sprites.keys():
                 self.sprites[direction] = [fallback_sprite] * 4
            return

        sheet_width, sheet_height = sheet.get_size()
        # Assumindo 4 linhas (direções) e 4 colunas (frames)
        sprite_width = sheet_width // 4
        sprite_height = sheet_height // 4

        # Ordem das direções na sua sprite sheet (ajuste se necessário)
        # Ex: ['down', 'left', 'right', 'up'] se a 1ª linha é para baixo, 2ª esquerda, etc.
        direcoes_na_sheet = ['down', 'left', 'right', 'up'] # Ajuste conforme a sua imagem

        for i, direcao in enumerate(direcoes_na_sheet):
            # Verifica se a direção existe no dicionário antes de adicionar
            if direcao in self.sprites:
                for j in range(4): # 4 frames por direção
                    rect = pygame.Rect(j * sprite_width, i * sprite_height, sprite_width, sprite_height)
                    sprite = pygame.Surface(rect.size, pygame.SRCALPHA)
                    sprite.blit(sheet, (0, 0), rect)

                    # Redimensiona o sprite para o tamanho do bloco do mapa
                    sprite = pygame.transform.scale(sprite, (TAMANHO_BLOCO, TAMANHO_BLOCO))
                    self.sprites[direcao].append(sprite)
            else:
                print(f"Aviso: Direção '{direcao}' inesperada encontrada na sheet ou erro de configuração.")


        # Garante que mesmo que o carregamento falhe parcialmente, haja sprites
        # A definição da imagem inicial agora é feita no __init__ APÓS esta função
        if not self.sprites['down']: # Verifica se a lista de uma direção chave está vazia
             print(f"Aviso: Falha ao extrair sprites para {self.nome}. Usando fallback.") # Nome adicionado
             fallback_sprite = self.image # Usa a imagem fallback já criada
             for direction in self.sprites.keys():
                 if not self.sprites[direction]:
                      self.sprites[direction] = [fallback_sprite] * 4
        # REMOVIDO: A lógica de definir self.image aqui foi movida para __init__

    def update(self):
        """Atualiza a animação do jogador baseado no tempo."""
        agora = pygame.time.get_ticks()
        if agora - self.tempo_ultima_animacao > self.delay_animacao:
            self.tempo_ultima_animacao = agora
            self.indice_frame = (self.indice_frame + 1) % len(self.sprites[self.direcao])
            self.image = self.sprites[self.direcao][self.indice_frame]

    def move(self, dx, dy, mapa_obj):
        """Move o jogador, atualiza a direção e a imagem imediatamente."""
        nova_pos_x = self.rect.x + dx * TAMANHO_BLOCO
        nova_pos_y = self.rect.y + dy * TAMANHO_BLOCO

        nova_direcao = self.direcao # Mantém a direção atual se não houver movimento
        if dx > 0: nova_direcao = 'right'
        elif dx < 0: nova_direcao = 'left'
        elif dy > 0: nova_direcao = 'down'
        elif dy < 0: nova_direcao = 'up'

        # Atualiza a direção e reseta o frame se a direção mudou
        if nova_direcao != self.direcao:
            self.direcao = nova_direcao
            self.indice_frame = 0 # Começa a animação da nova direção do início
            # Garante que a lista de sprites para a nova direção não está vazia
            if self.sprites[self.direcao]:
                 self.image = self.sprites[self.direcao][self.indice_frame]
            # else: mantém a imagem anterior se a nova direção não tiver sprites (improvável com o fallback)


        mapa_x = nova_pos_x // TAMANHO_BLOCO
        mapa_y = nova_pos_y // TAMANHO_BLOCO

        if 0 <= mapa_y < mapa_obj.altura_mapa and 0 <= mapa_x < mapa_obj.largura_mapa:
             self.rect.x = nova_pos_x
             self.rect.y = nova_pos_y

    def draw(self, surface):
        """Desenha o jogador na superfície."""
        surface.blit(self.image, self.rect.topleft)


class MapaAereo:
    def __init__(self, nome_arquivo):
        self.nome_arquivo = nome_arquivo
        self.mapa = self._carregar_mapa()
        if not self.mapa:
            sys.exit("Erro: Mapa não pôde ser carregado.")

        self.largura_mapa = len(self.mapa[0])
        self.altura_mapa = len(self.mapa)
        self.largura_tela = self.largura_mapa * TAMANHO_BLOCO
        self.altura_tela = self.altura_mapa * TAMANHO_BLOCO

        pygame.init()
        self.tela = pygame.display.set_mode((self.largura_tela, self.altura_tela))
        pygame.display.set_caption('Mapa do Santuário - Visão Aérea')

        # self.jogador = None # Removido
        # self.player_sprite_group = pygame.sprite.GroupSingle() # Removido

        self.cavaleiros = []
        self.cavaleiros_sprites = pygame.sprite.Group()
        self._inicializar_cavaleiros()

        # >>> GARANTA QUE ESTAS LINHAS EXISTEM <<<
        self.gold_saints = []
        self.gold_saints_sprites = pygame.sprite.Group()
        self._inicializar_gold_saints() # Chama a função para criar os Cavaleiros de Ouro

    def _carregar_mapa(self):
        """Carrega o mapa do arquivo CSV."""
        mapa_carregado = []
        try:
            with open(self.nome_arquivo, 'r', newline='') as arquivo:
                leitor = csv.reader(arquivo)
                primeira_linha_len = -1 # Para verificar consistência
                for i, linha in enumerate(leitor):
                    # Filtra strings vazias e converte para int
                    linha_int = []
                    for valor in linha:
                        valor_strip = valor.strip()
                        if valor_strip: # Se não for vazio após remover espaços
                            try:
                                linha_int.append(int(valor_strip))
                            except ValueError:
                                print(f"Erro: Valor não numérico '{valor}' encontrado na linha {i+1} do CSV.")
                                return None # Retorna None em caso de erro de valor
                        # else: ignora célula vazia

                    if not linha_int and any(v.strip() for v in linha):
                        # Linha tinha conteúdo não numérico ou apenas espaços/vírgulas extras
                        print(f"Aviso: Linha {i+1} contém dados inválidos ou está mal formatada.")
                        # Decide se quer parar ou continuar (aqui vamos pular a linha)
                        continue # Pula para a próxima linha

                    if linha_int: # Adiciona a linha apenas se não estiver vazia após a filtragem/conversão
                        if primeira_linha_len == -1:
                            primeira_linha_len = len(linha_int)
                        elif len(linha_int) != primeira_linha_len:
                            print(f"Erro: Linha {i+1} tem comprimento {len(linha_int)}, esperado {primeira_linha_len}.")
                            return None # Retorna None se as linhas tiverem comprimentos diferentes
                        mapa_carregado.append(linha_int)

            if not mapa_carregado:
                print("Erro: O mapa carregado está vazio ou o CSV não contém dados válidos.")
                return None

            return mapa_carregado
        except FileNotFoundError:
            print(f"Erro: Arquivo '{self.nome_arquivo}' não encontrado.")
            return None
        # Removido o catch genérico de ValueError aqui, pois tratamos dentro do loop
        except Exception as e:
            print(f"Erro inesperado ao carregar o mapa: {e}")
            return None

    def _obter_cor(self, valor):
        """Retorna a cor correspondente ao valor da célula."""
        if valor == 14:
            return COR_PLANO
        elif valor == 15:
            return COR_ROCHOSO
        elif valor == 16:
            return COR_MONTANHOSO
        elif valor == 1: # Ponto inicial original (verde)
             # Se você mudou o inicial para 0 (vermelho), ajuste aqui e em _encontrar_posicao_inicial
             return COR_INICIO
        elif valor == 0: # Ponto final original (vermelho)
             # Se você mudou o final para 1 (verde), ajuste aqui
             return COR_FIM
        elif 2 <= valor <= 13:
            return COR_CASAS
        else:
            # print(f"Aviso: Valor não mapeado encontrado no mapa: {valor}") # Comentado para não poluir
            return BRANCO # Cor padrão para valores desconhecidos

    def _encontrar_posicao_inicial(self):
        """Encontra as coordenadas (x, y) do ponto inicial no mapa (valor 1)."""
        for y, linha in enumerate(self.mapa):
            for x, valor in enumerate(linha):
                if valor == CASA_INICIO_PLAYER: 
                    return x, y
        print("Aviso: Posição inicial (valor 1) não encontrada no mapa. Usando (0,0).")
        return 0, 0

    def _inicializar_cavaleiros(self): # Renomeado e modificado
        """Cria as instâncias dos cavaleiros na posição inicial."""
        start_x, start_y = self._encontrar_posicao_inicial()
        for i, data in enumerate(CAVALEIROS_DATA):
            # Desloca ligeiramente cada cavaleiro para não ficarem sobrepostos
            # Ajuste o deslocamento (i * TAMANHO_BLOCO / 5) conforme necessário
            offset_x = i * (TAMANHO_BLOCO // len(CAVALEIROS_DATA)) # Espalha dentro do bloco inicial
            
            # Verifica se o sprite sheet existe antes de criar o Player
            if not os.path.exists(data["sprite_sheet"]):
                 print(f"Erro Crítico: Sprite sheet para {data['nome']} não encontrada em {data['sprite_sheet']}")
                 print("Verifique o caminho e o nome do arquivo.")
                 # Decide se quer continuar sem este cavaleiro ou parar
                 # sys.exit(1) # Descomente para parar se um sprite faltar
                 continue # Pula este cavaleiro se o sprite não for encontrado

            cavaleiro = Player(start_x, start_y, data["sprite_sheet"], data["nome"], data["poder"])
            # Ajusta a posição inicial exata após a criação do rect no Player.__init__
            cavaleiro.rect.x += offset_x 
            
            self.cavaleiros.append(cavaleiro)
            self.cavaleiros_sprites.add(cavaleiro)


    def _inicializar_gold_saints(self):
        """Encontra as posições das casas e inicializa os Cavaleiros de Ouro."""
        posicoes_casas = {}
        for y, linha in enumerate(self.mapa):
            for x, valor in enumerate(linha):
                # Verifica se o valor corresponde a uma casa (2 a 13)
                if 2 <= valor <= 13:
                    if valor not in posicoes_casas:
                         posicoes_casas[valor] = (x, y)

        for data in GOLD_SAINTS_DATA:
            map_value = data["map_value"]
            if map_value in posicoes_casas:
                start_x, start_y = posicoes_casas[map_value]
                if not os.path.exists(data["sprite_sheet"]):
                    print(f"Aviso: Sprite sheet para {data['nome']} não encontrada em {data['sprite_sheet']}. Usando fallback.")

                saint = GoldSaint(start_x, start_y, data["sprite_sheet"], data["nome"], data["dificuldade"])
                self.gold_saints.append(saint)
                self.gold_saints_sprites.add(saint) # <<< ESSENCIAL: Adiciona ao grupo
            else:
                print(f"Aviso: Posição para a casa {data['nome']} (valor {map_value}) não encontrada no mapa.")


    def desenhar(self):
        """Desenha o mapa, os cavaleiros de bronze e os de ouro na tela."""
        # Desenha o mapa
        for i, linha in enumerate(self.mapa):
            for j, valor in enumerate(linha):
                x = j * TAMANHO_BLOCO
                y = i * TAMANHO_BLOCO
                cor = self._obter_cor(valor)
                pygame.draw.rect(self.tela, cor, (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO))
                pygame.draw.rect(self.tela, PRETO, (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO), 1)

        # >>> GARANTA QUE ESTA LINHA EXISTE <<<
        self.gold_saints_sprites.draw(self.tela) # Desenha os Cavaleiros de Ouro

        self.cavaleiros_sprites.draw(self.tela) # Desenha os Cavaleiros de Bronze

    def run(self):
        """Executa o loop principal do Pygame."""
        rodando = True
        clock = pygame.time.Clock()

        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                # REMOVIDO/COMENTADO: Controle pelo teclado
                # if evento.type == pygame.KEYDOWN:
                #     dx, dy = 0, 0
                #     if evento.key == pygame.K_LEFT:
                #         dx = -1
                #     elif evento.key == pygame.K_RIGHT:
                #         dx = 1
                #     elif evento.key == pygame.K_UP:
                #         dy = -1
                #     elif evento.key == pygame.K_DOWN:
                #         dy = 1
                #
                #     # Moveria apenas um jogador se descomentado, precisaria de lógica adicional
                #     # if dx != 0 or dy != 0:
                #     #     # Qual cavaleiro mover? Precisa definir a lógica.
                #     #     # Exemplo: self.cavaleiros[0].move(dx, dy, self)
                #     #     pass


            # Atualiza a animação de TODOS os cavaleiros
            self.cavaleiros_sprites.update() # Chama o método update de cada sprite no grupo

            self.desenhar()
            pygame.display.flip()
            clock.tick(30) # Limita a 30 FPS

        pygame.quit()

def main():
    # Verifica se o arquivo CSV do mapa existe
    if not os.path.exists(NOME_ARQUIVO):
        print(f"Erro Crítico: Arquivo do mapa não encontrado em {NOME_ARQUIVO}")
        sys.exit(1)
        
    # A verificação dos sprites agora é feita em _inicializar_cavaleiros

    mapa_aereo = MapaAereo(NOME_ARQUIVO) # Não passa mais o sprite_path aqui
    if mapa_aereo.mapa: # Verifica se o mapa foi carregado com sucesso
        mapa_aereo.run()

if __name__ == '__main__':
    main()