import random

import pygame

from config import ALTURA, LARGURA, TAMANHO, VERMELHO


class Planeta:
    """Representa o que a cobra come.

    Por enquanto é desenhado como um quadrado vermelho (a "maçã" que
    o exemplo original usava). Quando tiverem os sprites dos planetas,
    troquem só o método desenhar() - o resto (tipo, pontos, tamanho)
    já está pronto pra planeta pequeno e planeta grande.
    """

    PONTOS_POR_TIPO = {
        "pequeno": 1,
        "grande": 3,
    }

    TAMANHO_POR_TIPO = {
        "pequeno": TAMANHO,
        "grande": TAMANHO * 2,
    }

    def __init__(self, tipo="pequeno"):
        self.tipo = tipo
        self.tamanho = self.TAMANHO_POR_TIPO[tipo]
        self.pontos = self.PONTOS_POR_TIPO[tipo]
        self.x = 0
        self.y = 0
        self.reposicionar()

    def reposicionar(self):
        self.x = random.randrange(0, LARGURA - self.tamanho, TAMANHO)
        self.y = random.randrange(0, ALTURA - self.tamanho, TAMANHO)

    def foi_comido_por(self, cobra_x, cobra_y):
        # TODO: essa comparação exata (==) funciona bem para o planeta
        # pequeno (mesmo tamanho de um segmento da cobra). Para o planeta
        # "grande" (2x o tamanho), troquem por colisão de retângulos:
        # pygame.Rect(cobra_x, cobra_y, TAMANHO, TAMANHO).colliderect(
        #     pygame.Rect(self.x, self.y, self.tamanho, self.tamanho))
        return cobra_x == self.x and cobra_y == self.y

    def desenhar(self, tela):
        pygame.draw.rect(tela, VERMELHO, [self.x, self.y, self.tamanho, self.tamanho])
