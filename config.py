import os

# Caminhos do projeto
PASTA_JOGO = os.path.dirname(os.path.abspath(__file__))
PASTA_SONS = os.path.join(PASTA_JOGO, "sons")

# Tela
LARGURA = 600
ALTURA = 400
FPS_MENU = 15
FPS_JOGO = 10

# Cores (RGB)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
BRANCO = (255, 255, 255)

# Tamanho de cada bloco (cobra e planeta pequeno)
TAMANHO = 25
