import pygame
import csv
import sys
import os
# import time # Não estritamente necessário se update não usar dt

# --- Constantes ---
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
COR_PLANO = (210, 180, 140)
COR_ROCHOSO = (160, 160, 160)
COR_MONTANHOSO = (105, 105, 105)
COR_INICIO = (0, 255, 0)      # Verde (Assumido como Valor = 1 no CSV)
COR_FIM = (255, 0, 0)        # Vermelho (Assumido como Valor = 0 no CSV)
COR_CASAS = (65, 105, 225)   # Azul
TAMANHO_BLOCO = 15
NOME_ARQUIVO_MAPA = 'coordernadasmapaco.csv' # Confirme o nome
VALOR_PONTO_INICIAL = 0 
CAMINHO_SPRITE = r'/home/alan-moraes/Downloads/'
# --- Informações dos Cavaleiros de Bronze ---
# Caminhos atualizados conforme sua última informação
CAVALEIROS_BRONZE_INFO = [
    {'nome': 'Seiya',  'poder': 1.5, 'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Bronze/Saint Seya Chara - 0001.png'},
    {'nome': 'Shiryu', 'poder': 1.4, 'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Bronze/Saint Seya Chara - 0002.png'},
    {'nome': 'Hyoga',  'poder': 1.3, 'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Bronze/Saint Seya Chara - 0003.png'},
    {'nome': 'Shun',   'poder': 1.2, 'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Bronze/Saint Seya Chara - 0004.png'},
    # Verifique se Ikki é 0005.png ou Ikki de Fênix.png
    {'nome': 'Ikki',   'poder': 1.1, 'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Bronze/Saint Seya Chara - 0005.png'},
]
# ----------------------------------------------------------

# --- Informações dos Cavaleiros de Ouro ---
# !!! VERIFIQUE SE OS CAMINHOS ESTÃO CORRETOS !!!
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
# ----------------------------------------------------------

# --- Informação do Cavaleiro de Prata ---
TREMY_INFO = {
    'nome': 'Sagitta Tremy',
    'sprite_path': f'{CAMINHO_SPRITE}/Saint Seiya/Cavaleiros de Prata/Athena_Sagita.png'
}
# ----------------------------------------------------------

# --- Classe para Gerenciar Lutas ---
class Luta:
    def __init__(self, cavaleiros_bronze_lista):
        """
        Inicializa o gerenciador de lutas.
        Args:
            cavaleiros_bronze_lista (list): Uma lista das instâncias Player dos cav. de bronze.
        """
        # Guarda uma referência à lista original de instâncias dos cavaleiros de bronze
        # Assim, as alterações de energia feitas aqui refletirão nos objetos originais
        self.cavaleiros_bronze = cavaleiros_bronze_lista
        # Poderia criar uma cópia se não quisesse alterar os originais diretamente,
        # mas para a simulação do algoritmo, alterar os originais é geralmente o desejado.

    def simular_batalha(self, dificuldade_casa, equipe_nomes):
        """
        Simula uma batalha contra um Cavaleiro de Ouro.

        Args:
            dificuldade_casa (int): O nível de dificuldade da casa (do Cav. Ouro).
            equipe_nomes (list): Uma lista de strings com os nomes dos Cav. Bronze
                                  selecionados para esta batalha (ex: ['Seiya', 'Ikki']).

        Returns:
            tuple: (tempo_gasto, cavaleiros_mortos_nomes)
                   tempo_gasto (float): O tempo calculado para a batalha (pode ser float('inf')).
                   cavaleiros_mortos_nomes (list): Lista de nomes dos cavaleiros que morreram (energia <= 0) nesta batalha.
                   Retorna (float('inf'), []) se nenhum cavaleiro válido puder lutar.
        """
        soma_poder_cosmico = 0.0
        participantes_validos = []
        cavaleiros_mortos_nomes = []

        print(f"/n--- Simulando Batalha (Dificuldade: {dificuldade_casa}) ---")
        print(f"Equipe Selecionada: {equipe_nomes}")

        # Verifica energia e calcula soma de poder dos participantes válidos
        for nome_cavaleiro in equipe_nomes:
            cavaleiro_encontrado = None
            for cb in self.cavaleiros_bronze:
                if cb.nome == nome_cavaleiro:
                    cavaleiro_encontrado = cb
                    break

            if cavaleiro_encontrado:
                if cavaleiro_encontrado.energia > 0:
                    soma_poder_cosmico += cavaleiro_encontrado.poder_cosmico
                    participantes_validos.append(cavaleiro_encontrado)
                    print(f"  - {nome_cavaleiro}: Participando (Energia: {cavaleiro_encontrado.energia}, Poder: {cavaleiro_encontrado.poder_cosmico})")
                else:
                    print(f"  - {nome_cavaleiro}: Não pode participar (Energia: {cavaleiro_encontrado.energia} <= 0)")
            else:
                print(f"  - Aviso: Cavaleiro '{nome_cavaleiro}' não encontrado na lista.")

        # Calcula o tempo
        if not participantes_validos or soma_poder_cosmico <= 0:
            print("Resultado: Nenhum participante válido ou poder total zero. Batalha impossível/infinita.")
            return float('inf'), [] # Tempo infinito se ninguém puder lutar

        tempo_gasto = dificuldade_casa / soma_poder_cosmico
        print(f"Poder Cósmico Total da Equipe: {soma_poder_cosmico:.2f}")
        print(f"Tempo Gasto Calculado: {tempo_gasto:.2f} minutos")

        # Deduz energia e verifica mortes
        for participante in participantes_validos:
            participante.energia -= 1
            print(f"  - {participante.nome}: Energia restante = {participante.energia}")
            if participante.energia <= 0:
                print(f"  >>> {participante.nome} gastou toda a energia e não pode mais lutar! <<<")
                cavaleiros_mortos_nomes.append(participante.nome)

        print("----------------------------------------------")
        return tempo_gasto, cavaleiros_mortos_nomes

    def get_energia_cavaleiros(self):
        """Retorna um dicionário com a energia atual de cada cavaleiro de bronze."""
        return {cb.nome: cb.energia for cb in self.cavaleiros_bronze}

    def reset_energia_cavaleiros(self, energia_inicial=5):
        """Reseta a energia de todos os cavaleiros de bronze para o valor inicial."""
        print(f"/n--- Resetando Energia para {energia_inicial} ---")
        for cb in self.cavaleiros_bronze:
            cb.energia = energia_inicial
        print("Energia resetada.")



# --- Classe Player (Reutilizada para todos os cavaleiros) ---
class Player(pygame.sprite.Sprite):
    def __init__(self, x_mapa, y_mapa, sprite_sheet_path, nome="?", poder=0.0, dificuldade=0):
        super().__init__()
        self.nome = nome
        self.poder_cosmico = poder
        self.dificuldade = dificuldade
        self.sprites = {'down': [], 'left': [], 'right': [], 'up': []}
        self.direcao = 'down' # Padrão para baixo
        self.indice_frame = 0

        # Define o rect inicial ANTES de carregar sprites
        self.rect = pygame.Rect(x_mapa * TAMANHO_BLOCO, y_mapa * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO)
        # Cria uma imagem fallback inicial que será substituída se o load funcionar
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.image.fill((200, 200, 200, 100)) # Fallback padrão

        self._load_sprites(sprite_sheet_path)

        # Tenta definir a imagem inicial correta APÓS _load_sprites
        if self.sprites.get(self.direcao): # Usa .get() para segurança
            self.image = self.sprites[self.direcao][self.indice_frame]
            # Atualiza o rect para o tamanho real do frame carregado
            frame_rect = self.image.get_rect()
            # Mantém o topleft na posição do mapa, mas usa o tamanho do sprite
            self.rect = frame_rect.copy()
            self.rect.topleft = (x_mapa * TAMANHO_BLOCO, y_mapa * TAMANHO_BLOCO)
        # else: self.image continua sendo o fallback criado acima


        self.energia = 5
        self.tempo_ultima_animacao = pygame.time.get_ticks()
        self.delay_animacao = 150

    def _load_sprites(self, sprite_sheet_path):
        # ... (código _load_sprites da resposta anterior, com verificações) ...
        if not os.path.exists(sprite_sheet_path):
             print(f"Erro: Arquivo de sprite não encontrado para {self.nome} em '{sprite_sheet_path}'")
             self._set_fallback_sprites()
             return
        try: sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        except pygame.error as e:
            print(f"Erro ao carregar imagem para {self.nome}: {e}")
            self._set_fallback_sprites()
            return

        sheet_width, sheet_height = sheet.get_size()
        num_frames_por_linha = 4 ; num_linhas_direcao = 4 # Assumindo 4x4
        sprite_width = sheet_width // num_frames_por_linha
        sprite_height = sheet_height // num_linhas_direcao

        if sprite_width <= 0 or sprite_height <= 0:
            print(f"Erro: Dimensões inválidas da sheet para {self.nome} ({sheet_width}x{sheet_height}).")
            self._set_fallback_sprites()
            return

        direcoes_na_sheet = ['down', 'left', 'right', 'up']
        for i, direcao in enumerate(direcoes_na_sheet):
            self.sprites[direcao] = [] # Limpa a lista para esta direção
            for j in range(num_frames_por_linha):
                rect = pygame.Rect(j * sprite_width, i * sprite_height, sprite_width, sprite_height)
                if sheet.get_rect().contains(rect):
                    try:
                        sprite = sheet.subsurface(rect)
                        sprite = pygame.transform.scale(sprite, (TAMANHO_BLOCO, TAMANHO_BLOCO))
                        self.sprites[direcao].append(sprite)
                    except ValueError as e: # Erro no subsurface
                         print(f"Erro no subsurface para {self.nome} frame ({j},{i}): {e}")
                         self.sprites[direcao].append(self._create_fallback_sprite((255,165,0,150))) # Laranja fallback
                else:
                    print(f"Aviso: Frame ({j},{i}) fora dos limites da sheet para {self.nome}.")
                    self.sprites[direcao].append(self._create_fallback_sprite((255,0,0,150))) # Vermelho fallback

        # Garante que mesmo após o loop, haja sprites
        for direcao in direcoes_na_sheet:
             if not self.sprites.get(direcao): # Se a lista não existe ou está vazia
                  print(f"Aviso crítico: Falha completa ao carregar direção '{direcao}' para {self.nome}.")
                  self.sprites[direcao] = [self._create_fallback_sprite()] * num_frames_por_linha


    def _create_fallback_sprite(self, color=(200, 200, 200, 150)):
        """Cria um sprite de fallback visual."""
        sprite = pygame.Surface((TAMANHO_BLOCO, TAMANHO_BLOCO), pygame.SRCALPHA)
        sprite.fill(color)
        pygame.draw.rect(sprite, PRETO, sprite.get_rect(), 1) # Borda
        return sprite

    def _set_fallback_sprites(self):
        """Define sprites de fallback para todas as direções."""
        fallback = self._create_fallback_sprite()
        for direction in self.sprites.keys():
            self.sprites[direction] = [fallback] * 4 # Assume 4 frames
        # Define a imagem atual também, caso a direção inicial falhe
        if self.direcao in self.sprites:
            self.image = self.sprites[self.direcao][0]
        else: # Se até a direção inicial for inválida (improvável)
            self.image = fallback


    def update(self):
        # ... (código update sem alterações) ...
        if not self.sprites.get(self.direcao) or len(self.sprites[self.direcao]) <= 1:
            if self.sprites.get(self.direcao): self.image = self.sprites[self.direcao][0]
            return

        agora = pygame.time.get_ticks()
        if agora - self.tempo_ultima_animacao > self.delay_animacao:
            self.tempo_ultima_animacao = agora
            # Acessa com get para segurança, embora a verificação acima deva cobrir
            sprite_list = self.sprites.get(self.direcao, [])
            if sprite_list: # Procede somente se a lista existir
                 self.indice_frame = (self.indice_frame + 1) % len(sprite_list)
                 self.image = sprite_list[self.indice_frame]
            # else: mantém a imagem atual (que seria fallback ou o último frame válido)


    def move(self, dx, dy, mapa_obj):
         # ... (movimento manual desativado) ...
         pass

    def draw(self, surface):
        # ... (código draw sem alterações) ...
        surface.blit(self.image, self.rect.topleft)


# --- Classe MapaAereo (Modificada) ---
class MapaAereo:
    def __init__(self, nome_arquivo_mapa, cav_bronze_data, cav_ouro_data, tremy_data): # Adicionado tremy_data
        self.nome_arquivo = nome_arquivo_mapa
        self.mapa = self._carregar_mapa()
        if not self.mapa: sys.exit("Erro: Mapa não pôde ser carregado.")

        self.largura_mapa = len(self.mapa[0])
        self.altura_mapa = len(self.mapa)
        self.largura_tela = self.largura_mapa * TAMANHO_BLOCO
        self.altura_tela = self.altura_mapa * TAMANHO_BLOCO

        pygame.init()
        self.tela = pygame.display.set_mode((self.largura_tela, self.altura_tela))
        pygame.display.set_caption('Santuário - IA')
        self.clock = pygame.time.Clock()

        # Grupos de Sprites
        self.cavaleiros_bronze = []
        self.grupo_cavaleiros_bronze = pygame.sprite.Group()
        self.cavaleiros_ouro = []
        self.grupo_cavaleiros_ouro = pygame.sprite.Group()
        self.cavaleiro_prata = None # Instância única
        self.grupo_cavaleiro_prata = pygame.sprite.GroupSingle() # Grupo para Tremy

        # Inicializações
        self._inicializar_cavaleiros_bronze(cav_bronze_data)
        self._inicializar_cavaleiros_ouro(cav_ouro_data)
        self._inicializar_cavaleiro_prata(tremy_data) # Inicializa Tremy
        if self.cavaleiros_bronze: # Só cria se houver cavaleiros de bronze
             self.gerenciador_lutas = Luta(self.cavaleiros_bronze)
             print("Gerenciador de Lutas inicializado.")
        else:
             self.gerenciador_lutas = None
             print("Aviso: Gerenciador de Lutas não criado (nenhum cavaleiro de bronze).")
    def _carregar_mapa(self):
        # ... (código _carregar_mapa sem alterações) ...
         mapa_carregado = []
         try:
             with open(self.nome_arquivo, 'r', newline='') as arquivo:
                 leitor = csv.reader(arquivo)
                 primeira_linha_len = -1 ; problemas_linha = False
                 for i, linha in enumerate(leitor):
                     linha_int = [] ; linha_contem_algo = any(v.strip() for v in linha)
                     if not linha_contem_algo: continue # Pula linhas totalmente vazias
                     for valor in linha:
                         valor_strip = valor.strip()
                         if valor_strip:
                             try: linha_int.append(int(valor_strip))
                             except ValueError:
                                 print(f"Erro: Valor não numérico '{valor}' linha {i+1}.")
                                 problemas_linha = True ; break # Para de processar esta linha
                     if problemas_linha: continue # Pula para a próxima linha do CSV
                     if not linha_int and linha_contem_algo:
                         print(f"Aviso: Linha {i+1} inválida (não numérica ou mal formatada).")
                         continue
                     if linha_int:
                         if primeira_linha_len == -1: primeira_linha_len = len(linha_int)
                         elif len(linha_int) != primeira_linha_len:
                             print(f"Erro: Linha {i+1} comprimento {len(linha_int)}, esperado {primeira_linha_len}.")
                             return None
                         mapa_carregado.append(linha_int)
             if not mapa_carregado: print("Erro: Mapa vazio ou inválido."); return None
             print(f"Mapa '{self.nome_arquivo}' carregado: {len(mapa_carregado)} linhas x {primeira_linha_len} colunas.")
             return mapa_carregado
         except FileNotFoundError: print(f"Erro: Arquivo '{self.nome_arquivo}' não encontrado."); return None
         except Exception as e: print(f"Erro inesperado ao carregar mapa: {e}"); return None

    def _obter_cor(self, valor):
        # ... (código _obter_cor sem alterações) ...
         # !!! CONFIRME OS VALORES PARA INICIO/FIM !!!
         if valor == 14: return COR_PLANO
         elif valor == 15: return COR_ROCHOSO
         elif valor == 16: return COR_MONTANHOSO
         elif valor == 1: return COR_INICIO # Assumindo 1 = Início (Verde)
         elif valor == 0: return COR_FIM    # Assumindo 0 = Fim (Vermelho)
         elif 2 <= valor <= 13: return COR_CASAS
         else: return BRANCO

    def _encontrar_posicao_valor(self, valor_procurado):
        # ... (código _encontrar_posicao_valor sem alterações) ...
        for y, linha in enumerate(self.mapa):
            for x, valor in enumerate(linha):
                if valor == valor_procurado:
                    return x, y
        return None

    def _encontrar_posicoes_casas(self):
        # ... (código _encontrar_posicoes_casas sem alterações) ...
        posicoes = {}
        for y, linha in enumerate(self.mapa):
            for x, valor in enumerate(linha):
                if 2 <= valor <= 13:
                    if valor not in posicoes: posicoes[valor] = (x, y)
        return posicoes

    def _inicializar_cavaleiros_bronze(self, cavaleiros_data):
        # --- CONFIRME O VALOR DO PONTO INICIAL (Ex: 1 para COR_INICIO Verde) ---
       # <<< AJUSTE AQUI SE NECESSÁRIO
        # --------------------------------------------------------------------
        pos_inicial = self._encontrar_posicao_valor(VALOR_PONTO_INICIAL)
        if pos_inicial is None:
            print(f"Erro Crítico: Posição inicial (valor {VALOR_PONTO_INICIAL}) não encontrada! Cav. Bronze não criados.")
            return
        start_x, start_y = pos_inicial
        print(f"Inicializando Cavaleiros de Bronze em (col={start_x}, lin={start_y})")

        for info in cavaleiros_data:
            # A verificação de existência do path é feita dentro de Player agora
            cavaleiro = Player(start_x, start_y, info['sprite_path'], info['nome'], info['poder'])
            self.cavaleiros_bronze.append(cavaleiro)
            self.grupo_cavaleiros_bronze.add(cavaleiro)
            # Não precisa imprimir sucesso aqui, Player já imprime
        if not self.cavaleiros_bronze: print("Aviso: Nenhum Cavaleiro de Bronze inicializado.")


    def _inicializar_cavaleiros_ouro(self, cavaleiros_data):
        # ... (código _inicializar_cavaleiros_ouro sem alterações) ...
        posicoes_casas = self._encontrar_posicoes_casas()
        if not posicoes_casas: print("Aviso: Nenhuma posição de Casa (2-13) encontrada."); return

        print("Inicializando Cavaleiros de Ouro...")
        for info in cavaleiros_data:
            casa_num = info['casa']
            if casa_num in posicoes_casas:
                pos_x, pos_y = posicoes_casas[casa_num]
                cavaleiro = Player(pos_x, pos_y, info['sprite_path'], info['nome'], 0.0, info['dificuldade'])
                self.cavaleiros_ouro.append(cavaleiro)
                self.grupo_cavaleiros_ouro.add(cavaleiro)
            else: print(f"Aviso: Posição Casa {casa_num} ({info['nome']}) não encontrada.")
        if not self.cavaleiros_ouro: print("Aviso: Nenhum Cavaleiro de Ouro inicializado.")

    # Novo método para inicializar Tremy
    def _inicializar_cavaleiro_prata(self, tremy_data):
        """Cria a instância do cavaleiro de prata na posição inicial."""
        # --- CONFIRME O VALOR DO PONTO INICIAL (Mesmo dos Bronze) ---
        VALOR_PONTO_INICIAL = 1 # <<< AJUSTE AQUI SE NECESSÁRIO
        # -----------------------------------------------------------
        pos_inicial = self._encontrar_posicao_valor(VALOR_PONTO_INICIAL)
        if pos_inicial is None:
            print("Erro Crítico: Posição inicial não encontrada! Tremy não criado.")
            return
        start_x, start_y = pos_inicial
        print(f"Inicializando Cavaleiro de Prata em (col={start_x}, lin={start_y})")

        # Cria a instância de Tremy (reutilizando Player)
        self.cavaleiro_prata = Player(start_x, start_y, tremy_data['sprite_path'], tremy_data['nome'])
        # Adiciona ao grupo single (GroupSingle só pode ter um sprite)
        self.grupo_cavaleiro_prata.add(self.cavaleiro_prata)


    def desenhar(self):
        """Desenha o mapa e todos os cavaleiros na tela."""
        self.tela.fill(PRETO)
        # Mapa
        for i, linha in enumerate(self.mapa):
            for j, valor in enumerate(linha):
                x = j * TAMANHO_BLOCO; y = i * TAMANHO_BLOCO
                cor = self._obter_cor(valor)
                pygame.draw.rect(self.tela, cor, (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO))
                pygame.draw.rect(self.tela, PRETO, (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO), 1)

        # Cavaleiros (Ordem de desenho importa para sobreposição)
        self.grupo_cavaleiros_ouro.draw(self.tela)  # Ouro primeiro (mais ao fundo)
        self.grupo_cavaleiro_prata.draw(self.tela) # Prata
        self.grupo_cavaleiros_bronze.draw(self.tela) # Bronze por cima de todos


    def run(self):
        """Executa o loop principal do Pygame."""
        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False

            # Atualiza todos os grupos de sprites
            self.grupo_cavaleiros_bronze.update()
            self.grupo_cavaleiros_ouro.update()
            self.grupo_cavaleiro_prata.update() # Atualiza Tremy (para animação)

            # Desenha tudo
            self.desenhar()

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

# --- Ponto de Entrada Principal ---
def main():
    # Verifica arquivos essenciais
    if not os.path.exists(NOME_ARQUIVO_MAPA): print(f"Erro: Mapa não encontrado {NOME_ARQUIVO_MAPA}"); sys.exit(1)
    # Verifica se pelo menos um sprite de cada grupo existe (exemplo)
    if not os.path.exists(CAVALEIROS_BRONZE_INFO[0]['sprite_path']): print(f"Erro: Sprite Seiya não encontrado."); sys.exit(1)
    if not os.path.exists(CAVALEIROS_OURO_INFO[0]['sprite_path']): print(f"Erro: Sprite Mu não encontrado."); sys.exit(1)
    if not os.path.exists(TREMY_INFO['sprite_path']): print(f"Erro: Sprite Tremy não encontrado."); sys.exit(1)


    # Cria a instância do MapaAereo, passando todas as informações
    mapa_aereo = MapaAereo(NOME_ARQUIVO_MAPA,
                           CAVALEIROS_BRONZE_INFO,
                           CAVALEIROS_OURO_INFO,
                           TREMY_INFO) # Passa info do Tremy

    # Roda o jogo
    if mapa_aereo.mapa and (mapa_aereo.cavaleiros_bronze or mapa_aereo.cavaleiros_ouro or mapa_aereo.cavaleiro_prata):
        mapa_aereo.run()
    else:
        print("Falha ao inicializar. Verifique os arquivos e logs.")
        pygame.quit()
        sys.exit(1)

if __name__ == '__main__':
    main()