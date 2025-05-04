import pygame
import csv
import sys
import os
import math
import heapq # Fila de prioridade para o A*

# --- Constantes ---
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
COR_PLANO = (210, 180, 140)         # Valor 14
COR_ROCHOSO = (160, 160, 160)        # Valor 15
COR_MONTANHOSO = (105, 105, 105)     # Valor 16
COR_INICIO = (255, 0, 0)             # Vermelho (VALOR_PONTO_INICIAL = 0)
COR_FIM = (0, 255, 0)              # Verde (VALOR_PONTO_FIM = 1 - CONFIRME!)
COR_CASAS = (65, 105, 225)          # Valores 2-13
TAMANHO_BLOCO = 15 # Reduzido para caber mais na tela? Verifique se 15 ou 20 é melhor.
NOME_ARQUIVO_MAPA = 'coordernadasmapaco.csv' # Confirme o nome
VALOR_PONTO_INICIAL = 0 # Confirmado pelo usuário
VALOR_PONTO_FIM = 1     # <<< --- CONFIRME ESTE VALOR (cor verde no mapa)

# Base do caminho para os sprites (ajustado para Linux/Mac)
CAMINHO_SPRITE = '/home/alan-moraes/Downloads' # Use '/' como separador

# Custos de movimento (tempo em minutos)
# !!! CONFIRME OS CUSTOS PARA INICIO/FIM/CASAS - Assumindo 1 (Plano) !!!
CUSTOS_TERRENO = {
    VALOR_PONTO_FIM: 1,      # Fim (Assumindo Plano)
    VALOR_PONTO_INICIAL: 1,  # Início (Assumindo Plano)
    14: 1,                  # Plano
    15: 5,                  # Rochoso
    16: 200,                # Montanhoso
    # Adiciona custo para entrar nas casas (assumindo 1 min)
    **{i: 1 for i in range(2, 14)} # Casas 2 a 13
}
TERRENOS_INTRANSITAVEIS = [] # Adicione valores aqui se houver (ex: [-1] se usar -1 para parede)

# --- Informações dos Cavaleiros de Bronze ---
CAVALEIROS_BRONZE_INFO = [
    {'nome': 'Seiya',  'poder': 1.5, 'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Bronze/Saint Seya Chara - 0001.png'},
    {'nome': 'Shiryu', 'poder': 1.4, 'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Bronze/Saint Seya Chara - 0002.png'},
    {'nome': 'Hyoga',  'poder': 1.3, 'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Bronze/Saint Seya Chara - 0003.png'},
    {'nome': 'Shun',   'poder': 1.2, 'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Bronze/Saint Seya Chara - 0004.png'},
    {'nome': 'Ikki',   'poder': 1.1, 'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Bronze/Saint Seya Chara - 0005.png'},
]
# --- Informações dos Cavaleiros de Ouro ---
CAVALEIROS_OURO_INFO = [
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
    {'casa': 13, 'nome': 'Afrodite', 'dificuldade': 120, 'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Ouro/_Afrodite.png'},
]
# --- Informação do Cavaleiro de Prata ---
TREMY_INFO = {
    'nome': 'Sagitta Tremy',
    'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Prata/Athena_Sagita.png'
}

# --- Classe Luta (Modificada para A*) ---
class Luta:
    def __init__(self, cavaleiros_bronze_data):
        self.cavaleiros_base = {info['nome']: {'poder': info['poder'], 'energia': 5} for info in cavaleiros_bronze_data}

    def simular_batalha(self, dificuldade_casa, equipe_nomes, energia_atual_dict):
        soma_poder_cosmico = 0.0
        participantes_nomes_validos = []
        cavaleiros_mortos_nomes = []
        novo_estado_energia = energia_atual_dict.copy()

        for nome_cavaleiro in equipe_nomes:
            if nome_cavaleiro in self.cavaleiros_base:
                if novo_estado_energia.get(nome_cavaleiro, 0) > 0:
                    soma_poder_cosmico += self.cavaleiros_base[nome_cavaleiro]['poder']
                    participantes_nomes_validos.append(nome_cavaleiro)

        if not participantes_nomes_validos or soma_poder_cosmico <= 0:
            return float('inf'), novo_estado_energia, []

        tempo_gasto = dificuldade_casa / soma_poder_cosmico

        for nome_participante in participantes_nomes_validos:
            novo_estado_energia[nome_participante] -= 1
            if novo_estado_energia[nome_participante] <= 0:
                cavaleiros_mortos_nomes.append(nome_participante)

        return tempo_gasto, novo_estado_energia, cavaleiros_mortos_nomes

    def get_nomes_cavaleiros_vivos(self, energia_dict):
        return [nome for nome, energia in energia_dict.items() if energia > 0]

# --- Classe Player (Apenas para Visualização) ---
class Player(pygame.sprite.Sprite):
    def __init__(self, x_mapa, y_mapa, sprite_sheet_path, nome="?"): # Removido poder/dificuldade
        super().__init__()
        self.nome = nome
        self.sprites = {'down': [], 'left': [], 'right': [], 'up': []}
        self.direcao = 'down'
        self.indice_frame = 0
        self.rect = pygame.Rect(x_mapa * TAMANHO_BLOCO, y_mapa * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA); self.image.fill((200, 200, 200, 100))
        self._load_sprites(sprite_sheet_path)
        if self.sprites.get(self.direcao):
            self.image = self.sprites[self.direcao][self.indice_frame]
            frame_rect = self.image.get_rect(); self.rect = frame_rect.copy()
            self.rect.topleft = (x_mapa * TAMANHO_BLOCO, y_mapa * TAMANHO_BLOCO)
        self.tempo_ultima_animacao = pygame.time.get_ticks()
        self.delay_animacao = 150

    def _load_sprites(self, sprite_sheet_path):
       # ... (código _load_sprites como na resposta anterior) ...
        if not os.path.exists(sprite_sheet_path):
             print(f"Erro: Arquivo de sprite não encontrado para {self.nome} em '{sprite_sheet_path}'")
             self._set_fallback_sprites(); return
        try: sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        except pygame.error as e:
            print(f"Erro ao carregar imagem para {self.nome}: {e}")
            self._set_fallback_sprites(); return
        sheet_width, sheet_height = sheet.get_size()
        num_frames_por_linha = 4 ; num_linhas_direcao = 4 # Assumindo 4x4
        sprite_width = sheet_width // num_frames_por_linha ; sprite_height = sheet_height // num_linhas_direcao
        if sprite_width <= 0 or sprite_height <= 0:
            print(f"Erro: Dimensões inválidas da sheet para {self.nome} ({sheet_width}x{sheet_height}).")
            self._set_fallback_sprites(); return
        direcoes_na_sheet = ['down', 'left', 'right', 'up']
        for i, direcao in enumerate(direcoes_na_sheet):
            self.sprites[direcao] = []
            for j in range(num_frames_por_linha):
                rect = pygame.Rect(j * sprite_width, i * sprite_height, sprite_width, sprite_height)
                if sheet.get_rect().contains(rect):
                    try:
                        sprite = sheet.subsurface(rect)
                        sprite = pygame.transform.scale(sprite, (TAMANHO_BLOCO, TAMANHO_BLOCO))
                        self.sprites[direcao].append(sprite)
                    except ValueError as e:
                         print(f"Erro subsurface {self.nome} ({j},{i}): {e}")
                         self.sprites[direcao].append(self._create_fallback_sprite((255,165,0,150)))
                else:
                    print(f"Aviso: Frame ({j},{i}) fora limites sheet {self.nome}.")
                    self.sprites[direcao].append(self._create_fallback_sprite((255,0,0,150)))
        for direcao in direcoes_na_sheet:
             if not self.sprites.get(direcao):
                  print(f"Aviso crítico: Falha direção '{direcao}' para {self.nome}.")
                  self.sprites[direcao] = [self._create_fallback_sprite()] * num_frames_por_linha

    def _create_fallback_sprite(self, color=(200, 200, 200, 150)):
       # ... (código _create_fallback_sprite como antes) ...
        sprite = pygame.Surface((TAMANHO_BLOCO, TAMANHO_BLOCO), pygame.SRCALPHA)
        sprite.fill(color) ; pygame.draw.rect(sprite, PRETO, sprite.get_rect(), 1)
        return sprite

    def _set_fallback_sprites(self):
       # ... (código _set_fallback_sprites como antes) ...
        fallback = self._create_fallback_sprite()
        for direction in self.sprites.keys(): self.sprites[direction] = [fallback] * 4
        if self.direcao in self.sprites: self.image = self.sprites[self.direcao][0]
        else: self.image = fallback

    def update(self):
       # ... (código update como antes) ...
        if not self.sprites.get(self.direcao) or len(self.sprites[self.direcao]) <= 1:
            if self.sprites.get(self.direcao): self.image = self.sprites[self.direcao][0]
            return
        agora = pygame.time.get_ticks()
        if agora - self.tempo_ultima_animacao > self.delay_animacao:
            self.tempo_ultima_animacao = agora
            sprite_list = self.sprites.get(self.direcao, [])
            if sprite_list:
                 self.indice_frame = (self.indice_frame + 1) % len(sprite_list)
                 self.image = sprite_list[self.indice_frame]

    def set_posicao(self, x_mapa, y_mapa):
         self.rect.topleft = (x_mapa * TAMANHO_BLOCO, y_mapa * TAMANHO_BLOCO)

    def set_direcao(self, direcao):
         if direcao in self.sprites:
             if self.direcao != direcao:
                 self.direcao = direcao
                 self.indice_frame = 0
                 if self.sprites[self.direcao]:
                     self.image = self.sprites[self.direcao][self.indice_frame]

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

# --- Classe AStar ---
class AStar:
    def __init__(self, mapa_obj, luta_obj, cavaleiros_bronze_data, cavaleiros_ouro_data):
        self.mapa = mapa_obj.mapa
        self.mapa_largura = mapa_obj.largura_mapa
        self.mapa_altura = mapa_obj.altura_mapa
        self.luta = luta_obj
        self.cavaleiros_bronze_data = cavaleiros_bronze_data
        self.cavaleiros_ouro_map = {info['casa']: info for info in cavaleiros_ouro_data}

        self.pos_inicial = mapa_obj._encontrar_posicao_valor(VALOR_PONTO_INICIAL)
        self.pos_final = mapa_obj._encontrar_posicao_valor(VALOR_PONTO_FIM)

        if not self.pos_inicial or not self.pos_final:
            raise ValueError("Erro: Posição inicial ou final não encontrada no mapa.")

        self.todas_casas = set(range(2, 14))

    # Dentro da classe AStar:
    def heuristica(self, pos_atual, casas_visitadas):
        """Estima o custo restante. Heurística: Dist. Manhattan * Custo Mínimo Mov."""
        (x, y) = pos_atual
        (gx, gy) = self.pos_final
        dist_manhattan = abs(x - gx) + abs(y - gy)
        custo_minimo_mov = 1 # Custo do terreno 'Plano'
        return dist_manhattan * custo_minimo_mov # Heurística admissível simples # Pode superestimar se a equipe real for mais fraca que a média




# Nova função auxiliar para calcular energia final (para o relatório)
    def recalcular_energia_final(self, batalhas_resultado):
     energia_final = {cb['nome']: 5 for cb in self.cavaleiros_bronze_data}
     for batalha in batalhas_resultado:
         for nome_cavaleiro in batalha['equipe']:
             if nome_cavaleiro in energia_final:
                 energia_final[nome_cavaleiro] -= 1
                 # Garante que não fique negativo no relatório
                 if energia_final[nome_cavaleiro] < 0: energia_final[nome_cavaleiro] = 0
     return energia_final

    def get_vizinhos(self, estado_atual):
        # ... (Cole aqui o código completo de get_vizinhos da resposta anterior) ...
        vizinhos = []
        (x, y), energia_tupla, casas_visitadas_fs = estado_atual
        energia_dict = dict(zip([cb['nome'] for cb in self.cavaleiros_bronze_data], energia_tupla))

        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Cima, Baixo, Esq, Dir
            nx, ny = x + dx, y + dy

            if not (0 <= nx < self.mapa_largura and 0 <= ny < self.mapa_altura): continue # Fora do mapa

            tipo_terreno_vizinho = self.mapa[ny][nx]
            if tipo_terreno_vizinho in TERRENOS_INTRANSITAVEIS: continue # Parede, etc.

            custo_movimento = CUSTOS_TERRENO.get(tipo_terreno_vizinho)
            if custo_movimento is None: continue # Terreno desconhecido/inválido

            pos_vizinho = (nx, ny)
            energia_vizinho_dict = energia_dict.copy() # Copia para possível modificação na batalha
            casas_vizinho_fs = casas_visitadas_fs
            custo_batalha = 0.0
            mortos_batalha = []
            equipe_usada_nomes = []
            num_casa_lutada = None

            if 2 <= tipo_terreno_vizinho <= 13 and tipo_terreno_vizinho not in casas_visitadas_fs:
                num_casa = tipo_terreno_vizinho
                num_casa_lutada = num_casa # Guarda para info_extra
                if num_casa in self.cavaleiros_ouro_map:
                    dificuldade_casa = self.cavaleiros_ouro_map[num_casa]['dificuldade']
                    equipe_usada_nomes = self.luta.get_nomes_cavaleiros_vivos(energia_vizinho_dict) # Estratégia: todos vivos

                    if not equipe_usada_nomes:
                        custo_batalha = float('inf')
                    else:
                        tempo_b, energia_apos_batalha, mortos_batalha = self.luta.simular_batalha(
                            dificuldade_casa, equipe_usada_nomes, energia_vizinho_dict
                        )
                        # Verifica se a batalha foi possível (tempo finito)
                        if tempo_b == float('inf'):
                            custo_batalha = float('inf') # Marca transição como impossível
                        else:
                            custo_batalha = tempo_b
                            energia_vizinho_dict = energia_apos_batalha # Atualiza energia SÓ para este vizinho
                            casas_vizinho_fs = casas_visitadas_fs.union({num_casa})
                else:
                    print(f"Aviso: Casa {num_casa} mapa sem dados Ouro.")
                    casas_vizinho_fs = casas_visitadas_fs.union({num_casa}) # Visita mesmo sem lutar?

            custo_total_transicao = custo_movimento + custo_batalha

            # Verifica se a transição é possível (custo finito)
            if custo_total_transicao != float('inf'):
                energia_vizinho_tupla = tuple(energia_vizinho_dict.get(cb['nome'], 0) for cb in self.cavaleiros_bronze_data)
                estado_vizinho = (pos_vizinho, energia_vizinho_tupla, casas_vizinho_fs)
                info_extra = {
                    'custo_mov': custo_movimento,
                    'casa_lutada': num_casa_lutada,
                    'equipe_usada': equipe_usada_nomes if num_casa_lutada else [], # Guarda equipe só se lutou
                    'custo_bat': custo_batalha,
                    'mortos_nesta_batalha': mortos_batalha
                }
                vizinhos.append((estado_vizinho, custo_total_transicao, info_extra))

        return vizinhos


    def buscar(self):
        
        print("\nIniciando busca A*...")
        # ... (código inicial de buscar: estado_inicial, fila_aberta, etc.) ...
        estado_inicial_energia = tuple(5 for _ in self.cavaleiros_bronze_data)
        estado_inicial_casas = frozenset()
        estado_inicial = (self.pos_inicial, estado_inicial_energia, estado_inicial_casas)

        fila_aberta = [(self.heuristica(self.pos_inicial, estado_inicial_casas), 0, estado_inicial, [self.pos_inicial], [])]
        heapq.heapify(fila_aberta)
        custo_g = {estado_inicial: 0}
        veio_de = {estado_inicial: None}
        # detalhes_transicao_map = {} # Removido se não for usar para reconstruir detalhes

        conjunto_fechado = set()
        nos_explorados = 0
        MAX_NOS_EXPLORADOS = 1000000 # <<< --- LIMITE ADICIONADO (Ajuste se necessário)

        while fila_aberta:
            nos_explorados += 1
            # Adiciona um log mais frequente ou só quando atinge limite
            if nos_explorados % 50000 == 0:
                print(f"Nós explorados: {nos_explorados}, Fila aberta: {len(fila_aberta)}")

            # Verifica limite
            if nos_explorados > MAX_NOS_EXPLORADOS:
                print(f"\n!!! Limite de {MAX_NOS_EXPLORADOS} nós explorados atingido! Busca interrompida. !!!")
                return None, float('inf'), [] # Falha por limite

            # ... (resto do loop while: heapq.heappop, checagem conjunto_fechado) ...
            f_cost_atual, g_cost_atual, estado_atual, caminho_atual, batalhas_atuais = heapq.heappop(fila_aberta)

            if estado_atual in conjunto_fechado: continue
            conjunto_fechado.add(estado_atual)

            pos_atual, _, casas_visitadas_fs = estado_atual

            # ... (código da checagem do objetivo) ...
            if pos_atual == self.pos_final and casas_visitadas_fs == self.todas_casas:
                print(f"\nObjetivo alcançado! Nós explorados: {nos_explorados}")
                # Recalcula energia final baseada nas batalhas do caminho encontrado
                energia_final_calculada = self.recalcular_energia_final(batalhas_atuais)
                # Você pode querer retornar ou usar energia_final_calculada
                return caminho_atual, g_cost_atual, batalhas_atuais

            # ... (código da geração de vizinhos e adição na fila) ...
            for estado_vizinho, custo_transicao, info_extra in self.get_vizinhos(estado_atual):
                if estado_vizinho in conjunto_fechado: continue

                novo_custo_g = g_cost_atual + custo_transicao

                if estado_vizinho not in custo_g or novo_custo_g < custo_g[estado_vizinho]:
                    custo_g[estado_vizinho] = novo_custo_g
                    pos_vizinho, _, casas_visitadas_vizinho = estado_vizinho
                    custo_h = self.heuristica(pos_vizinho, casas_visitadas_vizinho)
                    custo_f = novo_custo_g + custo_h

                    novo_caminho = caminho_atual + [pos_vizinho]
                    novas_batalhas = batalhas_atuais[:]
                    if info_extra.get('casa_lutada') is not None:
                        novas_batalhas.append({
                            'casa': info_extra['casa_lutada'],
                            'equipe': info_extra['equipe_usada'],
                            'tempo': info_extra['custo_bat'],
                            'mortos': info_extra['mortos_nesta_batalha']
                        })

                    heapq.heappush(fila_aberta, (custo_f, novo_custo_g, estado_vizinho, novo_caminho, novas_batalhas))
                    veio_de[estado_vizinho] = estado_atual


        print(f"\nBusca A* falhou após explorar {nos_explorados} nós. Fila vazia.")
        return None, float('inf'), [] # Falha
    # --- Classe MapaAereo (Modificada para usar A*) ---

class MapaAereo:
    def __init__(self, nome_arquivo_mapa, cav_bronze_data, cav_ouro_data, tremy_data):
        self.nome_arquivo = nome_arquivo_mapa
        self.mapa = self._carregar_mapa()
        if not self.mapa: sys.exit("Erro: Mapa não pôde ser carregado.")
        self.largura_mapa = len(self.mapa[0]) ; self.altura_mapa = len(self.mapa)
        self.largura_tela = self.largura_mapa * TAMANHO_BLOCO
        self.altura_tela = self.altura_mapa * TAMANHO_BLOCO

        pygame.init()
        self.tela = pygame.display.set_mode((self.largura_tela, self.altura_tela))
        pygame.display.set_caption('Santuário - A* Pathfinding')
        self.clock = pygame.time.Clock()
        try:
            self.font = pygame.font.SysFont(None, 20) # Fonte menor
        except pygame.error:
             self.font = pygame.font.Font(None, 20) # Fallback font


        # Sprites (apenas para visualização)
        self.cavaleiros_bronze_sprites = [] ; self.grupo_cb = pygame.sprite.Group()
        self.cavaleiros_ouro_sprites = [] ; self.grupo_co = pygame.sprite.Group()
        self.cavaleiro_prata_sprite = None ; self.grupo_cp = pygame.sprite.GroupSingle()

        # Instância da Luta
        self.gerenciador_lutas = Luta(cav_bronze_data)

        # Inicializa Sprites Visuais
        self._inicializar_sprites_visuais(cav_bronze_data, cav_ouro_data, tremy_data)

        # --- Executa A* ---
        self.astar = AStar(self, self.gerenciador_lutas, cav_bronze_data, cav_ouro_data)
        self.caminho_otimo, self.custo_otimo, self.batalhas_resultado = self.astar.buscar()

        # Visualização
        self.indice_passo_atual = 0
        self.tempo_ultimo_passo = pygame.time.get_ticks()
        self.delay_passo_vis = 150 # Mais rápido

        self._imprimir_resultados()


    def _carregar_mapa(self):
        # ... (código _carregar_mapa como antes) ...
         mapa_carregado = []
         try:
             with open(self.nome_arquivo, 'r', newline='') as arquivo:
                 leitor = csv.reader(arquivo)
                 primeira_linha_len = -1 ; problemas_linha = False
                 for i, linha in enumerate(leitor):
                     linha_int = [] ; linha_contem_algo = any(v.strip() for v in linha)
                     if not linha_contem_algo: continue
                     for valor in linha:
                         valor_strip = valor.strip()
                         if valor_strip:
                             try: linha_int.append(int(valor_strip))
                             except ValueError: print(f"Erro: Valor não numérico '{valor}' linha {i+1}."); problemas_linha = True ; break
                     if problemas_linha: continue
                     if not linha_int and linha_contem_algo: print(f"Aviso: Linha {i+1} inválida."); continue
                     if linha_int:
                         if primeira_linha_len == -1: primeira_linha_len = len(linha_int)
                         elif len(linha_int) != primeira_linha_len: print(f"Erro: Linha {i+1} comp {len(linha_int)}, esperado {primeira_linha_len}."); return None
                         mapa_carregado.append(linha_int)
             if not mapa_carregado: print("Erro: Mapa vazio ou inválido."); return None
             print(f"Mapa '{self.nome_arquivo}' carregado: {len(mapa_carregado)} linhas x {primeira_linha_len} colunas.")
             return mapa_carregado
         except FileNotFoundError: print(f"Erro: Arquivo '{self.nome_arquivo}' não encontrado."); return None
         except Exception as e: print(f"Erro inesperado ao carregar mapa: {e}"); return None

    def _obter_cor(self, valor):
        # ... (código _obter_cor como antes) ...
         if valor == 14: return COR_PLANO
         elif valor == 15: return COR_ROCHOSO
         elif valor == 16: return COR_MONTANHOSO
         elif valor == VALOR_PONTO_INICIAL: return COR_INICIO
         elif valor == VALOR_PONTO_FIM: return COR_FIM
         elif 2 <= valor <= 13: return COR_CASAS
         else: return BRANCO # Para outros valores (ex: paredes se houverem com outro numero)

    def _encontrar_posicao_valor(self, valor_procurado):
        # ... (código _encontrar_posicao_valor como antes) ...
        for y, linha in enumerate(self.mapa):
            for x, valor in enumerate(linha):
                if valor == valor_procurado: return x, y
        print(f"Aviso: Valor {valor_procurado} não encontrado no mapa.") # Adiciona aviso
        return None

    def _encontrar_posicoes_casas(self):
        # ... (código _encontrar_posicoes_casas como antes) ...
        posicoes = {}
        for y, linha in enumerate(self.mapa):
            for x, valor in enumerate(linha):
                if 2 <= valor <= 13:
                    if valor not in posicoes: posicoes[valor] = (x, y)
        return posicoes

    def _inicializar_sprites_visuais(self, cav_bronze_data, cav_ouro_data, tremy_data):
        print("Inicializando sprites para visualização...")
        # Bronze
        pos_inicial_b = self._encontrar_posicao_valor(VALOR_PONTO_INICIAL)
        if pos_inicial_b:
            start_x, start_y = pos_inicial_b
            for info in cav_bronze_data:
                sprite = Player(start_x, start_y, info['sprite_path'], info['nome'])
                self.cavaleiros_bronze_sprites.append(sprite)
                self.grupo_cb.add(sprite)
        else: print("Erro: Posição inicial não encontrada para sprites Bronze.")

        # Ouro
        pos_casas = self._encontrar_posicoes_casas()
        for info in cav_ouro_data:
             if info['casa'] in pos_casas:
                  pos_x, pos_y = pos_casas[info['casa']]
                  sprite = Player(pos_x, pos_y, info['sprite_path'], info['nome'])
                  self.cavaleiros_ouro_sprites.append(sprite)
                  self.grupo_co.add(sprite)
             else: print(f"Aviso: Posição não encontrada para sprite Ouro Casa {info['casa']}")

        # Prata
        pos_inicial_p = self._encontrar_posicao_valor(VALOR_PONTO_INICIAL)
        if pos_inicial_p:
             start_x, start_y = pos_inicial_p
             self.cavaleiro_prata_sprite = Player(start_x, start_y, tremy_data['sprite_path'], tremy_data['nome'])
             self.grupo_cp.add(self.cavaleiro_prata_sprite)
        else: print("Erro: Posição inicial não encontrada para sprite Prata.")


    def _imprimir_resultados(self):
         """Imprime os resultados da busca A* no console."""
         print("\n--- RESULTADOS DA BUSCA A* ---")
         if self.caminho_otimo:
             # ... (impressão do caminho e custo como antes) ...
             print(f"Caminho Encontrado ({len(self.caminho_otimo)} passos).")
             if len(self.caminho_otimo) <= 30: print(f"  {self.caminho_otimo}")
             else: print(f"  {self.caminho_otimo[:10]} ... {self.caminho_otimo[-10:]}")
             print(f"\nCusto Total (Tempo): {self.custo_otimo:.2f} minutos")

             print("\nResumo das Batalhas:")
             if self.batalhas_resultado:
                 for i, batalha in enumerate(self.batalhas_resultado):
                     # ... (código para imprimir detalhes da batalha como antes) ...
                     nome_ouro = "Desconhecido"
                     for co_info in CAVALEIROS_OURO_INFO:
                         if co_info['casa'] == batalha['casa']: nome_ouro = co_info['nome']; break
                     print(f"  Batalha {i+1} - Casa {batalha['casa']} ({nome_ouro}):")
                     print(f"    Equipe: {batalha['equipe']}")
                     print(f"    Tempo: {batalha['tempo']:.2f} min")
                     if batalha['mortos']: print(f"    Mortos: {batalha['mortos']}")

                 # --- Calcula e imprime energia final CORRETAMENTE ---
                 energia_final_dict = self.astar.recalcular_energia_final(self.batalhas_resultado)
                 print("\nEnergia Final dos Cavaleiros de Bronze:")
                 # Mantém a ordem original da lista INFO para impressão
                 for nome_cb in [cb['nome'] for cb in CAVALEIROS_BRONZE_INFO]:
                     energia = energia_final_dict.get(nome_cb, 5) # Pega do resultado ou 5 default
                     print(f"  - {nome_cb}: {energia if energia > 0 else 'Morto'}")
                 # ---------------------------------------------------

             else:
                 print("  Nenhuma batalha realizada.")

         else:
             print("Não foi encontrado um caminho válido para o objetivo.")
             # Imprime a energia inicial se a busca falhou
             print("\nEnergia Inicial dos Cavaleiros de Bronze:")
             for cb_info in CAVALEIROS_BRONZE_INFO:
                  print(f"  - {cb_info['nome']}: 5")

         print("-------------------------------")


    def desenhar(self):
        self.tela.fill(PRETO)
        # Mapa e Caminho
        for i, linha in enumerate(self.mapa):
            for j, valor in enumerate(linha):
                x = j * TAMANHO_BLOCO; y = i * TAMANHO_BLOCO
                cor = self._obter_cor(valor)
                pygame.draw.rect(self.tela, cor, (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO))
                if self.caminho_otimo and (j, i) in self.caminho_otimo:
                     # Desenha indicação do caminho (mais sutil)
                     overlay = pygame.Surface((TAMANHO_BLOCO, TAMANHO_BLOCO), pygame.SRCALPHA)
                     overlay.fill((255, 255, 0, 70)) # Amarelo semi-transparente
                     self.tela.blit(overlay, (x,y))
                pygame.draw.rect(self.tela, PRETO, (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO), 1)

        # Cavaleiros Ouro e Prata (fixos)
        self.grupo_co.draw(self.tela)
        self.grupo_cp.draw(self.tela)

        # Cavaleiros Bronze (movendo na visualização)
        if self.caminho_otimo and self.indice_passo_atual < len(self.caminho_otimo):
            pos_x, pos_y = self.caminho_otimo[self.indice_passo_atual]
            direcao_movimento = 'down' # Padrão
            if self.indice_passo_atual + 1 < len(self.caminho_otimo):
                prox_x, prox_y = self.caminho_otimo[self.indice_passo_atual + 1]
                dx = prox_x - pos_x; dy = prox_y - pos_y
                if dx > 0: direcao_movimento = 'right'
                elif dx < 0: direcao_movimento = 'left'
                elif dy > 0: direcao_movimento = 'down'
                elif dy < 0: direcao_movimento = 'up'

            for sprite_cb in self.grupo_cb:
                 sprite_cb.set_direcao(direcao_movimento)
                 sprite_cb.set_posicao(pos_x, pos_y)
            self.grupo_cb.draw(self.tela)
        else: # Se não há caminho ou acabou, desenha parados na origem/fim?
             # Desenha no início para consistência se não houver caminho
             pos_inicial_vis = self._encontrar_posicao_valor(VALOR_PONTO_INICIAL)
             if pos_inicial_vis:
                 start_x, start_y = pos_inicial_vis
                 for sprite_cb in self.grupo_cb:
                     sprite_cb.set_posicao(start_x, start_y)
             self.grupo_cb.draw(self.tela) # Desenha grupo mesmo se parado

        # Mostra Custo e Passo Atual na Tela
        if self.custo_otimo != float('inf'):
             texto_custo = self.font.render(f"Custo: {self.custo_otimo:.1f} min", True, BRANCO, PRETO)
             self.tela.blit(texto_custo, (5, 5))
             if self.caminho_otimo:
                 texto_passo = self.font.render(f"Passo: {self.indice_passo_atual+1}/{len(self.caminho_otimo)}", True, BRANCO, PRETO)
                 self.tela.blit(texto_passo, (5, 25))
        else:
             texto_falha = self.font.render("Caminho nao encontrado", True, BRANCO, PRETO)
             self.tela.blit(texto_falha, (5, 5))


    def run(self):
        """Executa o loop de VISUALIZAÇÃO do caminho A*."""
        if not self.caminho_otimo:
            print("Nenhum caminho para visualizar.")
            self.desenhar() # Desenha estado inicial
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            return

        rodando = True
        self.indice_passo_atual = 0
        self.tempo_ultimo_passo = pygame.time.get_ticks()

        while rodando:
            agora = pygame.time.get_ticks()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT: rodando = False

            if agora - self.tempo_ultimo_passo > self.delay_passo_vis:
                if self.indice_passo_atual < len(self.caminho_otimo) - 1:
                    self.indice_passo_atual += 1
                self.tempo_ultimo_passo = agora

            # Atualiza animação dos sprites parados ou movendo
            self.grupo_cb.update()
            self.grupo_co.update()
            self.grupo_cp.update()

            self.desenhar() # Desenha o estado atual da visualização
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

# --- Ponto de Entrada Principal ---
def main():
    print("Verificando arquivos...")
    arquivos_ok = True
    if not os.path.exists(NOME_ARQUIVO_MAPA): print(f"Erro: Mapa não encontrado {NOME_ARQUIVO_MAPA}"); arquivos_ok = False
    # Verifica todos os sprites
    for info in CAVALEIROS_BRONZE_INFO + CAVALEIROS_OURO_INFO + [TREMY_INFO]:
        if not os.path.exists(info['sprite_path']):
            print(f"Erro: Sprite não encontrado '{info['sprite_path']}' para {info['nome']}")
            arquivos_ok = False
    if not arquivos_ok: sys.exit(1)
    print("Arquivos verificados.")

    mapa_aereo = MapaAereo(NOME_ARQUIVO_MAPA,
                           CAVALEIROS_BRONZE_INFO,
                           CAVALEIROS_OURO_INFO,
                           TREMY_INFO)

    if mapa_aereo.mapa:
        mapa_aereo.run() # Executa A* na inicialização e depois visualiza
    else:
        print("Falha ao inicializar MapaAereo.")
        pygame.quit()
        sys.exit(1)

if __name__ == '__main__':
    main()