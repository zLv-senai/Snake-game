import random

import pygame
import os

from config import  TAMANHO, VERMELHO

#pastas
game_folder = os.path.dirname(__file__)
disign_folder = os.path.join(game_folder, "disign")

def carregar_imagem_arrumada(caminho, tamanho):
    img = pygame.image.load(caminho).convert_alpha()
    bounding_rect = img.get_bounding_rect()
    img_recortada = img.subsurface(bounding_rect).copy()
    img_final = pygame.transform.scale(img_recortada, (tamanho, tamanho))
    return img_final

imagem_planeta = []

def carregar_planeta_imagem():
    global imagem_planeta
    imagem_planeta = [
        carregar_imagem_arrumada(os.path.join(disign_folder, "planeta1.png"), TAMANHO),
        carregar_imagem_arrumada(os.path.join(disign_folder, "planeta2.png"), TAMANHO),
        carregar_imagem_arrumada(os.path.join(disign_folder, "planeta3.png"), TAMANHO)
    ]

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
        self.imagem = None
        self.reposicionar()

    def reposicionar(self):

        """Coloca o planeta em uma posição aleatória na tela."""

        largura, altura = pygame.display.get_surface().get_size()

        self.x = random.randrange(0, largura - self.tamanho, TAMANHO)
        self.y = random.randrange(0, altura - self.tamanho, TAMANHO)

        imagem_original = random.choice(imagem_planeta)
        self.imagem = pygame.transform.scale(imagem_original, (self.tamanho, self.tamanho))

    def foi_comido_por(self, cobra_x, cobra_y):
        # Cria as hitboxes (caixas de colisão) baseadas nas posições e tamanhos atuais
        hitbox_cobra = pygame.Rect(cobra_x, cobra_y, TAMANHO, TAMANHO)
        hitbox_planeta = pygame.Rect(self.x, self.y, self.tamanho, self.tamanho)
        
        # O colliderect retorna True se os retângulos se tocarem, e False caso contrário
        return hitbox_cobra.colliderect(hitbox_planeta)

    def desenhar(self, tela):
          tela.blit(self.imagem, (self.x, self.y))
