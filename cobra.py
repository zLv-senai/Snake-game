import pygame

from config import TAMANHO, VERDE


class Cobra:
    """Representa a cobra: seus segmentos, direção e movimento."""

    def __init__(self, x_inicial, y_inicial):
        self.x = x_inicial
        self.y = y_inicial
        self.dx = 0
        self.dy = 0
        self.segmentos = []
        self.comprimento = 1

    def mudar_direcao(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def mover(self):
        self.x += self.dx
        self.y += self.dy

        cabeca = [self.x, self.y]
        self.segmentos.append(cabeca)

        if len(self.segmentos) > self.comprimento:
            del self.segmentos[0]

    def cresce(self):
        self.comprimento += 1

    def colidiu_com_borda(self, largura, altura):
        return self.x < 0 or self.x >= largura or self.y < 0 or self.y >= altura

    def colidiu_com_proprio_corpo(self):
        cabeca = self.segmentos[-1]
        return cabeca in self.segmentos[:-1]

    def desenhar(self, tela):
        for bloco in self.segmentos:
            pygame.draw.rect(tela, VERDE, [bloco[0], bloco[1], TAMANHO, TAMANHO])
