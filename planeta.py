import random

import pygame


from config import  TAMANHO, VERMELHO



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

        """Coloca o planeta em uma posição aleatória na tela."""

        largura, altura = pygame.display.get_surface().get_size()

        self.x = random.randrange(0, largura - self.tamanho, TAMANHO)
        self.y = random.randrange(0, altura - self.tamanho, TAMANHO)

    def foi_comido_por(self, cobra_x, cobra_y):
        # Cria as hitboxes (caixas de colisão) baseadas nas posições e tamanhos atuais
        hitbox_cobra = pygame.Rect(cobra_x, cobra_y, TAMANHO, TAMANHO)
        hitbox_planeta = pygame.Rect(self.x, self.y, self.tamanho, self.tamanho)
        
        # O colliderect retorna True se os retângulos se tocarem, e False caso contrário
        return hitbox_cobra.colliderect(hitbox_planeta)

    def desenhar(self, tela):
        pygame.draw.rect(tela, VERMELHO, [self.x, self.y, self.tamanho, self.tamanho])
