import pygame
import csv
import sys
import os
import heapq
import random


# --- Constantes (CORES AJUSTADAS) ---
PRETO = (0, 0, 0)
DELAY_MOVIMENTO = 50 # MUDE AQUI A VELOCIDADE DE MOVIMENTO ENZO INSETO
BRANCO = (255, 255, 255)
# Valores do CSV mapeados para Cor e Custo
TERRENOS_INFO = {
    # Valor: {'cor': (R,G,B), 'custo': TEMPO, 'nome': 'Nome'}
    15: {'cor': (202, 202, 202), 'custo': 1,   'nome': 'Plano'},        # Cinza Médio
    16: {'cor': (178, 156, 156), 'custo': 5,   'nome': 'Rochoso'},      # Cinza Claro
    14: {'cor': (105, 105, 105), 'custo': 200, 'nome': 'Montanhoso'},   # Cinza Escuro
}
COR_CASAS = (65, 105, 225)   # Azul
COR_INICIO = (0, 255, 0)      # Verde
COR_FIM = (255, 0, 0)        # Vermelho
TAMANHO_BLOCO = 15
NOME_ARQUIVO_MAPA = 'coordernadasmapaco.csv'
VALOR_PONTO_INICIAL = 0
VALOR_PONTO_FINAL = 13
CAMINHO_SPRITE = '.' # <<< AJUSTE SE NECESSÁRIO PARAO CAMINHOS DAS SPRITES
# -------------------------------------

# --- Informações Cavaleiros (SEM ALTERAÇÕES) ---
CAVALEIROS_BRONZE_INFO = [
    {'nome': 'Seiya',  'poder': 1.5, 'energia_inicial': 5, 'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Bronze/Saint Seya Chara - 0001.png'},
    {'nome': 'Shiryu', 'poder': 1.4, 'energia_inicial': 5, 'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Bronze/Saint Seya Chara - 0002.png'},
    {'nome': 'Hyoga',  'poder': 1.3, 'energia_inicial': 5, 'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Bronze/Saint Seya Chara - 0003.png'},
    {'nome': 'Shun',   'poder': 1.2, 'energia_inicial': 5, 'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Bronze/Saint Seya Chara - 0004.png'},
    {'nome': 'Ikki',   'poder': 1.1, 'energia_inicial': 5, 'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Bronze/Saint Seya Chara - 0005.png'},
]
NUM_CAVALEIROS_BRONZE = len(CAVALEIROS_BRONZE_INFO)

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
], key=lambda c: c['casa'])
NUM_CASAS = len(CAVALEIROS_OURO_INFO)

TREMY_INFO = {
    'nome': 'Sagitta Tremy',
    'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Prata/Athena_Sagita.png'
}
# ---------------------------------------------

# --- Funções Auxiliares ---
def calcular_distancia_manhattan(p1, p2):
    if p1 is None or p2 is None: return float('inf')
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# --- Classe Player (COLE O CÓDIGO COMPLETO DA CLASSE PLAYER DA RESPOSTA ANTERIOR AQUI) ---
class Player(pygame.sprite.Sprite):
    def __init__(self, x_mapa, y_mapa, sprite_sheet_path, nome="?", poder=0.0, dificuldade=0, energia_inicial=5):
        super().__init__()
        self.nome = nome
        self.poder_cosmico = poder
        self.dificuldade = dificuldade # Usado para Cavaleiros de Ouro
        self.sprites = {'down': [], 'left': [], 'right': [], 'up': []}
        self.direcao = 'down'
        self.indice_frame = 0

        # Posição lógica inicial no mapa (grid)
        self.map_x = x_mapa
        self.map_y = y_mapa

        # Rect inicial (será ajustado após carregar sprite)
        self.rect = pygame.Rect(x_mapa * TAMANHO_BLOCO, y_mapa * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.image.fill((200, 200, 200, 100)) # Fallback

        self._load_sprites(sprite_sheet_path)

        # Ajusta rect e imagem inicial se o carregamento funcionou
        if self.sprites.get(self.direcao) and self.sprites[self.direcao]:
            self.image = self.sprites[self.direcao][0] # Pega o primeiro frame
            frame_rect = self.image.get_rect()
            # Centraliza o rect do sprite no bloco do mapa
            self.rect = frame_rect.copy()
            self.rect.center = ((x_mapa * TAMANHO_BLOCO) + TAMANHO_BLOCO // 2,
                                (y_mapa * TAMANHO_BLOCO) + TAMANHO_BLOCO // 2)

        self.energia = energia_inicial # Usado para Cavaleiros de Bronze
        self.tempo_ultima_animacao = pygame.time.get_ticks()
        self.delay_animacao = 150

        # Offset para visualização (para não sobrepor)
        # Gera offset uma vez para cada instância
        self.offset_x = random.randint(-TAMANHO_BLOCO // 4, TAMANHO_BLOCO // 4)
        self.offset_y = random.randint(-TAMANHO_BLOCO // 4, TAMANHO_BLOCO // 4)


    def _load_sprites(self, sprite_sheet_path):
        # --- INICIO _load_sprites ---
        if not os.path.exists(sprite_sheet_path):
             # print(f"Erro: Arquivo de sprite não encontrado para {self.nome} em '{sprite_sheet_path}'")
             self._set_fallback_sprites()
             return
        try: sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        except pygame.error as e:
            print(f"Erro ao carregar imagem para {self.nome}: {e}")
            self._set_fallback_sprites()
            return

        sheet_width, sheet_height = sheet.get_size()
        num_frames_por_linha = 4
        num_linhas_direcao = 4
        sprite_width = sheet_width // num_frames_por_linha
        sprite_height = sheet_height // num_linhas_direcao

        if sprite_width <= 0 or sprite_height <= 0:
            # print(f"Aviso: Dimensões inválidas da sheet para {self.nome}. Tentando carregar como imagem única.")
            try:
                sprite = pygame.image.load(sprite_sheet_path).convert_alpha()
                escala = min(TAMANHO_BLOCO / sprite.get_width(), TAMANHO_BLOCO / sprite.get_height()) if sprite.get_width() > 0 and sprite.get_height() > 0 else 1
                novo_w = max(1, int(sprite.get_width() * escala))
                novo_h = max(1, int(sprite.get_height() * escala))
                sprite = pygame.transform.smoothscale(sprite, (novo_w, novo_h))

                for direcao in ['down', 'left', 'right', 'up']:
                    self.sprites[direcao] = [sprite]
                self.image = sprite
                return
            except Exception as e_load:
                print(f"Falha ao carregar como imagem única: {e_load}")
                self._set_fallback_sprites()
                return

        direcoes_na_sheet = ['down', 'left', 'right', 'up']
        for i, direcao in enumerate(direcoes_na_sheet):
            self.sprites[direcao] = []
            for j in range(num_frames_por_linha):
                rect = pygame.Rect(j * sprite_width, i * sprite_height, sprite_width, sprite_height)
                if sheet.get_rect().contains(rect):
                    try:
                        sub_image = sheet.subsurface(rect)
                        escala = min(TAMANHO_BLOCO / sub_image.get_width(), TAMANHO_BLOCO / sub_image.get_height()) if sub_image.get_width() > 0 and sub_image.get_height() > 0 else 1
                        novo_w = max(1, int(sub_image.get_width() * escala))
                        novo_h = max(1, int(sub_image.get_height() * escala))
                        scaled_sprite = pygame.transform.smoothscale(sub_image, (novo_w, novo_h))
                        self.sprites[direcao].append(scaled_sprite)
                    except ValueError as e:
                         # print(f"Erro no subsurface para {self.nome} frame ({j},{i}): {e}")
                         self.sprites[direcao].append(self._create_fallback_sprite((255,165,0,150)))
                else:
                    pass

            if not self.sprites[direcao]:
                self.sprites[direcao] = [self._create_fallback_sprite()]
        # --- FIM _load_sprites ---


    def _create_fallback_sprite(self, color=(200, 200, 200, 150)):
        sprite = pygame.Surface((TAMANHO_BLOCO, TAMANHO_BLOCO), pygame.SRCALPHA)
        sprite.fill(color)
        pygame.draw.rect(sprite, PRETO, sprite.get_rect(), 1)
        return sprite

    def _set_fallback_sprites(self):
        fallback = self._create_fallback_sprite()
        for direction in ['down', 'left', 'right', 'up']:
            self.sprites[direction] = [fallback]
        self.image = fallback
        self.direcao = 'down'

    def update(self): # Atualiza apenas a animação do frame
        if not self.sprites.get(self.direcao) or not self.sprites[self.direcao] or len(self.sprites[self.direcao]) <= 1:
            if self.sprites.get(self.direcao) and self.sprites[self.direcao]:
                 self.image = self.sprites[self.direcao][0]
            return

        agora = pygame.time.get_ticks()
        if agora - self.tempo_ultima_animacao > self.delay_animacao:
            self.tempo_ultima_animacao = agora
            sprite_list = self.sprites[self.direcao]
            self.indice_frame = (self.indice_frame + 1) % len(sprite_list)
            self.image = sprite_list[self.indice_frame]

    def set_visual_position(self, map_x, map_y):
        self.map_x = map_x
        self.map_y = map_y
        centro_x_bloco = (map_x * TAMANHO_BLOCO) + TAMANHO_BLOCO // 2
        centro_y_bloco = (map_y * TAMANHO_BLOCO) + TAMANHO_BLOCO // 2
        self.rect.center = (centro_x_bloco + self.offset_x, centro_y_bloco + self.offset_y)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
# --- FIM DA CLASSE PLAYER ---

# --- Classe Luta (Estática - SEM ALTERAÇÕES) ---
class Luta:
    @staticmethod
    def calcular_tempo_batalha(dificuldade_casa, equipe_indices, cavaleiros_bronze_info):
        soma_poder_cosmico = 0.0
        if not equipe_indices: return float('inf')
        for indice in equipe_indices:
            if 0 <= indice < len(cavaleiros_bronze_info):
                 soma_poder_cosmico += cavaleiros_bronze_info[indice]['poder']
            else:
                 return float('inf')
        if soma_poder_cosmico <= 0: return float('inf')
        return dificuldade_casa / soma_poder_cosmico
# --- FIM DA CLASSE LUTA ---

# --- Classe MapaAereo ---
class MapaAereo:
    def __init__(self, nome_arquivo_mapa, cav_bronze_data, cav_ouro_data, tremy_data):
        self.nome_arquivo = nome_arquivo_mapa
        self.mapa = self._carregar_mapa()
        if not self.mapa: sys.exit("Erro: Mapa não pôde ser carregado.")

        self.largura_mapa = len(self.mapa[0])
        self.altura_mapa = len(self.mapa)
        self.largura_tela = self.largura_mapa * TAMANHO_BLOCO
        self.altura_tela = self.altura_mapa * TAMANHO_BLOCO

        pygame.init()
        pygame.font.init()
        try:
            self.tela = pygame.display.set_mode((self.largura_tela, self.altura_tela))
            pygame.display.set_caption('Santuário - IA (Simulação)')
        except pygame.error as e:
             print(f"ERRO FATAL ao criar tela Pygame: {e}")
             sys.exit(1)
        self.clock = pygame.time.Clock()

        self.cavaleiros_bronze_info = cav_bronze_data
        self.cavaleiros_ouro_info = cav_ouro_data
        self.tremy_info = tremy_data

        self.posicao_inicial = self._encontrar_posicao_valor(VALOR_PONTO_INICIAL)
        self.posicao_final = self._encontrar_posicao_valor(VALOR_PONTO_FINAL)
        self.posicoes_casas_dict = self._encontrar_posicoes_casas()
        self.posicoes_casas_lista = self._mapear_posicoes_casas_para_lista()

        if self.posicao_inicial is None or self.posicao_final is None or None in self.posicoes_casas_lista:
             print("Erro Crítico: Posições essenciais não encontradas. Verifique CSV e valores.")
             pygame.quit()
             sys.exit(1)

        self.grupo_cavaleiros_ouro_fixos = pygame.sprite.Group()
        self.sprite_cavaleiro_prata_fixo = pygame.sprite.GroupSingle()
        self.grupo_cavaleiros_bronze_moveis = pygame.sprite.Group()
        self._inicializar_sprites_visuais()

        self.font = None
        try:
            self.font = pygame.font.SysFont(None, 20)
        except Exception as e:
            print(f"Erro ao carregar fonte: {e}.")


    # --- INICIO METODOS INTERNOS MapaAereo ---
    def _carregar_mapa(self):
         mapa_carregado = []
         primeira_linha_len = -1
         try:
             with open(self.nome_arquivo, 'r', newline='', encoding='utf-8') as arquivo:
                 leitor = csv.reader(arquivo)
                 for i, linha in enumerate(leitor):
                     # Remove apenas células completamente vazias (string vazia) do final
                     cleaned_line = list(linha)
                     while cleaned_line and not cleaned_line[-1]:
                          cleaned_line.pop()
                     if not cleaned_line: continue # Pula linha se ficou vazia

                     linha_int = []
                     for idx_col, valor_str in enumerate(cleaned_line):
                         valor_strip = valor_str.strip()
                         if not valor_strip: # Se célula ficou vazia após strip
                             linha_int.append(None) # Trata como None (pode ser obstáculo)
                             # print(f"Aviso Mapa: Célula vazia na linha {i+1} coluna {idx_col+1}.")
                             continue
                         try:
                             linha_int.append(int(valor_strip))
                         except ValueError:
                             # print(f"Aviso Mapa: Valor não inteiro '{valor_strip}' na linha {i+1} col {idx_col+1}. Tratando como None.")
                             linha_int.append(None) # Tratar como obstáculo ou valor padrão

                     if primeira_linha_len == -1:
                         primeira_linha_len = len(linha_int)
                     elif len(linha_int) != primeira_linha_len:
                         # print(f"Aviso Mapa: Linha {i+1} tem comprimento {len(linha_int)}, esperado {primeira_linha_len}. Ajustando...")
                         diff = primeira_linha_len - len(linha_int)
                         if diff > 0:
                             linha_int.extend([None] * diff)
                         else:
                             linha_int = linha_int[:primeira_linha_len]

                     mapa_carregado.append(linha_int)

             if not mapa_carregado or primeira_linha_len <= 0:
                 print("Erro: Mapa vazio ou inválido após carregar."); return None
             print(f"Mapa '{self.nome_arquivo}' carregado: {len(mapa_carregado)} linhas x {primeira_linha_len} colunas.")
             return mapa_carregado
         except FileNotFoundError: print(f"Erro: Arquivo '{self.nome_arquivo}' não encontrado."); return None
         except Exception as e: print(f"Erro inesperado ao carregar mapa: {e}"); return None

    def _obter_cor(self, valor):
         # Prioriza Inicio/Fim
         if valor == VALOR_PONTO_INICIAL: return COR_INICIO
         elif valor == VALOR_PONTO_FINAL: return COR_FIM
         # Depois Terrenos Mapeados
         info_terreno = TERRENOS_INFO.get(valor)
         if info_terreno: return info_terreno['cor']
         # Depois Casas
         elif isinstance(valor, int) and 1 <= valor <= 12: return COR_CASAS
         # Default
         else: return BRANCO # Para None ou qualquer outro valor

    def _obter_custo_terreno(self, x, y):
        if 0 <= y < self.altura_mapa and 0 <= x < self.largura_mapa:
            valor = self.mapa[y][x]
            info_terreno = TERRENOS_INFO.get(valor)
            if info_terreno:
                # DEBUG: Confirma custo alto
                # if info_terreno['custo'] == 200:
                #     print(f"DEBUG Custo: Montanhoso ({valor}) em ({x},{y}) -> Custo 200")
                return info_terreno['custo']
            elif valor is not None and (1 <= valor <= 12 or valor == VALOR_PONTO_INICIAL or valor == VALOR_PONTO_FINAL):
                return 1 # Custo 1 para casas, início, fim
            else:
                # Trata None e outros como obstáculo
                return float('inf')
        else:
            return float('inf') # Fora do mapa

    def _encontrar_posicao_valor(self, valor_procurado):
        for y, linha in enumerate(self.mapa):
            for x, valor_celula in enumerate(linha):
                if valor_celula == valor_procurado:
                    return x, y
        print(f"Aviso: Valor {valor_procurado} não encontrado no mapa.")
        return None

    def _encontrar_posicoes_casas(self):
        posicoes = {}
        for y, linha in enumerate(self.mapa):
            for x, valor in enumerate(linha):
                 if isinstance(valor, int) and 1 <= valor <= 12:
                    if valor not in posicoes:
                        posicoes[valor] = (x, y)
        casas_faltando = [i for i in range(2, 14) if i not in posicoes]
        if casas_faltando:
             print(f"Aviso: Números de casa não encontrados: {casas_faltando}")
        return posicoes

    def _mapear_posicoes_casas_para_lista(self):
        lista_pos = [None] * NUM_CASAS
        cav_ouro_ordenado = sorted(self.cavaleiros_ouro_info, key=lambda c: c['casa'])
        for i, cav_ouro in enumerate(cav_ouro_ordenado):
             casa_num = cav_ouro['casa']
             pos = self.posicoes_casas_dict.get(casa_num)
             if pos:
                 lista_pos[i] = pos
        return lista_pos
    # --- FIM METODOS INTERNOS MapaAereo ---

    def _inicializar_sprites_visuais(self):
        self.grupo_cavaleiros_ouro_fixos.empty()
        self.sprite_cavaleiro_prata_fixo.empty()
        self.grupo_cavaleiros_bronze_moveis.empty()

        # Ouro FIXOS
        for i, info in enumerate(self.cavaleiros_ouro_info):
            pos = self.posicoes_casas_lista[i]
            if pos:
                sprite = Player(pos[0], pos[1], info['sprite_path'], info['nome'], 0.0, info['dificuldade'])
                self.grupo_cavaleiros_ouro_fixos.add(sprite)

        # Prata FIXO
        if self.posicao_inicial and self.tremy_info:
             print('debug: Posição inicial encontrada:', self.posicao_inicial)
             sprite = Player(22, 38, self.tremy_info['sprite_path'], self.tremy_info['nome'])
             self.sprite_cavaleiro_prata_fixo.add(sprite)

        # Bronze MÓVEIS
        if self.posicao_inicial:
            start_x, start_y = self.posicao_inicial
            print('debug: Posição inicial encontrada:', self.posicao_inicial)
            for info in self.cavaleiros_bronze_info:
                sprite_anim = Player(start_x, start_y, info['sprite_path'], info['nome'])
                self.grupo_cavaleiros_bronze_moveis.add(sprite_anim)
        else:
             print("ERRO: Posição inicial não definida, não é possível criar sprites móveis.")


    def desenhar_estado_simulacao(self, texto_info_passo="", texto_info_batalha=""):
        try:
            self.tela.fill(PRETO)
            # Mapa
            for i, linha in enumerate(self.mapa):
                for j, valor in enumerate(linha):
                    x = j * TAMANHO_BLOCO; y = i * TAMANHO_BLOCO
                    cor = self._obter_cor(valor)
                    pygame.draw.rect(self.tela, cor, (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO))
                    pygame.draw.rect(self.tela, PRETO, (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO), 1)

            # Sprites Fixos
            self.grupo_cavaleiros_ouro_fixos.draw(self.tela)
            self.sprite_cavaleiro_prata_fixo.draw(self.tela)
            # Sprites Móveis
            self.grupo_cavaleiros_bronze_moveis.draw(self.tela)

            # Texto
            if self.font:
                y_offset = 5
                if texto_info_passo:
                    img_passo = self.font.render(texto_info_passo, True, BRANCO, PRETO)
                    self.tela.blit(img_passo, (5, y_offset)); y_offset += 20
                if texto_info_batalha:
                    img_perm = self.font.render(texto_info_batalha, True, BRANCO, PRETO)
                    self.tela.blit(img_perm, (5, y_offset))

            pygame.display.flip()
            # O clock.tick AGORA É CHAMADO DENTRO DA SIMULAÇÃO para controlar a velocidade geral
            # self.clock.tick(45) # Removido daqui
        except Exception as e:
            print(f"ERRO durante desenho: {e}")
            pygame.quit()
            sys.exit(1)

# --- FIM DA CLASSE MapaAereo ---


# --- Classe A* Simplificada (Fase 1: Caminho Físico) ---
class BuscaAEstrelaCaminho:
    def __init__(self, mapa_obj):
        self.mapa_obj = mapa_obj
        self.waypoints = []
        if mapa_obj.posicao_inicial: self.waypoints.append(mapa_obj.posicao_inicial)
        self.waypoints.extend([p for p in mapa_obj.posicoes_casas_lista if p is not None])
        if mapa_obj.posicao_final: self.waypoints.append(mapa_obj.posicao_final)
        if len(self.waypoints) < NUM_CASAS + 2:
             print(f"Erro A* Caminho: Waypoints insuficientes ({len(self.waypoints)}). Esperado {NUM_CASAS + 2}.")
             self.waypoints = None

    def buscar(self):
        if not self.waypoints: return None
        inicio = self.waypoints[0]
        num_waypoints = len(self.waypoints)
        objetivo_final = self.waypoints[-1] # O último waypoint é o objetivo final

        # Estado: ( (x,y), target_waypoint_index )
        estado_inicial = (inicio, 1) # Mira o primeiro waypoint após o início

        open_set = []
        h_inicial = self._calcular_heuristica_caminho(estado_inicial)
        # Fila: (f_cost, g_cost, estado) -> g_cost é o custo de TERRENO acumulado
        heapq.heappush(open_set, (h_inicial, 0.0, estado_inicial))

        # g_score armazena o menor custo de TERRENO para chegar a um estado
        g_score = {estado_inicial: 0.0}
        # came_from armazena o ESTADO anterior para reconstruir o caminho
        came_from = {estado_inicial: None}

        max_iter = 60000
        iter_count = 0

        while open_set and iter_count < max_iter:
            iter_count += 1
            f_atual, g_atual, estado_atual = heapq.heappop(open_set)

            if g_atual > g_score.get(estado_atual, float('inf')): continue

            pos_atual, target_idx = estado_atual

            # Chegou ao waypoint alvo? Avança o alvo.
            proximo_target_idx = target_idx
            waypoint_alvo_atual = self.waypoints[target_idx]

            if pos_atual == waypoint_alvo_atual:
                proximo_target_idx += 1

                # Chegou ao waypoint FINAL?
                if proximo_target_idx >= num_waypoints:
                    print(f"A* Caminho: Solução encontrada! Custo g (terreno): {g_atual:.1f} ({iter_count} iterações)")
                    return self._reconstruir_caminho_coords(came_from, estado_atual)

                # Atualiza o estado para mirar o próximo waypoint
                estado_novo_target = (pos_atual, proximo_target_idx)
                if g_atual < g_score.get(estado_novo_target, float('inf')):
                     g_score[estado_novo_target] = g_atual
                     came_from[estado_novo_target] = estado_atual # Veio do estado anterior para este novo target
                     h_novo = self._calcular_heuristica_caminho(estado_novo_target)
                     heapq.heappush(open_set, (g_atual + h_novo, g_atual, estado_novo_target))
                # Não expande vizinhos aqui, força a busca a partir da nova meta
                continue


            # Gerar Sucessores (Movimento)
            px, py = pos_atual
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = px + dx, py + dy
                # Usa a função do mapa para obter o custo do terreno
                custo_movimento = self.mapa_obj._obter_custo_terreno(nx, ny)

                # Verifica se é um movimento válido (não é obstáculo/fora do mapa)
                if custo_movimento != float('inf'):
                    nova_pos = (nx, ny)
                    # O estado sucessor continua mirando o MESMO target_idx
                    estado_sucessor = (nova_pos, target_idx)
                    novo_g = g_atual + custo_movimento # Acumula custo do terreno

                    # Se achou um caminho mais curto para este estado (pos, target)
                    if novo_g < g_score.get(estado_sucessor, float('inf')):
                        g_score[estado_sucessor] = novo_g
                        came_from[estado_sucessor] = estado_atual # Guarda estado anterior
                        h_novo = self._calcular_heuristica_caminho(estado_sucessor)
                        if h_novo != float('inf'): # Ignora se heurística for infinita
                           f_novo = novo_g + h_novo
                           heapq.heappush(open_set, (f_novo, novo_g, estado_sucessor))

        print(f"A* Caminho: Limite de {max_iter} iterações atingido ou falha.")
        return None


    def _calcular_heuristica_caminho(self, estado):
        pos_atual, target_idx = estado
        # Se target_idx está fora do range (já passou por todos), heurística é 0
        if target_idx >= len(self.waypoints): return 0
        target_pos = self.waypoints[target_idx]
        # Heurística simples: Distância de Manhattan (custo mínimo de movimento é 1)
        h = calcular_distancia_manhattan(pos_atual, target_pos)
        return h

    def _reconstruir_caminho_coords(self, came_from, estado_final):
         path_states = []
         curr_state = estado_final
         while curr_state is not None:
              path_states.append(curr_state)
              curr_state = came_from.get(curr_state)
         path_states.reverse()

         # Extrai apenas as coordenadas, evitando duplicatas consecutivas
         path_coords = []
         last_coord = None
         for state in path_states:
              pos, _ = state
              if pos != last_coord:
                   path_coords.append(pos)
                   last_coord = pos
         return path_coords

# --- FIM DA CLASSE BuscaAEstrelaCaminho ---


# --- Fase 2: Simulação e Escolha Greedy de Equipes ---

def escolher_equipe_greedy_final(casa_index, energias_atuais, cav_ouro_info, cav_bronze_info):
    """ Escolhe a equipe focando no menor tempo, mas limitando o tamanho da equipe. """
    from itertools import combinations
    if casa_index >= len(cav_ouro_info): return None, "Erro: Índice"

    dificuldade_casa = cav_ouro_info[casa_index]['dificuldade']
    # Lista de vivos: (indice, poder, energia)
    vivos = [(i, cb['poder'], energias_atuais[i]) for i, cb in enumerate(cav_bronze_info) if energias_atuais[i] > 0]
    if not vivos: return None, "Ninguém vivo"

    melhor_equipe_geral_indices = None
    menor_tempo_geral = float('inf')
    # --- AJUSTE AQUI: Limite o tamanho máximo da equipe ---
    max_tam_equipe_greedy = 2 # Ex: Não usar mais que 2 cavaleiros
    # -----------------------------------------------------

    # Avalia equipes de tamanho 1 até max_tam_equipe_greedy
    for tam in range(1, min(len(vivos), max_tam_equipe_greedy) + 1):
        melhor_equipe_tam = None
        menor_tempo_tam = float('inf')

        for combo_tuplas in combinations(vivos, tam):
            indices = [item[0] for item in combo_tuplas]
            poder_total = sum(item[1] for item in combo_tuplas)
            if poder_total > 0:
                tempo = dificuldade_casa / poder_total
                if tempo < menor_tempo_tam:
                    menor_tempo_tam = tempo
                    melhor_equipe_tam = indices

        # Compara com a melhor geral (entre os tamanhos já testados)
        if melhor_equipe_tam and menor_tempo_tam < menor_tempo_geral:
            menor_tempo_geral = menor_tempo_tam
            melhor_equipe_geral_indices = melhor_equipe_tam

    # Se nenhuma equipe até o tamanho limite funcionou, tenta usar todos os vivos
    if melhor_equipe_geral_indices is None:
        todos_indices = [item[0] for item in vivos]
        poder_todos = sum(item[1] for item in vivos)
        if poder_todos > 0:
            tempo_todos = dificuldade_casa / poder_todos
            # Considera usar todos APENAS se nenhuma outra equipe funcionou
            return todos_indices, f"Fallback: Todos (tempo {tempo_todos:.1f})"
        else:
            return None, "Nenhuma equipe vence" # Nem todos juntos

    # Retorna a melhor equipe encontrada dentro do limite de tamanho
    return melhor_equipe_geral_indices, f"Greedy Tam<= {max_tam_equipe_greedy} (tempo {menor_tempo_geral:.1f})"


def simular_caminho_e_lutas_com_visualizacao(caminho_coords, mapa_obj):
    if not caminho_coords or mapa_obj.posicao_inicial is None:
        print("Erro simulação: Caminho ou posição inicial inválidos.")
        return 0, [], [], "Erro inicial"

    tempo_total = 0.0
    energias_atuais = [cb['energia_inicial'] for cb in mapa_obj.cavaleiros_bronze_info]
    battle_log = []
    mapa_casas_coord_idx = {coord: idx for idx, coord in enumerate(mapa_obj.posicoes_casas_lista) if coord is not None}
    status_final = "Não iniciado"

    texto_info_passo = "Iniciando Simulação..."
    
    battle_info_display_time = 2500 # Aumenta tempo de exibição da info da batalha
    last_battle_info_time = -battle_info_display_time
    # --- AJUSTE AQUI: Velocidade da animação (maior = mais lento) ---
    # ms entre passos de movimento
    # --------------------------------------------------------------

    print("\n--- Iniciando Simulação com Visualização (Fase 2) ---")
    print(f"Energias Iniciais: {energias_atuais}")

    rodando_visualizacao = True
    passo_caminho_idx = 0

    while rodando_visualizacao and passo_caminho_idx < len(caminho_coords):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando_visualizacao = False
                status_final = "Visualização Interrompida"
                print(f"\n{status_final}")
                break
        if not rodando_visualizacao: break

        pos_atual_coord = caminho_coords[passo_caminho_idx]

        # Custo Viagem
        if passo_caminho_idx > 0:
             custo_viagem = mapa_obj._obter_custo_terreno(pos_atual_coord[0], pos_atual_coord[1])
             if custo_viagem == float('inf'):
                  print(f"Erro Simulação: Movimento inválido para {pos_atual_coord}.")
                  status_final = "Erro no caminho"; rodando_visualizacao = False; break
             tempo_total += custo_viagem
             texto_info_passo = f"Pos:{pos_atual_coord} T Viagem: +{custo_viagem:.0f} = {tempo_total:.1f} min"
        else:
             texto_info_passo = f"Pos:{pos_atual_coord} T Total: {tempo_total:.1f} min"

        # Atualiza Posição Visual Sprites
        for sprite_b in mapa_obj.grupo_cavaleiros_bronze_moveis:
            sprite_b.set_visual_position(pos_atual_coord[0], pos_atual_coord[1])
            if passo_caminho_idx + 1 < len(caminho_coords):
                 pos_next = caminho_coords[passo_caminho_idx+1]
                 dx = pos_next[0] - pos_atual_coord[0]; dy = pos_next[1] - pos_atual_coord[1]
                 if dx > 0:
                     sprite_b.direcao = 'right'
                 elif dx < 0:
                     sprite_b.direcao = 'left'
                 elif dy > 0:
                     sprite_b.direcao = 'down'
                 elif dy < 0:
                     sprite_b.direcao = 'up'

        # Lógica Batalha
        texto_info_batalha_atual = ""
        if pos_atual_coord in mapa_casas_coord_idx:
            casa_index = mapa_casas_coord_idx[pos_atual_coord]
            if not any(log[0] == casa_index for log in battle_log): # Luta só uma vez por casa
                nome_casa = mapa_obj.cavaleiros_ouro_info[casa_index]['nome']
                dificuldade_casa = mapa_obj.cavaleiros_ouro_info[casa_index]['dificuldade']
                print(f"\n-- Chegou na Casa {casa_index+1} ({nome_casa}) em {pos_atual_coord} | T:{tempo_total:.1f} --")
                print(f"Energias Atuais: {['{}:{}'.format(mapa_obj.cavaleiros_bronze_info[i]['nome'][0], energias_atuais[i]) for i in range(len(energias_atuais))]}")

                # ---> USA A NOVA FUNÇÃO GREEDY <---
                equipe_escolhida_indices, motivo = escolher_equipe_greedy_final(
                    casa_index, energias_atuais, mapa_obj.cavaleiros_ouro_info, mapa_obj.cavaleiros_bronze_info
                )

                if equipe_escolhida_indices is None:
                    print(f"FALHA NA SIMULAÇÃO: {motivo} para {nome_casa}."); texto_info_batalha_atual = f"FALHA! {motivo}!"
                    status_final = f"Falha-{nome_casa}"; rodando_visualizacao = False; break
                else:
                    tempo_batalha = Luta.calcular_tempo_batalha(dificuldade_casa, equipe_escolhida_indices, mapa_obj.cavaleiros_bronze_info)
                    tempo_total += tempo_batalha
                    equipe_nomes = []
                    for indice in equipe_escolhida_indices:
                        energias_atuais[indice] -= 1
                        equipe_nomes.append(mapa_obj.cavaleiros_bronze_info[indice]['nome'])
                    energias_depois_tupla = tuple(energias_atuais)
                    battle_log.append((casa_index, equipe_nomes, tempo_batalha, energias_depois_tupla))

                    texto_info_batalha_atual = f"Luta! {nome_casa}: [{', '.join(equipe_nomes)}] (T: {tempo_batalha:.1f})"
                    print(f"Luta Casa {nome_casa}: Equipe: {equipe_nomes} ({motivo}). Tempo Batalha: {tempo_batalha:.1f}. T Total: {tempo_total:.1f}")
                    print(f"Energias Após: {['{}:{}'.format(mapa_obj.cavaleiros_bronze_info[i]['nome'][0], energias_atuais[i]) for i in range(len(energias_atuais))]}")
                    last_battle_info_time = pygame.time.get_ticks()

                    if all(e <= 0 for e in energias_atuais):
                        print("FALHA: Todos morreram."); texto_info_batalha_atual += " - MORRERAM!"
                        status_final = "Todos morreram"; rodando_visualizacao = False; break

        # Desenho e Controle de Tempo
        agora = pygame.time.get_ticks()
        info_batalha_visivel = texto_info_batalha_atual
        if not info_batalha_visivel and (agora - last_battle_info_time < battle_info_display_time):
             if battle_log:
                  last_log = battle_log[-1]
                  nome_casa_log = mapa_obj.cavaleiros_ouro_info[last_log[0]]['nome']
                  info_batalha_visivel = f"Luta! {nome_casa_log}: [{', '.join(last_log[1])}] (T: {last_log[2]:.1f})"

        mapa_obj.grupo_cavaleiros_bronze_moveis.update()
        mapa_obj.grupo_cavaleiros_ouro_fixos.update()
        mapa_obj.sprite_cavaleiro_prata_fixo.update()
        mapa_obj.desenhar_estado_simulacao(texto_info_passo, info_batalha_visivel)

        # Pausa para velocidade da visualização
        mapa_obj.clock.tick(1000 // DELAY_MOVIMENTO) # Tenta manter FPS baseado no delay

        passo_caminho_idx += 1

    # Fim do Loop
    if rodando_visualizacao:
        status_final = "Sucesso"
        print("\n--- Simulação com Visualização Concluída ---")
        mapa_obj.desenhar_estado_simulacao("Caminho Concluído!", f"Tempo Final: {tempo_total:.1f}")
        pygame.time.wait(3000) # Espera 3 seg no final

    pygame.quit()
    return tempo_total, battle_log, energias_atuais, status_final
# --- FIM DA FASE 2 ---


# --- Ponto de Entrada Principal ---
def main():
    if not os.path.exists(NOME_ARQUIVO_MAPA):
        print(f"Erro Fatal: Mapa '{NOME_ARQUIVO_MAPA}' não encontrado."); sys.exit(1)

    print("Inicializando MapaAereo...")
    mapa_aereo = MapaAereo(NOME_ARQUIVO_MAPA,
                           CAVALEIROS_BRONZE_INFO,
                           CAVALEIROS_OURO_INFO,
                           TREMY_INFO)
    if mapa_aereo.posicao_inicial is None or mapa_aereo.posicao_final is None or None in mapa_aereo.posicoes_casas_lista:
         print("Erro Fatal: Posições essenciais não encontradas."); sys.exit(1) # Sai direto
    print("MapaAereo inicializado.")

    print("\n--- Fase 1: Buscando Caminho Físico (A*) ---")
    buscador_caminho = BuscaAEstrelaCaminho(mapa_aereo)
    caminho_coords = buscador_caminho.buscar()

    if not caminho_coords:
        print("Falha ao encontrar o caminho físico. Abortando."); sys.exit(1)
    print(f"Caminho físico encontrado com {len(caminho_coords)} passos.")

    # --- Fase 2: Simular COM VISUALIZAÇÃO ---
    tempo_final, log_batalhas, energias_finais, status_simulacao = simular_caminho_e_lutas_com_visualizacao(
        caminho_coords, mapa_aereo
    )

    # --- Resultados Finais (após visualização) ---
    print("\n--- RESULTADO FINAL (Abordagem 2 Fases) ---")
    print(f"Status da Simulação: {status_simulacao}")
    print(f"Tempo Total Gasto: {tempo_final:.2f} minutos")
    print("\nLog das Batalhas Realizadas:")
    if not log_batalhas:
        print("  Nenhuma batalha realizada.")
    else:
        for casa_idx, nomes, tempo, _ in log_batalhas:
            nome_casa = mapa_aereo.cavaleiros_ouro_info[casa_idx]['nome']
            print(f"  - Casa {casa_idx+1} ({nome_casa}): Equipe: [{', '.join(nomes)}], Tempo: {tempo:.1f}")
    print(f"\nEnergias Finais: {energias_finais}")

    if status_simulacao == "Sucesso":
        if tempo_final <= 720:
            print(f"\nSUCESSO! Atena foi salva a tempo! (Tempo: {tempo_final:.2f} min)")
        else:
            print(f"\nFALHA! O tempo limite (720 min) foi excedido! (Tempo: {tempo_final:.2f} min)")
    else:
        print(f"\nFALHA na missão: {status_simulacao}")

    print("\nExecução concluída.")

if __name__ == '__main__':
    main()