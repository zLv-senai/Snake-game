import os
from math import sqrt

# Caminhos do projeto
PASTA_JOGO = os.path.dirname(os.path.abspath(__file__))
PASTA_SONS = os.path.join(PASTA_JOGO, "sons")

# Tela
LARGURA_principal = 800
ALTURA_principal = 400
FPS_PADRAO = 10




# Cores (Rgb)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
BRANCO = (255, 255, 255)

# Cores extras usadas no menu
AZUL_ESCURO = (10, 10, 35)
AMARELO = (255, 215, 0)
CINZA = (120, 120, 130)

RESOLUCOES = [
    (800, 600),
    (1024, 768),
    (1280, 720),
    (1366, 768),
    (1600, 900),
    (1920, 1080)
]

# Tamanho de cada bloco (cobra e planeta pequeno)
TAMANHO = 25


# Calcula o FPS ideal baseado na resolução da tela.

def calcular_fps(Largura_atual, Altura_atual):    
    area = Largura_atual * Altura_atual
    fator = sqrt(area / (LARGURA_principal * ALTURA_principal))
    return int(FPS_PADRAO * fator)

    
