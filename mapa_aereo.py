import pygame
import csv
import sys

# Constantes
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255) # Cor para valores não mapeados (se houver)

# --- Cores baseadas na imagem image_343f7d.png ---

# Terrenos
COR_PLANO = (210, 180, 140)  # Bege / Areia (Valor 14 no CSV)
COR_ROCHOSO = (160, 160, 160)  # Cinza Médio (Valor 15 no CSV)
COR_MONTANHOSO = (105, 105, 105) # Cinza Escuro / Tundra (Valor 16 no CSV)

# Pontos Especiais
COR_INICIO = (0, 255, 0)      # Verde Vivo (Valor 1 no CSV)
COR_FIM = (255, 0, 0)        # Vermelho Vivo (Valor 0 no CSV)

# Estruturas
COR_CASAS = (65, 105, 225)   # Azul "Royal" (Valores 2-13 no CSV)

# --- Fim das Cores ---

# Configurações (mantidas como no seu código)
TAMANHO_BLOCO = 15
NOME_ARQUIVO = 'coordernadasmapaco.csv'

def carregar_mapa(nome_arquivo):
    """Carrega o mapa do arquivo CSV."""
    mapa = []
    try:
        with open(nome_arquivo, 'r', newline='') as arquivo:
            leitor = csv.reader(arquivo)
            for linha in leitor:
                # Filtra strings vazias antes de converter para int
                linha_int = [int(valor) for valor in linha if valor.strip()]
                if linha_int: # Adiciona a linha apenas se não estiver vazia após a filtragem
                    mapa.append(linha_int)
            return mapa
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
        sys.exit(1)
    except ValueError as e:
        print(f"Erro ao converter valor no CSV para inteiro: {e}")
        print("Verifique se o arquivo CSV contém apenas números inteiros e não há células vazias ou vírgulas extras.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro inesperado ao carregar o mapa: {e}")
        sys.exit(1)

def obter_cor(valor):
    """Retorna a cor correspondente ao valor da célula."""
    if valor == 14:      # Terreno plano
        return COR_PLANO
    elif valor == 15:    # Terreno rochoso
        return COR_ROCHOSO
    elif valor == 16:    # Terreno montanhoso
        return COR_MONTANHOSO
    elif valor == 1:     # Início
        return COR_INICIO
    elif valor == 0:     # Fim
        return COR_FIM
    elif 2 <= valor <= 13: # Casas do Zodíaco
        return COR_CASAS
    else:
        # Define uma cor padrão para qualquer valor inesperado no CSV
        print(f"Aviso: Valor não mapeado encontrado no mapa: {valor}")
        return BRANCO # Ou PRETO, ou outra cor de aviso

def desenhar_mapa(tela, mapa):
    """Desenha o mapa na tela."""
    for i, linha in enumerate(mapa):
        for j, valor in enumerate(linha):
            x = j * TAMANHO_BLOCO
            y = i * TAMANHO_BLOCO
            cor = obter_cor(valor)
            pygame.draw.rect(tela, cor, (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO))
            pygame.draw.rect(tela, PRETO, (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO), 1)

def main():
    # Inicializa o Pygame
    pygame.init()
    
    # Carrega o mapa
    mapa = carregar_mapa(NOME_ARQUIVO)
    if not mapa:
        return

    # Configura a tela
    largura = len(mapa[0]) * TAMANHO_BLOCO
    altura = len(mapa) * TAMANHO_BLOCO
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Mapa do Santuário - Visão Aérea')

    # Loop principal
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # Limpa a tela
        tela.fill(PRETO)

        # Desenha o mapa
        desenhar_mapa(tela, mapa)

        # Atualiza a tela
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()