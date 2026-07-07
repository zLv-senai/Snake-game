import os

import pygame

from config import ALTURA, BRANCO, FPS_MENU, LARGURA, PASTA_SONS, PRETO, VERDE


def tela_menu(tela):
    fonte = pygame.font.SysFont("Arial", 25)
    clock = pygame.time.Clock()

    pygame.mixer.music.load(os.path.join(PASTA_SONS, "musica_menu.mp3"))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)

    esperando = True
    while esperando:
        tela.fill(PRETO)

        titulo = fonte.render("SNAKE GAME", True, VERDE)
        jogar = fonte.render("ENTER para jogar", True, BRANCO)
        opcoes = fonte.render("O para opções", True, BRANCO)

        tela.blit(titulo, [LARGURA // 2 - titulo.get_width() // 2, ALTURA // 2 - 80])
        tela.blit(jogar, [LARGURA // 2 - jogar.get_width() // 2, ALTURA // 2])
        tela.blit(opcoes, [LARGURA // 2 - opcoes.get_width() // 2, ALTURA // 2 + 35])

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    esperando = False
                if event.key == pygame.K_o:
                    tela_opcoes(tela)

        clock.tick(FPS_MENU)

    pygame.mixer.music.stop()


def tela_opcoes(tela):
    """Tela de opções simples: por enquanto só o volume da música.

    TODO: resolução da tela ainda não está aqui - mudar resolução em
    tempo real exige recriar a janela (pygame.display.set_mode) e
    coordenar com quem usa LARGURA/ALTURA em outros arquivos. É mais
    trabalhoso, então deixamos separado - avisem se quiserem ajuda.
    """
    fonte = pygame.font.SysFont("Arial", 25)
    clock = pygame.time.Clock()
    volume = pygame.mixer.music.get_volume()

    esperando = True
    while esperando:
        tela.fill(PRETO)

        titulo = fonte.render("OPÇÕES", True, VERDE)
        instrucao = fonte.render("Setas CIMA/BAIXO ajustam o volume", True, BRANCO)
        valor = fonte.render(f"Volume: {int(volume * 100)}%", True, BRANCO)
        voltar = fonte.render("ESC para voltar", True, BRANCO)

        tela.blit(titulo, [LARGURA // 2 - titulo.get_width() // 2, ALTURA // 2 - 100])
        tela.blit(instrucao, [LARGURA // 2 - instrucao.get_width() // 2, ALTURA // 2 - 40])
        tela.blit(valor, [LARGURA // 2 - valor.get_width() // 2, ALTURA // 2])
        tela.blit(voltar, [LARGURA // 2 - voltar.get_width() // 2, ALTURA // 2 + 60])

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    esperando = False
                if event.key == pygame.K_UP:
                    volume = min(1.0, volume + 0.1)
                    pygame.mixer.music.set_volume(volume)
                if event.key == pygame.K_DOWN:
                    volume = max(0.0, volume - 0.1)
                    pygame.mixer.music.set_volume(volume)

        clock.tick(FPS_MENU)
