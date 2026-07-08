import pygame
import os

from config import TAMANHO, VERDE

#Pastas
game_folder = os.path.dirname(__file__)
disign_folder = os.path.join(game_folder, "disign")

def carregar_imagem_ajustada(caminho, tamanho):

    img = pygame.image.load(caminho).convert_alpha()
    
    # Descobre o retângulo que contém o desenho (ignora pixels transparentes)
    bounding_rect = img.get_bounding_rect()
    
    # Recorta só essa área
    img_recortada = img.subsurface(bounding_rect).copy()
    
    # Agora sim, redimensiona para o tamanho do bloco
    img_final = pygame.transform.scale(img_recortada, (tamanho, tamanho))
    return img_final

img_cabeca_original = None
img_corpo = None

def carregar_imagens_cobra():
    global img_cabeca_original, img_corpo
    img_cabeca_original = carregar_imagem_ajustada(os.path.join(disign_folder, "cabeca.png"), TAMANHO)
    img_corpo = carregar_imagem_ajustada(os.path.join(disign_folder, "corpo.png"), TAMANHO)

    
class Cobra:
    """Representa a cobra: seus segmentos, direção e movimento."""

    def __init__(self, x_inicial, y_inicial):
        self.x = x_inicial
        self.y = y_inicial
        self.dx = 0
        self.dy = 0
        self.segmentos = []
        self.direcoes = []          # <-- guarda a direção de cada segmento
        self.comprimento = 1

    def mudar_direcao(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def mover(self):
        self.x += self.dx
        self.y += self.dy

        cabeca = [self.x, self.y]
        self.segmentos.append(cabeca)
        self.direcoes.append((self.dx, self.dy))   # <-- salva a direção junto

        if len(self.segmentos) > self.comprimento:
            del self.segmentos[0]
            del self.direcoes[0]

    def cresce(self):
        self.comprimento += 1

    def colidiu_com_borda(self, largura, altura):
        return self.x < 0 or self.x >= largura or self.y < 0 or self.y >= altura

    def colidiu_com_proprio_corpo(self):
        cabeca = self.segmentos[-1]
        return cabeca in self.segmentos[:-1]

    def _rotacionar(self, imagem, dx, dy):
        if dx == TAMANHO:
            angulo = 0        # direita
        elif dx == -TAMANHO:
            angulo = 180      # esquerda
        elif dy == -TAMANHO:
            angulo = 90       # cima
        elif dy == TAMANHO:
            angulo = -90      # baixo
        else:
            angulo = 0
        return pygame.transform.rotate(imagem, angulo)

    def desenhar(self, tela):
        # corpo primeiro
        for i, bloco in enumerate(self.segmentos[:-1]):
            dx, dy = self.direcoes[i]
            img = self._rotacionar(img_corpo, dx, dy)
            tela.blit(img, (bloco[0], bloco[1]))

        # cabeça por cima
        cabeca = self.segmentos[-1]
        dx, dy = self.direcoes[-1]
        img_cabeca = self._rotacionar(img_cabeca_original, dx, dy)
        tela.blit(img_cabeca, (cabeca[0], cabeca[1]))