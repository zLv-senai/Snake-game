import pygame

from config import ALTURA, BRANCO, FPS_JOGO, LARGURA, PRETO, TAMANHO, VERMELHO
from cobra import Cobra
from planeta import Planeta
from menu import tela_menu


def mostrar_pontuacao(tela, fonte, pontos):
    texto = fonte.render(f"Pontos: {pontos}", True, BRANCO)
    tela.blit(texto, [10, 10])


def tela_game_over(tela, fonte, pontos):
    while True:
        tela.fill(PRETO)

        msg = fonte.render("Game Over! Pressione C para continuar ou Q para sair", True, VERMELHO)
        pontuacao = fonte.render(f"Pontos: {pontos}", True, BRANCO)

        tela.blit(msg, [40, ALTURA // 2])
        tela.blit(pontuacao, [10, 10])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
                if event.key == pygame.K_c:
                    return True


def rodada(tela, fonte, clock):
    """Executa uma partida até o jogador colidir. Retorna True se ele
    quiser jogar de novo (escolhido na tela de game over) e False se
    ele quiser sair.
    """
    cobra = Cobra(LARGURA // 2, ALTURA // 2)
    planeta = Planeta(tipo="pequeno")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                # o "and cobra.dx == 0" impede inverter a direção na hora
                # e colidir com o próprio corpo instantaneamente
                if event.key == pygame.K_LEFT and cobra.dx == 0:
                    cobra.mudar_direcao(-TAMANHO, 0)
                elif event.key == pygame.K_RIGHT and cobra.dx == 0:
                    cobra.mudar_direcao(TAMANHO, 0)
                elif event.key == pygame.K_UP and cobra.dy == 0:
                    cobra.mudar_direcao(0, -TAMANHO)
                elif event.key == pygame.K_DOWN and cobra.dy == 0:
                    cobra.mudar_direcao(0, TAMANHO)

        cobra.mover()

        if cobra.colidiu_com_borda(LARGURA, ALTURA) or cobra.colidiu_com_proprio_corpo():
            return tela_game_over(tela, fonte, cobra.comprimento - 1)

        tela.fill(PRETO)
        planeta.desenhar(tela)
        cobra.desenhar(tela)
        mostrar_pontuacao(tela, fonte, cobra.comprimento - 1)
        pygame.display.update()

        if planeta.foi_comido_por(cobra.x, cobra.y):
            cobra.cresce()
            planeta.reposicionar()

        clock.tick(FPS_JOGO)


def jogo(tela):
    fonte = pygame.font.SysFont("Arial", 25)
    clock = pygame.time.Clock()

    jogar_de_novo = True
    while jogar_de_novo:
        jogar_de_novo = rodada(tela, fonte, clock)


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()

    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Snake Game - Devorar Planetas")

    from cobra import Cobra, carregar_imagens_cobra
    carregar_imagens_cobra()

    tela_menu(tela)
    jogo(tela)

    pygame.quit()