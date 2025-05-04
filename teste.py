import pygame
import csv
import sys
import os
import heapq
import random
from itertools import combinations # Importa combinations para escolher_equipe_greedy_final

# --- Constantes ---
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

# Valores do CSV mapeados para Cor e Custo
# Assume-se que o CSV usa 0 para início, 13 para fim, 2-13 para casas, e 14,15,16 para terrenos.
TERRENOS_INFO = {
    # Valor: {'cor': (R,G,B), 'custo': TEMPO, 'nome': 'Nome'}
    15: {'cor': (202, 202, 202), 'custo': 1,   'nome': 'Plano'},        # Cinza Médio
    16: {'cor': (178, 156, 156), 'custo': 5,   'nome': 'Rochoso'},      # Cinza Claro
    14: {'cor': (105, 105, 105), 'custo': 200, 'nome': 'Montanhoso'},   # Cinza Escuro
}
COR_CASAS = (65, 105, 225)   # Azul (Usado para valores 2-13 no mapa)
COR_INICIO = (0, 255, 0)      # Verde (Usado para valor 0 no mapa)
COR_FIM = (255, 0, 0)        # Vermelho (Usado para valor 13 no mapa)
TAMANHO_BLOCO = 15
NOME_ARQUIVO_MAPA = 'coordernadasmapaco.csv' # <<< VERIFIQUE O NOME DO ARQUIVO
VALOR_PONTO_INICIAL = 0 # Valor no CSV que marca o início
VALOR_PONTO_FINAL = 13  # Valor no CSV que marca o fim
# Caminho para a pasta RAIZ onde estão as subpastas "Saint Seiya/..."
CAMINHO_SPRITE = r'/home/alan-moraes/Downloads/' # <<< AJUSTE ESTE CAMINHO SE NECESSÁRIO

# --- Informações Cavaleiros ---
CAVALEIROS_BRONZE_INFO = [
    {'nome': 'Seiya',  'poder': 1.5, 'energia_inicial': 5, 'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Bronze/Saint Seya Chara - 0001.png'},
    {'nome': 'Shiryu', 'poder': 1.4, 'energia_inicial': 5, 'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Bronze/Saint Seya Chara - 0002.png'},
    {'nome': 'Hyoga',  'poder': 1.3, 'energia_inicial': 5, 'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Bronze/Saint Seya Chara - 0003.png'},
    {'nome': 'Shun',   'poder': 1.2, 'energia_inicial': 5, 'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Bronze/Saint Seya Chara - 0004.png'},
    {'nome': 'Ikki',   'poder': 1.1, 'energia_inicial': 5, 'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Bronze/Saint Seya Chara - 0005.png'},
]
NUM_CAVALEIROS_BRONZE = len(CAVALEIROS_BRONZE_INFO)

# Casas numeradas de 2 a 13 para corresponder aos valores esperados no mapa CSV
CAVALEIROS_OURO_INFO = sorted([
    {'casa': 2, 'nome': 'Mu', 'dificuldade': 50, 'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Ouro/MU.png'},
    {'casa': 3, 'nome': 'Aldebaran', 'dificuldade': 55, 'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Ouro/#Aldebaran (Taurus).png'},
    {'casa': 4, 'nome': 'Saga', 'dificuldade': 60, 'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Ouro/SAGA.png'},
    {'casa': 5, 'nome': 'Máscara da Morte', 'dificuldade': 70, 'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Ouro/_Athena_Mdm.png'},
    {'casa': 6, 'nome': 'Aiolia', 'dificuldade': 75, 'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Ouro/_Athena_Aioria.png'},
    {'casa': 7, 'nome': 'Shaka', 'dificuldade': 80, 'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Ouro/_Athena_Shaka.png'},
    {'casa': 8, 'nome': 'Dohko', 'dificuldade': 85, 'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Ouro/#Athena_Dohko.png'},
    {'casa': 9, 'nome': 'Milo', 'dificuldade': 90, 'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Ouro/_Athena_Milo.png'},
    {'casa': 10, 'nome': 'Aiolos', 'dificuldade': 95, 'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Ouro/_Athena_Aiorios.png'},
    {'casa': 11, 'nome': 'Shura', 'dificuldade': 100, 'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Ouro/_Athena_Shura.png'},
    {'casa': 12, 'nome': 'Camus', 'dificuldade': 110, 'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Ouro/KAMUS.png'},
    {'casa': 1, 'nome': 'Afrodite', 'dificuldade': 120, 'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Ouro/_Afrodite.png'},
], key=lambda c: c['casa']) # Ordena pelas casas 2 a 13
NUM_CASAS = len(CAVALEIROS_OURO_INFO) # Deve ser 12

TREMY_INFO = {
    'nome': 'Sagitta Tremy',
    'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Prata/Athena_Sagita.png'
}
# ---------------------------------------------

# --- Funções Auxiliares ---
def calcular_distancia_manhattan(p1, p2):
    """Calcula a distância de Manhattan entre dois pontos (x,y)."""
    if p1 is None or p2 is None: return float('inf')
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# --- Classe Player ---
class Player(pygame.sprite.Sprite):
    def __init__(self, x_mapa, y_mapa, sprite_sheet_path, nome="?", poder=0.0, dificuldade=0, energia_inicial=5):
        super().__init__()
        self.nome = nome
        self.poder_cosmico = poder # Usado para Cavaleiros de Bronze
        self.dificuldade = dificuldade # Usado para Cavaleiros de Ouro
        self.sprites = {'down': [], 'left': [], 'right': [], 'up': []}
        self.direcao = 'down'
        self.indice_frame = 0

        # Posição lógica inicial no mapa (grid)
        self.map_x = x_mapa
        self.map_y = y_mapa

        # Rect inicial (será ajustado após carregar sprite)
        self.rect = pygame.Rect(x_mapa * TAMANHO_BLOCO, y_mapa * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA) # Cria surface transparente

        # Carrega sprites e ajusta imagem/rect inicial
        self._load_sprites(sprite_sheet_path)
        # A posição visual final é definida por set_visual_position

        self.energia = energia_inicial # Usado para Cavaleiros de Bronze
        self.tempo_ultima_animacao = pygame.time.get_ticks()
        self.delay_animacao = 150 # ms entre frames de animação

        # Offset aleatório para visualização (para desempilhar sprites no mesmo bloco)
        self.offset_x = random.randint(-TAMANHO_BLOCO // 4, TAMANHO_BLOCO // 4)
        self.offset_y = random.randint(-TAMANHO_BLOCO // 4, TAMANHO_BLOCO // 4)

        # Define a posição visual inicial (com offset)
        self.set_visual_position(self.map_x, self.map_y)


    def _load_sprites(self, sprite_sheet_path):
        """Carrega sprites de um arquivo, tentando como sheet ou imagem única."""
        if not os.path.exists(sprite_sheet_path):
             # print(f"Erro: Arquivo de sprite não encontrado para {self.nome} em '{sprite_sheet_path}'")
             self._set_fallback_sprites()
             return
        try:
            sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        except pygame.error as e:
            print(f"Erro ao carregar imagem para {self.nome}: {e}")
            self._set_fallback_sprites()
            return

        sheet_width, sheet_height = sheet.get_size()
        num_frames_por_linha = 4 # Assumindo 4 frames de animação por direção
        num_linhas_direcao = 4  # Assumindo 4 direções (down, left, right, up)
        sprite_width = sheet_width // num_frames_por_linha
        sprite_height = sheet_height // num_linhas_direcao

        # Se dimensões não batem com sheet 4x4, tenta carregar como imagem única
        if sprite_width <= 0 or sprite_height <= 0 or sheet_width % num_frames_por_linha != 0 or sheet_height % num_linhas_direcao != 0:
            # print(f"Aviso: Dimensões ({sheet_width}x{sheet_height}) não são 4x4 para {self.nome}. Tentando carregar como imagem única.")
            try:
                sprite = pygame.image.load(sprite_sheet_path).convert_alpha()
                # Redimensiona para caber no bloco, mantendo proporção
                escala = min(TAMANHO_BLOCO / sprite.get_width(), TAMANHO_BLOCO / sprite.get_height()) if sprite.get_width() > 0 and sprite.get_height() > 0 else 1
                novo_w = max(1, int(sprite.get_width() * escala))
                novo_h = max(1, int(sprite.get_height() * escala))
                sprite = pygame.transform.smoothscale(sprite, (novo_w, novo_h))

                # Usa a mesma imagem para todas as direções
                for direcao in ['down', 'left', 'right', 'up']:
                    self.sprites[direcao] = [sprite]
                self.image = sprite
                self.rect = self.image.get_rect() # Atualiza rect para o tamanho do sprite
                # print(f"  -> {self.nome} carregado como imagem única redimensionada.")
                return # Sai após carregar como imagem única
            except Exception as e_load:
                print(f"Falha ao carregar como imagem única para {self.nome}: {e_load}")
                self._set_fallback_sprites()
                return

        # Processamento como spritesheet 4x4
        # print(f"Debug: Processando {self.nome} como spritesheet 4x4 ({sprite_width}x{sprite_height} por frame)")
        direcoes_na_sheet = ['down', 'left', 'right', 'up'] # Ordem comum em sheets
        for i, direcao in enumerate(direcoes_na_sheet):
            self.sprites[direcao] = []
            for j in range(num_frames_por_linha):
                # Define o retângulo (subárea) para extrair o frame
                rect = pygame.Rect(j * sprite_width, i * sprite_height, sprite_width, sprite_height)
                # Verifica se o retângulo está dentro dos limites da sheet
                if sheet.get_rect().contains(rect):
                    try:
                        sub_image = sheet.subsurface(rect)
                        # Redimensiona o frame para caber no TAMANHO_BLOCO
                        escala = min(TAMANHO_BLOCO / sub_image.get_width(), TAMANHO_BLOCO / sub_image.get_height()) if sub_image.get_width() > 0 and sub_image.get_height() > 0 else 1
                        novo_w = max(1, int(sub_image.get_width() * escala))
                        novo_h = max(1, int(sub_image.get_height() * escala))
                        scaled_sprite = pygame.transform.smoothscale(sub_image, (novo_w, novo_h))
                        self.sprites[direcao].append(scaled_sprite)
                    except ValueError as e:
                         # print(f"Erro no subsurface para {self.nome} frame ({j},{i}): {e}")
                         # Adiciona um fallback para este frame específico se falhar
                         self.sprites[direcao].append(self._create_fallback_sprite((255, 0, 0, 150))) # Vermelho translúcido
                else:
                     # print(f"Aviso: Rect {rect} fora dos limites da sheet para {self.nome}")
                     # Não adiciona frame se o rect estiver fora
                     pass # ou adiciona um fallback: self.sprites[direcao].append(self._create_fallback_sprite())

            # Se nenhuma imagem foi carregada para uma direção, usa fallback
            if not self.sprites[direcao]:
                # print(f"Aviso: Nenhum frame carregado para direção '{direcao}' de {self.nome}. Usando fallback.")
                self.sprites[direcao] = [self._create_fallback_sprite()]

        # Define a imagem inicial e o rect baseado no primeiro frame da direção 'down'
        if self.sprites.get('down') and self.sprites['down']:
             self.image = self.sprites['down'][0]
             self.rect = self.image.get_rect()
        else:
             # Se nem 'down' funcionou, usa o fallback geral
             self._set_fallback_sprites()


    def _create_fallback_sprite(self, color=(128, 128, 128, 180)):
        """Cria um sprite quadrado simples como fallback."""
        sprite = pygame.Surface((TAMANHO_BLOCO, TAMANHO_BLOCO), pygame.SRCALPHA)
        sprite.fill(color) # Cinza translúcido por padrão
        pygame.draw.rect(sprite, PRETO, sprite.get_rect(), 1) # Borda preta
        return sprite

    def _set_fallback_sprites(self):
        """Define um sprite fallback para todas as direções e atualiza a imagem."""
        fallback = self._create_fallback_sprite()
        for direction in ['down', 'left', 'right', 'up']:
            self.sprites[direction] = [fallback]
        self.image = fallback
        self.rect = self.image.get_rect()
        self.direcao = 'down' # Reseta direção padrão


    def update(self):
        """Atualiza o frame da animação baseado na direção atual."""
        # Verifica se a lista de sprites para a direção atual existe e tem mais de um frame
        sprite_list = self.sprites.get(self.direcao)
        if not sprite_list or len(sprite_list) <= 1:
            # Se não há animação (ou só 1 frame), garante que a imagem correta está setada
            if sprite_list:
                self.image = sprite_list[0]
            # Se nem lista existe (erro extremo), a imagem fallback já deve estar setada
            return # Não há o que animar

        # Lógica da animação
        agora = pygame.time.get_ticks()
        if agora - self.tempo_ultima_animacao > self.delay_animacao:
            self.tempo_ultima_animacao = agora
            self.indice_frame = (self.indice_frame + 1) % len(sprite_list) # Avança e cicla o frame
            self.image = sprite_list[self.indice_frame]
            # O rect da imagem não muda de tamanho durante a animação,
            # mas a posição PODE mudar se a imagem tiver espaços transparentes diferentes.
            # No entanto, como centralizamos em set_visual_position, deve ficar ok.


    def set_visual_position(self, map_x, map_y):
        """Define a posição VISUAL do sprite na tela, centralizado no bloco do mapa com offset."""
        self.map_x = map_x
        self.map_y = map_y
        # Calcula o centro do bloco no grid do mapa
        centro_x_bloco = (map_x * TAMANHO_BLOCO) + TAMANHO_BLOCO // 2
        centro_y_bloco = (map_y * TAMANHO_BLOCO) + TAMANHO_BLOCO // 2
        # Define o centro do Rect do sprite para ser o centro do bloco + offset
        # Usa o rect atual da imagem (que pode ter sido atualizado no _load_sprites ou update)
        current_rect = self.image.get_rect()
        current_rect.center = (centro_x_bloco + self.offset_x, centro_y_bloco + self.offset_y)
        self.rect = current_rect # Atualiza o rect do sprite

    def draw(self, surface):
        """Desenha o sprite na superfície."""
        surface.blit(self.image, self.rect.topleft)
# --- FIM DA CLASSE PLAYER ---

# --- Classe Luta (Estática) ---
class Luta:
    @staticmethod
    def calcular_tempo_batalha(dificuldade_casa, equipe_indices, cavaleiros_bronze_info):
        """Calcula o tempo de batalha baseado na dificuldade e poder da equipe."""
        soma_poder_cosmico = 0.0
        if not equipe_indices: return float('inf') # Ninguém na equipe

        for indice in equipe_indices:
            if 0 <= indice < len(cavaleiros_bronze_info):
                 soma_poder_cosmico += cavaleiros_bronze_info[indice]['poder']
            else:
                 print(f"Erro Luta: Índice de cavaleiro inválido {indice}")
                 return float('inf') # Índice inválido

        if soma_poder_cosmico <= 0:
            # print("Debug Luta: Poder cósmico da equipe é zero ou negativo.")
            return float('inf') # Evita divisão por zero ou tempo negativo

        tempo = dificuldade_casa / soma_poder_cosmico
        return tempo
# --- FIM DA CLASSE LUTA ---

# --- Classe MapaAereo ---
class MapaAereo:
    def __init__(self, nome_arquivo_mapa, cav_bronze_data, cav_ouro_data, tremy_data):
        self.nome_arquivo = nome_arquivo_mapa
        self.mapa = self._carregar_mapa()
        if not self.mapa:
            sys.exit(f"Erro Crítico: Mapa '{nome_arquivo_mapa}' não pôde ser carregado.")

        self.altura_mapa = len(self.mapa)
        self.largura_mapa = len(self.mapa[0]) if self.altura_mapa > 0 else 0
        if self.largura_mapa == 0:
             sys.exit("Erro Crítico: Mapa carregado está vazio ou inválido.")

        self.largura_tela = self.largura_mapa * TAMANHO_BLOCO
        self.altura_tela = self.altura_mapa * TAMANHO_BLOCO

        # Inicializa Pygame e a tela
        pygame.init()
        pygame.font.init() # Para textos
        try:
            self.tela = pygame.display.set_mode((self.largura_tela, self.altura_tela))
            pygame.display.set_caption('Santuário - Simulação IA')
        except pygame.error as e:
             print(f"ERRO FATAL ao inicializar Pygame/Tela: {e}")
             sys.exit(1)
        self.clock = pygame.time.Clock() # Para controle de FPS

        # Guarda referências aos dados dos cavaleiros
        self.cavaleiros_bronze_info = cav_bronze_data
        self.cavaleiros_ouro_info = cav_ouro_data # Já deve estar ordenado por casa 2-13
        self.tremy_info = tremy_data

        # Encontra posições chave no mapa
        self.posicao_inicial = self._encontrar_posicao_valor(VALOR_PONTO_INICIAL)
        self.posicao_final = self._encontrar_posicao_valor(VALOR_PONTO_FINAL)
        # Encontra posições das casas (valores 2-13)
        self.posicoes_casas_dict = self._encontrar_posicoes_casas(start_val=1, end_val=12)
        # Mapeia as posições encontradas para uma lista na ordem dos cavaleiros de ouro (índice 0 = casa 2, etc.)
        self.posicoes_casas_lista = self._mapear_posicoes_casas_para_lista()

        # Verifica se posições essenciais foram encontradas
        if self.posicao_inicial is None:
             print("Erro Crítico: Posição inicial (valor 0) não encontrada no mapa.")
             pygame.quit(); sys.exit(1)
        if self.posicao_final is None:
             print("Erro Crítico: Posição final (valor 13) não encontrada no mapa.")
             pygame.quit(); sys.exit(1)
        if None in self.posicoes_casas_lista:
             casas_faltantes = [self.cavaleiros_ouro_info[i]['nome'] for i, pos in enumerate(self.posicoes_casas_lista) if pos is None]
             print(f"Erro Crítico: Posições não encontradas no mapa para as casas: {casas_faltantes}. Verifique o CSV.")
             pygame.quit(); sys.exit(1)

        # Grupos de Sprites
        self.grupo_cavaleiros_ouro_fixos = pygame.sprite.Group()
        self.sprite_cavaleiro_prata_fixo = pygame.sprite.GroupSingle() # Grupo para Tremy (fixo)
        self.grupo_cavaleiros_bronze_moveis = pygame.sprite.Group() # Grupo para Bronze (móveis)

        # Inicializa os sprites visuais nas posições corretas
        self._inicializar_sprites_visuais()

        # Fonte para texto na tela
        self.font = None
        try:
            # Tenta carregar uma fonte padrão do sistema
            self.font = pygame.font.SysFont(None, 20) # Tamanho 20
        except Exception as e:
            print(f"Aviso: Erro ao carregar fonte padrão: {e}. Textos não serão exibidos.")


    # --- Métodos Internos da Classe MapaAereo ---
    def _carregar_mapa(self):
         """Carrega o mapa do arquivo CSV, tratando erros e linhas de tamanho variável."""
         mapa_carregado = []
         primeira_linha_len = -1 # Para verificar consistência do tamanho das linhas
         try:
             with open(self.nome_arquivo, 'r', newline='', encoding='utf-8') as arquivo:
                 leitor = csv.reader(arquivo)
                 num_linha = 0
                 for linha in leitor:
                     num_linha += 1
                     # Remove células vazias no FINAL da linha
                     cleaned_line = list(linha)
                     while cleaned_line and not cleaned_line[-1].strip(): # Verifica se é string vazia ou só espaços
                          cleaned_line.pop()

                     if not cleaned_line: continue # Pula linha se ficou completamente vazia

                     linha_int = []
                     num_col = 0
                     for valor_str in cleaned_line:
                         num_col += 1
                         valor_strip = valor_str.strip()
                         if not valor_strip: # Célula ficou vazia após strip
                             # print(f"Aviso Mapa: Célula vazia na linha {num_linha} coluna {num_col}. Tratando como obstáculo (inf).")
                             linha_int.append(None) # Trata como obstáculo/inválido
                             continue
                         try:
                             linha_int.append(int(valor_strip))
                         except ValueError:
                             # print(f"Aviso Mapa: Valor não inteiro '{valor_strip}' na linha {num_linha} col {num_col}. Tratando como obstáculo (inf).")
                             linha_int.append(None) # Tratar como obstáculo

                     # Verifica e ajusta o comprimento da linha para ser consistente
                     if primeira_linha_len == -1:
                         primeira_linha_len = len(linha_int)
                     elif len(linha_int) != primeira_linha_len:
                         # print(f"Aviso Mapa: Linha {num_linha} tem comprimento {len(linha_int)}, esperado {primeira_linha_len}. Ajustando com None...")
                         diff = primeira_linha_len - len(linha_int)
                         if diff > 0:
                             linha_int.extend([None] * diff) # Preenche com None
                         else:
                             linha_int = linha_int[:primeira_linha_len] # Trunca

                     mapa_carregado.append(linha_int)

             if not mapa_carregado or primeira_linha_len <= 0:
                 print("Erro: Mapa vazio ou inválido após carregar."); return None

             print(f"Mapa '{self.nome_arquivo}' carregado: {len(mapa_carregado)} linhas x {primeira_linha_len} colunas.")
             return mapa_carregado
         except FileNotFoundError:
             print(f"Erro Fatal: Arquivo do mapa '{self.nome_arquivo}' não encontrado."); return None
         except Exception as e:
             print(f"Erro inesperado ao carregar mapa: {e}"); return None

    def _obter_cor(self, valor):
         """Retorna a cor correspondente a um valor do mapa."""
         if valor == VALOR_PONTO_INICIAL: return COR_INICIO
         elif valor == VALOR_PONTO_FINAL: return COR_FIM
         elif isinstance(valor, int) and 1 <= valor <= 12: return COR_CASAS # Casas 2-13
         else:
             info_terreno = TERRENOS_INFO.get(valor)
             if info_terreno: return info_terreno['cor']
             else: return PRETO # Cor padrão para obstáculos (None) ou valores não mapeados


    def _obter_custo_terreno(self, x, y):
        """Retorna o custo de movimento para uma coordenada (x,y) do mapa."""
        # Verifica se está dentro dos limites do mapa
        if 0 <= y < self.altura_mapa and 0 <= x < self.largura_mapa:
            valor = self.mapa[y][x]

            # Verifica se é Ponto Inicial, Final ou Casa (custo 1)
            if valor == VALOR_PONTO_INICIAL or valor == VALOR_PONTO_FINAL or \
               (isinstance(valor, int) and 1 <= valor <= 12):
                return 1

            # Verifica se é um terreno mapeado
            info_terreno = TERRENOS_INFO.get(valor)
            if info_terreno:
                return info_terreno['custo']
            else:
                # Valor é None (obstáculo explícito) ou não mapeado -> Custo infinito
                return float('inf')
        else:
            # Fora do mapa -> Custo infinito
            return float('inf')

    def _encontrar_posicao_valor(self, valor_procurado):
        """Encontra a primeira ocorrência de um valor no mapa e retorna suas coordenadas (x, y)."""
        for y, linha in enumerate(self.mapa):
            for x, valor_celula in enumerate(linha):
                if valor_celula == valor_procurado:
                    # print(f"Debug: Valor {valor_procurado} encontrado em ({x},{y})")
                    return x, y
        # print(f"Aviso: Valor {valor_procurado} não encontrado no mapa.")
        return None # Retorna None se não encontrar

    def _encontrar_posicoes_casas(self, start_val=1, end_val=12):
        """Encontra as posições de todos os valores entre start_val e end_val no mapa."""
        posicoes = {} # Dicionário para armazenar {valor_casa: (x, y)}
        for y, linha in enumerate(self.mapa):
            for x, valor in enumerate(linha):
                 if isinstance(valor, int) and start_val <= valor <= end_val:
                    if valor not in posicoes: # Guarda apenas a primeira ocorrência
                        posicoes[valor] = (x, y)
                        # print(f"Debug: Casa com valor {valor} encontrada em ({x},{y})")
                    # else: # Se encontrar duplicatas, pode ser útil avisar
                        # print(f"Aviso: Valor de casa duplicado {valor} encontrado em ({x},{y}). Usando a primeira ocorrência.")

        # Verifica se todas as casas esperadas foram encontradas
        casas_faltando = [i for i in range(start_val, end_val + 1) if i not in posicoes]
        if casas_faltando:
             print(f"Aviso: Números de casa não encontrados no mapa: {casas_faltando}")
        return posicoes

    def _mapear_posicoes_casas_para_lista(self):
        """
        Cria uma lista de posições (x,y) na ordem dos cavaleiros de ouro.
        Assume que self.cavaleiros_ouro_info está ordenado por 'casa' (2 a 13).
        Assume que self.posicoes_casas_dict contém {valor_mapa: (x,y)} para valores 2 a 13.
        """
        lista_pos = [None] * NUM_CASAS # Cria lista de tamanho 12 (para casas 2 a 13)
        for i, cav_ouro in enumerate(self.cavaleiros_ouro_info):
             casa_num_mapa = cav_ouro['casa'] # Este é o valor esperado no mapa (2 a 13)
             pos = self.posicoes_casas_dict.get(casa_num_mapa) # Busca a posição no dict
             if pos:
                 lista_pos[i] = pos # Armazena a posição (x,y) no índice correspondente (0 a 11)
             # else: O erro já foi reportado em __init__ se pos é None
        return lista_pos

    def _inicializar_sprites_visuais(self):
        """Cria e posiciona todos os sprites iniciais (fixos e móveis)."""
        self.grupo_cavaleiros_ouro_fixos.empty()
        self.sprite_cavaleiro_prata_fixo.empty()
        self.grupo_cavaleiros_bronze_moveis.empty()

        # --- Validação Essencial ---
        if self.posicao_inicial is None:
            print("ERRO CRÍTICO: Posição inicial não definida. Não é possível inicializar sprites.")
            # Deveria ter saído no __init__, mas é uma checagem extra
            pygame.quit(); sys.exit(1)

        start_x, start_y = self.posicao_inicial
        # print(f'Debug: Posição inicial ({start_x},{start_y}) encontrada para inicializar sprites.')

        # --- Ouro FIXOS (nas suas casas 2-13) ---
        for i, info in enumerate(self.cavaleiros_ouro_info):
            # posicoes_casas_lista já mapeia o índice 0..11 para as posições das casas 2..13
            pos = self.posicoes_casas_lista[i]
            if pos:
                # Cria o sprite na posição (x_mapa, y_mapa) da casa
                sprite = Player(pos[0], pos[1], info['sprite_path'], info['nome'], 0.0, info['dificuldade'])
                self.grupo_cavaleiros_ouro_fixos.add(sprite)
            # else: O erro já foi reportado no __init__

        # --- Prata FIXO (na Posição Inicial - Casa 0) ---
        if self.tremy_info:
             # Cria o sprite de Tremy usando as coordenadas da posição inicial (start_x, start_y)
             # print(f"Debug: Criando Tremy Fixo em ({start_x},{start_y})")
             sprite_tremy = Player(start_x, start_y, self.tremy_info['sprite_path'], self.tremy_info['nome'])
             # Adiciona ao grupo de sprite ÚNICO e FIXO
             self.sprite_cavaleiro_prata_fixo.add(sprite_tremy)
        else:
             print("Aviso: Informações de Tremy não fornecidas.")


        # --- Bronze MÓVEIS (começam na Posição Inicial - Casa 0) ---
        # Eles também começam em start_x, start_y, mas estão no grupo que se move
        # print(f"Debug: Criando Cavaleiros de Bronze Móveis em ({start_x},{start_y})")
        for info in self.cavaleiros_bronze_info:
            # Cria o sprite na posição inicial (x_mapa, y_mapa)
            sprite_anim = Player(start_x, start_y, info['sprite_path'], info['nome'])
            # Adiciona ao grupo de sprites MÓVEIS
            self.grupo_cavaleiros_bronze_moveis.add(sprite_anim)

        # print("Debug: Inicialização de sprites visuais concluída.")
        # print(f"  - Ouro Fixos: {len(self.grupo_cavaleiros_ouro_fixos)} sprites")
        # print(f"  - Prata Fixo: {'Sim' if self.sprite_cavaleiro_prata_fixo.sprite else 'Não'}")
        # print(f"  - Bronze Móveis: {len(self.grupo_cavaleiros_bronze_moveis)} sprites")

    # --- Métodos Públicos da Classe MapaAereo ---
    def desenhar_estado_simulacao(self, texto_info_passo="", texto_info_batalha=""):
        """Desenha o estado atual do mapa, sprites e informações na tela."""
        try:
            self.tela.fill(PRETO) # Limpa a tela com fundo preto

            # Desenha o Mapa (terrenos, casas, início, fim)
            for i, linha in enumerate(self.mapa):
                for j, valor in enumerate(linha):
                    x = j * TAMANHO_BLOCO
                    y = i * TAMANHO_BLOCO
                    cor = self._obter_cor(valor)
                    pygame.draw.rect(self.tela, cor, (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO))
                    # Desenha grade (opcional)
                    # pygame.draw.rect(self.tela, BRANCO, (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO), 1)

            # Desenha Sprites Fixos (Ouro e Prata)
            self.grupo_cavaleiros_ouro_fixos.draw(self.tela)
            self.sprite_cavaleiro_prata_fixo.draw(self.tela) # Tremy fixo

            # Desenha Sprites Móveis (Bronze)
            # É importante desenhar os móveis por último para que apareçam "por cima"
            self.grupo_cavaleiros_bronze_moveis.draw(self.tela)

            # Desenha Textos de Informação (se a fonte foi carregada)
            if self.font:
                y_offset = 5 # Posição Y inicial para o texto
                # Texto do passo atual
                if texto_info_passo:
                    img_passo = self.font.render(texto_info_passo, True, BRANCO, PRETO) # Texto branco, fundo preto
                    self.tela.blit(img_passo, (5, y_offset))
                    y_offset += img_passo.get_height() + 2 # Move para baixo para o próximo texto

                # Texto da última batalha
                if texto_info_batalha:
                    img_batalha = self.font.render(texto_info_batalha, True, BRANCO, PRETO)
                    self.tela.blit(img_batalha, (5, y_offset))

            # Atualiza a tela inteira para mostrar o que foi desenhado
            pygame.display.flip()

        except Exception as e:
            print(f"ERRO FATAL durante o desenho: {e}")
            pygame.quit()
            sys.exit(1)
# --- FIM DA CLASSE MapaAereo ---


# --- Classe A* Simplificada (Fase 1: Caminho Físico) ---
class BuscaAEstrelaCaminho:
    """Encontra o caminho físico entre waypoints usando A* com custo de terreno."""

    def __init__(self, mapa_obj):
        self.mapa_obj = mapa_obj
        self.waypoints = [] # Lista de coordenadas (x,y) a serem visitadas em ordem

        # --- Construção Sequencial da Lista de Waypoints ---
        # 1. Ponto Inicial (Obrigatório)
        if mapa_obj.posicao_inicial:
            self.waypoints.append(mapa_obj.posicao_inicial)
        else:
            print("ERRO A* Path: Posição inicial não encontrada no mapa_obj.")
            self.waypoints = None; return # Invalida waypoints

        # 2. Posições das Casas (Obrigatórias, na ordem)
        #    mapa_obj.posicoes_casas_lista já está na ordem correta (índice 0 = pos da casa 2, etc.)
        #    e já foi validado no __init__ do MapaAereo se alguma está faltando.
        casas_validas = [p for p in mapa_obj.posicoes_casas_lista if p is not None]
        for casa_pos in casas_validas:
             # Evita adicionar a mesma coordenada consecutivamente (se casa for no mesmo lugar da anterior)
            if not self.waypoints or self.waypoints[-1] != casa_pos:
                self.waypoints.append(casa_pos)

        # 3. Ponto Final (Obrigatório)
        if mapa_obj.posicao_final:
            # Evita adicionar se for igual ao último waypoint (última casa = ponto final)
            if not self.waypoints or self.waypoints[-1] != mapa_obj.posicao_final:
                 self.waypoints.append(mapa_obj.posicao_final)
        else:
            print("ERRO A* Path: Posição final não encontrada no mapa_obj.")
            self.waypoints = None; return # Invalida waypoints
        # --- Fim da Construção ---

        if not self.waypoints:
             print("ERRO A* Path: Falha ao construir lista de waypoints.")
             return

        # print(f"Debug A* Path: Waypoints definidos ({len(self.waypoints)}): {self.waypoints}")

        # Verificação de sanidade: Deve ter pelo menos início + fim
        if len(self.waypoints) < 2:
             print(f"Erro A* Path: Waypoints insuficientes ({len(self.waypoints)}). Necessário pelo menos Início e Fim.")
             self.waypoints = None # Invalida waypoints


    def buscar(self):
        """Executa o algoritmo A* para encontrar o caminho entre os waypoints."""
        if not self.waypoints:
             print("A* Busca: Não pode buscar, waypoints inválidos.")
             return None

        caminho_completo_coords = []
        num_waypoints = len(self.waypoints)

        # Itera por cada segmento do caminho (Waypoint N -> Waypoint N+1)
        for i in range(num_waypoints - 1):
            inicio_segmento = self.waypoints[i]
            objetivo_segmento = self.waypoints[i+1]

            # print(f"\n--- A* Buscando Segmento {i+1}/{num_waypoints-1}: {inicio_segmento} -> {objetivo_segmento} ---")

            # --- A* para um único segmento ---
            open_set = [] # Fila de prioridade (min-heap)
            # Estado na fila: (f_cost, g_cost, (x, y))
            h_inicial = calcular_distancia_manhattan(inicio_segmento, objetivo_segmento)
            heapq.heappush(open_set, (h_inicial, 0.0, inicio_segmento))

            came_from = {inicio_segmento: None} # Rastreia o nó anterior para reconstruir o caminho
            g_score = {inicio_segmento: 0.0} # Custo (terreno) do início até um nó

            max_iter_segmento = 10000 # Limite de iterações por segurança
            iter_count_segmento = 0
            segmento_encontrado = False

            while open_set and iter_count_segmento < max_iter_segmento:
                iter_count_segmento += 1
                f_atual, g_atual, pos_atual = heapq.heappop(open_set)

                # Se já encontramos um caminho melhor para este nó, ignora
                if g_atual > g_score.get(pos_atual, float('inf')):
                    continue

                # Chegou ao objetivo do segmento?
                if pos_atual == objetivo_segmento:
                    # print(f"  Segmento encontrado! Custo g (terreno): {g_atual:.1f} ({iter_count_segmento} iterações)")
                    path_segmento = self._reconstruir_caminho_segmento(came_from, pos_atual)
                    if not caminho_completo_coords: # Primeiro segmento
                        caminho_completo_coords.extend(path_segmento)
                    else:
                        # Adiciona o segmento, mas pula o primeiro ponto (que é o final do segmento anterior)
                        caminho_completo_coords.extend(path_segmento[1:])
                    segmento_encontrado = True
                    break # Passa para o próximo segmento

                # Explora vizinhos (Norte, Sul, Leste, Oeste)
                px, py = pos_atual
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # Movimentos possíveis
                    vizinho_pos = (px + dx, py + dy)
                    nx, ny = vizinho_pos

                    # Obtém o custo de mover para o vizinho
                    custo_movimento = self.mapa_obj._obter_custo_terreno(nx, ny)

                    # Se o vizinho é válido (dentro do mapa e não obstáculo)
                    if custo_movimento != float('inf'):
                        novo_g = g_atual + custo_movimento # Custo acumulado para chegar ao vizinho

                        # Se este caminho para o vizinho é melhor que qualquer anterior
                        if novo_g < g_score.get(vizinho_pos, float('inf')):
                            g_score[vizinho_pos] = novo_g
                            came_from[vizinho_pos] = pos_atual # Registra de onde viemos
                            # Calcula heurística (distância até o OBJETIVO DO SEGMENTO)
                            h_vizinho = calcular_distancia_manhattan(vizinho_pos, objetivo_segmento)
                            f_novo = novo_g + h_vizinho # Custo f = g + h
                            heapq.heappush(open_set, (f_novo, novo_g, vizinho_pos))

            # --- Fim do A* para o segmento ---
            if not segmento_encontrado:
                 print(f"ERRO A* Path: Falha ao encontrar caminho para o segmento {i+1}: {inicio_segmento} -> {objetivo_segmento} (Iterações: {iter_count_segmento})")
                 return None # Aborta a busca completa se um segmento falhar

        # print(f"\n--- A* Caminho Completo Encontrado ({len(caminho_completo_coords)} passos) ---")
        return caminho_completo_coords


    def _reconstruir_caminho_segmento(self, came_from, no_final):
         """Reconstrói a lista de coordenadas (x,y) de um segmento do caminho."""
         path = []
         curr = no_final
         while curr is not None:
              path.append(curr)
              curr = came_from.get(curr)
         path.reverse() # O caminho é reconstruído do fim para o início
         return path

# --- FIM DA CLASSE BuscaAEstrelaCaminho ---


# --- Fase 2: Simulação e Escolha Greedy de Equipes ---

def escolher_equipe_greedy_final(casa_index, energias_atuais, cav_ouro_info, cav_bronze_info):
    """
    Escolhe a melhor equipe para uma casa, priorizando o menor tempo de batalha,
    mas com um limite no tamanho máximo da equipe.
    Se nenhuma equipe dentro do limite funcionar, tenta usar todos os vivos como fallback.
    """
    from itertools import combinations # Garante que combinations está disponível
    if not (0 <= casa_index < len(cav_ouro_info)):
        return None, "Erro: Índice de casa inválido"

    dificuldade_casa = cav_ouro_info[casa_index]['dificuldade']
    # Lista de cavaleiros vivos com seus dados: (indice_original, poder, energia_atual)
    vivos = [(i, cb['poder'], energias_atuais[i])
             for i, cb in enumerate(cav_bronze_info) if energias_atuais[i] > 0]

    if not vivos:
        return None, "Nenhum cavaleiro de bronze vivo"

    melhor_equipe_geral_indices = None
    menor_tempo_geral = float('inf')
    # --- Limite o tamanho máximo da equipe a ser considerada na busca inicial ---
    max_tam_equipe_greedy = 2 # Exemplo: Considera equipes de 1 ou 2 cavaleiros primeiro
    # -------------------------------------------------------------------------

    # Avalia equipes de tamanho 1 até o limite definido (ou até o número de vivos, se menor)
    for tam in range(1, min(len(vivos), max_tam_equipe_greedy) + 1):
        melhor_equipe_tam = None
        menor_tempo_tam = float('inf')

        # Gera todas as combinações de 'tam' cavaleiros vivos
        for combo_tuplas in combinations(vivos, tam):
            indices = [item[0] for item in combo_tuplas] # Índices originais dos cavaleiros na combinação
            poder_total = sum(item[1] for item in combo_tuplas) # Soma o poder deles

            if poder_total > 0:
                tempo_batalha = dificuldade_casa / poder_total
                # Se esta combinação é a melhor para este tamanho de equipe
                if tempo_batalha < menor_tempo_tam:
                    menor_tempo_tam = tempo_batalha
                    melhor_equipe_tam = indices

        # Compara a melhor equipe deste tamanho com a melhor geral encontrada até agora
        if melhor_equipe_tam and menor_tempo_tam < menor_tempo_geral:
            menor_tempo_geral = menor_tempo_tam
            melhor_equipe_geral_indices = melhor_equipe_tam

    # Se encontramos uma boa equipe dentro do limite de tamanho, retorna ela
    if melhor_equipe_geral_indices is not None:
         motivo = f"Greedy (Tam <= {max_tam_equipe_greedy}, T: {menor_tempo_geral:.1f})"
         return melhor_equipe_geral_indices, motivo

    # --- Fallback: Se nenhuma equipe limitada funcionou, tenta usar TODOS os vivos ---
    # print(f"Debug Greedy: Nenhuma equipe com até {max_tam_equipe_greedy} cavaleiros foi ótima. Tentando todos os {len(vivos)} vivos.")
    todos_indices = [item[0] for item in vivos]
    poder_todos = sum(item[1] for item in vivos)
    if poder_todos > 0:
        tempo_todos = dificuldade_casa / poder_todos
        # Considera usar todos APENAS se nenhuma outra equipe funcionou E se eles podem vencer
        motivo = f"Fallback (Todos {len(vivos)} vivos, T: {tempo_todos:.1f})"
        return todos_indices, motivo
    else:
        # Nem todos juntos conseguem (poder total zero)
        return None, "Nenhuma equipe pode vencer (Poder total 0)"


def simular_caminho_e_lutas_com_visualizacao(caminho_coords, mapa_obj):
    """
    Executa a simulação passo a passo, movendo os sprites, calculando custos,
    realizando batalhas e atualizando a visualização Pygame.
    """
    if not caminho_coords or mapa_obj.posicao_inicial is None:
        print("Erro simulação: Caminho físico ou posição inicial inválidos.")
        return 0, [], [], "Erro inicial"

    tempo_total = 0.0
    energias_atuais = [cb['energia_inicial'] for cb in mapa_obj.cavaleiros_bronze_info]
    battle_log = [] # Lista para registrar as batalhas: [(casa_idx, nomes, tempo, energias_depois)]
    # Mapeia coordenada (x,y) da casa para o índice (0-11) na lista cavaleiros_ouro_info
    mapa_casas_coord_idx = {coord: idx for idx, coord in enumerate(mapa_obj.posicoes_casas_lista) if coord is not None}
    status_final = "Não iniciado"

    # Configurações da visualização
    texto_info_passo = "Iniciando Simulação..."
    texto_info_batalha = ""
    battle_info_display_duration = 2500 # ms para mostrar info da batalha
    last_battle_info_time = -battle_info_display_duration # Garante que não mostra nada no início
    delay_movimento = 130 # ms entre passos de movimento (menor = mais rápido)
    target_fps = 1000 // delay_movimento if delay_movimento > 0 else 60 # FPS alvo

    print("\n--- Iniciando Simulação com Visualização (Fase 2) ---")
    print(f"Energias Iniciais: {energias_atuais}")

    rodando_visualizacao = True
    passo_caminho_idx = 0 # Índice do passo atual no caminho_coords

    while rodando_visualizacao and passo_caminho_idx < len(caminho_coords):
        # --- Processar Eventos Pygame (fechar janela, etc.) ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando_visualizacao = False
                status_final = "Visualização Interrompida"
                print(f"\n{status_final}")
                break
        if not rodando_visualizacao: break # Sai do loop while se a janela foi fechada

        # --- Lógica do Passo Atual ---
        pos_atual_coord = caminho_coords[passo_caminho_idx]

        # Calcular Custo da Viagem (apenas se não for o primeiro passo)
        if passo_caminho_idx > 0:
             # O custo é do terreno ONDE ESTAMOS ENTRANDO (pos_atual_coord)
             custo_viagem = mapa_obj._obter_custo_terreno(pos_atual_coord[0], pos_atual_coord[1])
             if custo_viagem == float('inf'):
                  # Isso não deveria acontecer se o A* funcionou corretamente
                  print(f"ERRO FATAL Simulação: Movimento para coordenada inválida/obstáculo {pos_atual_coord} no caminho.")
                  status_final = "Erro no caminho (obstáculo)"; rodando_visualizacao = False; break
             tempo_total += custo_viagem
             texto_info_passo = f"Pos:{pos_atual_coord} T Viagem: +{custo_viagem:.0f} = {tempo_total:.1f} min"
        else:
             # Primeiro passo (posição inicial) - sem custo de viagem
             texto_info_passo = f"Pos:{pos_atual_coord} T Total: {tempo_total:.1f} min"

        # --- Atualizar Posição Visual dos Sprites Móveis (Bronze) ---
        pos_proxima_coord = caminho_coords[passo_caminho_idx + 1] if passo_caminho_idx + 1 < len(caminho_coords) else pos_atual_coord
        dx = pos_proxima_coord[0] - pos_atual_coord[0]
        dy = pos_proxima_coord[1] - pos_atual_coord[1]

        for sprite_b in mapa_obj.grupo_cavaleiros_bronze_moveis:
            # Define a posição visual do sprite para o bloco atual
            sprite_b.set_visual_position(pos_atual_coord[0], pos_atual_coord[1])
            # Define a direção do sprite com base no próximo movimento
            if dx > 0: sprite_b.direcao = 'right'
            elif dx < 0: sprite_b.direcao = 'left'
            elif dy > 0: sprite_b.direcao = 'down'
            elif dy < 0: sprite_b.direcao = 'up'
            # else: fica na direção anterior se dx e dy forem 0 (parado)

        # --- Lógica de Batalha (se a posição atual for uma casa) ---
        texto_info_batalha_atual = "" # Reseta a info da batalha para este passo
        if pos_atual_coord in mapa_casas_coord_idx:
            casa_index = mapa_casas_coord_idx[pos_atual_coord] # Obtém índice 0-11

            # Verifica se já lutamos nesta casa (evita lutar múltiplas vezes se o caminho passa pela mesma casa)
            if not any(log[0] == casa_index for log in battle_log):
                nome_casa = mapa_obj.cavaleiros_ouro_info[casa_index]['nome']
                dificuldade_casa = mapa_obj.cavaleiros_ouro_info[casa_index]['dificuldade']
                print(f"\n-- Chegou na Casa {casa_index+2} ({nome_casa}) em {pos_atual_coord} | T:{tempo_total:.1f} --") # Mostra casa 2 a 13
                print(f"   Energias Atuais: {[f'{mapa_obj.cavaleiros_bronze_info[i]['nome'][0]}:{energias_atuais[i]}' for i in range(len(energias_atuais))]}")

                # ---> Escolhe a equipe usando a função Greedy <---
                equipe_escolhida_indices, motivo_escolha = escolher_equipe_greedy_final(
                    casa_index, energias_atuais, mapa_obj.cavaleiros_ouro_info, mapa_obj.cavaleiros_bronze_info
                )

                if equipe_escolhida_indices is None:
                    # Se nenhuma equipe pode vencer
                    print(f"   FALHA NA SIMULAÇÃO: {motivo_escolha} na casa de {nome_casa}.")
                    texto_info_batalha_atual = f"FALHA! {nome_casa}: {motivo_escolha}!"
                    status_final = f"Falha-{nome_casa}"; rodando_visualizacao = False; break
                else:
                    # Calcula tempo da batalha com a equipe escolhida
                    tempo_batalha = Luta.calcular_tempo_batalha(dificuldade_casa, equipe_escolhida_indices, mapa_obj.cavaleiros_bronze_info)
                    tempo_total += tempo_batalha
                    equipe_nomes = []
                    # Aplica perda de energia e obtém nomes
                    for indice in equipe_escolhida_indices:
                        energias_atuais[indice] -= 1
                        equipe_nomes.append(mapa_obj.cavaleiros_bronze_info[indice]['nome'])
                    energias_depois_tupla = tuple(energias_atuais) # Guarda estado das energias após a luta

                    # Registra a batalha
                    battle_log.append((casa_index, equipe_nomes, tempo_batalha, energias_depois_tupla))

                    # Prepara texto para exibição e log
                    texto_info_batalha_atual = f"Luta! {nome_casa}: [{', '.join(equipe_nomes)}] (T: {tempo_batalha:.1f})"
                    print(f"   Luta Casa {nome_casa}: Equipe: {equipe_nomes} ({motivo_escolha}).")
                    print(f"   Tempo Batalha: {tempo_batalha:.1f}. T Total: {tempo_total:.1f}")
                    print(f"   Energias Após: {[f'{mapa_obj.cavaleiros_bronze_info[i]['nome'][0]}:{energias_atuais[i]}' for i in range(len(energias_atuais))]}")
                    last_battle_info_time = pygame.time.get_ticks() # Marca quando a info da batalha deve começar a ser mostrada

                    # Verifica se todos morreram após a batalha
                    if all(e <= 0 for e in energias_atuais):
                        print("   FALHA: Todos os cavaleiros de bronze morreram.")
                        texto_info_batalha_atual += " - TODOS MORRERAM!"
                        status_final = "Todos morreram"; rodando_visualizacao = False; break

        # --- Atualização e Desenho ---
        # Atualiza animação dos sprites (todos os grupos)
        mapa_obj.grupo_cavaleiros_bronze_moveis.update()
        mapa_obj.grupo_cavaleiros_ouro_fixos.update()
        mapa_obj.sprite_cavaleiro_prata_fixo.update()

        # Define qual texto de batalha mostrar (o atual ou o último por um tempo)
        agora = pygame.time.get_ticks()
        info_batalha_visivel = texto_info_batalha_atual
        if not info_batalha_visivel and (agora - last_battle_info_time < battle_info_display_duration):
             # Se não houve batalha neste passo, mas a última foi recente, mostra a info da última
             if battle_log:
                  last_log = battle_log[-1]
                  nome_casa_log = mapa_obj.cavaleiros_ouro_info[last_log[0]]['nome']
                  info_batalha_visivel = f"Luta! {nome_casa_log}: [{', '.join(last_log[1])}] (T: {last_log[2]:.1f})"

        # Desenha tudo na tela
        mapa_obj.desenhar_estado_simulacao(texto_info_passo, info_batalha_visivel)

        # Controla a velocidade da simulação
        mapa_obj.clock.tick(target_fps) # Tenta manter o FPS alvo

        # Avança para o próximo passo do caminho
        passo_caminho_idx += 1

    # --- Fim do Loop de Simulação ---
    if rodando_visualizacao and status_final == "Não iniciado":
        # Se o loop terminou normalmente (chegou ao fim do caminho)
        status_final = "Sucesso"
        print("\n--- Simulação com Visualização Concluída ---")
        # Mostra estado final por alguns segundos
        mapa_obj.desenhar_estado_simulacao("Caminho Concluído!", f"Tempo Final: {tempo_total:.1f}")
        pygame.time.wait(3000) # Espera 3 segundos

    # Fecha o Pygame de forma limpa
    pygame.quit()

    return tempo_total, battle_log, energias_atuais, status_final
# --- FIM DA FASE 2 ---


# --- Ponto de Entrada Principal ---
def main():
    """Função principal que orquestra a execução."""
    # Verifica se o arquivo do mapa existe
    if not os.path.exists(NOME_ARQUIVO_MAPA):
        print(f"Erro Fatal: Arquivo do mapa '{NOME_ARQUIVO_MAPA}' não encontrado no diretório atual ou caminho especificado.")
        print(f"Verifique se o nome está correto e se o arquivo está no lugar esperado.")
        sys.exit(1)

    print("Inicializando MapaAereo e carregando dados...")
    # Cria a instância do MapaAereo, que também inicializa Pygame e carrega o mapa
    mapa_aereo = MapaAereo(NOME_ARQUIVO_MAPA,
                           CAVALEIROS_BRONZE_INFO,
                           CAVALEIROS_OURO_INFO,
                           TREMY_INFO)
    # O __init__ do MapaAereo já faz as validações críticas (mapa, posições),
    # então não precisamos repetir aqui. O programa já teria saído se algo falhasse.
    print("MapaAereo inicializado com sucesso.")

    print("\n--- Fase 1: Buscando Caminho Físico (A*) ---")
    buscador_caminho = BuscaAEstrelaCaminho(mapa_aereo)
    if buscador_caminho.waypoints is None:
         print("Falha ao definir os waypoints necessários para o A*. Abortando."); sys.exit(1)

    caminho_coords = buscador_caminho.buscar()

    if not caminho_coords:
        print("Falha ao encontrar o caminho físico entre os waypoints. Abortando."); sys.exit(1)
    print(f"Caminho físico encontrado com {len(caminho_coords)} passos.")
    # print(f"  Caminho: {caminho_coords}") # Descomente para ver o caminho detalhado

    # --- Fase 2: Simular COM VISUALIZAÇÃO ---
    # A simulação agora é controlada pela função que inclui o loop Pygame
    tempo_final, log_batalhas, energias_finais, status_simulacao = simular_caminho_e_lutas_com_visualizacao(
        caminho_coords, mapa_aereo # Passa o caminho e o objeto mapa (que contém a tela e os sprites)
    )

    # --- Resultados Finais (após a visualização fechar) ---
    print("\n" + "="*40)
    print("--- RESULTADO FINAL DA SIMULAÇÃO ---")
    print("="*40)
    print(f"Status da Simulação: {status_simulacao}")
    print(f"Tempo Total Gasto: {tempo_final:.2f} minutos")

    print("\nLog das Batalhas Realizadas:")
    if not log_batalhas:
        print("  Nenhuma batalha realizada.")
    else:
        # Itera sobre o log [(casa_idx, nomes, tempo, energias_depois)]
        for casa_idx, nomes, tempo, _ in log_batalhas:
            # Obtém o nome da casa a partir do índice (0-11) e da lista ordenada (casas 2-13)
            nome_casa = mapa_aereo.cavaleiros_ouro_info[casa_idx]['nome']
            print(f"  - Casa {casa_idx+2} ({nome_casa}): Equipe: [{', '.join(nomes)}], Tempo Batalha: {tempo:.1f} min")

    print("\nEnergias Finais dos Cavaleiros de Bronze:")
    nomes_bronze = [cb['nome'] for cb in CAVALEIROS_BRONZE_INFO]
    print(f"  {list(zip(nomes_bronze, energias_finais))}")

    # Avaliação final da missão
    tempo_limite = 720 # 12 horas * 60 minutos
    if status_simulacao == "Sucesso":
        if tempo_final <= tempo_limite:
            print(f"\n--> SUCESSO! Atena foi salva a tempo! (Tempo Total: {tempo_final:.2f} min <= {tempo_limite} min)")
        else:
            print(f"\n--> FALHA! O tempo limite ({tempo_limite} min) foi excedido! (Tempo Total: {tempo_final:.2f} min)")
    elif status_simulacao == "Visualização Interrompida":
         print(f"\n--> SIMULAÇÃO INTERROMPIDA PELO USUÁRIO.")
    else:
        # Outros status de falha (Todos morreram, Falha na casa X, Erro no caminho)
        print(f"\n--> FALHA NA MISSÃO! Motivo: {status_simulacao}")

    print("\nExecução concluída.")

# Garante que a função main() só é chamada quando o script é executado diretamente
if __name__ == '__main__':
    main()