import os
import random
import pygame

from config import (FPS_PADRAO, AMARELO, AZUL_ESCURO,
    BRANCO, CINZA, VERDE, 
    PASTA_SONS,
    RESOLUCOES,
)


def carregar_som(nome_arquivo):
    """Carrega um som opcional - se o arquivo ainda não existir, não quebra o jogo."""
    try:
        return pygame.mixer.Sound(os.path.join(PASTA_SONS, nome_arquivo))
    except (pygame.error, FileNotFoundError):
        return None
    
def gerar_estrelas(largura, altura, quantidade=40):
    return [
        (random.randrange(0, largura), random.randrange(0, altura), random.randint(1, 2))
        for _ in range(quantidade)
    ]

def desenhar_estrelas(tela, estrelas):
    for x, y, raio in estrelas:
        pygame.draw.circle(tela, BRANCO, (x, y), raio)





def tela_menu(tela):
    """Tela inicial. Retorna a tela (pode ter mudado de tamanho, se o
    jogador trocou a resolução na tela de opções)."""

    fonte_titulo = pygame.font.SysFont("Arial", 42, bold=True)
    fonte_item = pygame.font.SysFont("Arial", 26)
    clock = pygame.time.Clock()

    som_mover = carregar_som("menu_mover.wav")
    som_selecionar = carregar_som("menu_selecionar.wav")

    pygame.mixer.music.load(os.path.join(PASTA_SONS, "musica_menu.mp3"))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)

    estrelas = gerar_estrelas(tela.get_width(), tela.get_height())

    itens = ["Jogar", "Opções", "Sair"]
    selecionado = 0

    esperando = True
    while esperando:
        largura, altura = tela.get_width(), tela.get_height()

        tela.fill(AZUL_ESCURO)
        desenhar_estrelas(tela, estrelas)

        titulo = fonte_titulo.render("SNAKE GAME", True, VERDE)
        tela.blit(titulo, [largura // 2 - titulo.get_width() // 2, altura // 4])

        for i, item in enumerate(itens):
            cor = AMARELO if i == selecionado else CINZA
            prefixo = "> " if i == selecionado else "  "
            texto = fonte_item.render(prefixo + item, True, cor)
            y = altura // 2 + i * 40
            tela.blit(texto, [largura // 2 - texto.get_width() // 2, y])

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selecionado = (selecionado - 1) % len(itens)
                    if som_mover:
                        som_mover.play()
                if event.key == pygame.K_DOWN:
                    selecionado = (selecionado + 1) % len(itens)
                    if som_mover:
                        som_mover.play()
                if event.key == pygame.K_RETURN:
                    if som_selecionar:
                        som_selecionar.play()
                    if itens[selecionado] == "Jogar":
                        esperando = False
                    elif itens[selecionado] == "Opções":
                        tela = tela_opcoes(tela)
                        estrelas = gerar_estrelas(tela.get_width(), tela.get_height())
                    elif itens[selecionado] == "Sair":
                        pygame.quit()
                        exit()

        clock.tick(FPS_PADRAO)

    pygame.mixer.music.stop()
    return tela

def tela_opcoes(tela):
    """Tela de opções: volume e resolução. Retorna a tela (nova, se a
    resolução foi trocada)."""
    fonte_titulo = pygame.font.SysFont("Arial", 32, bold=True)
    fonte_item = pygame.font.SysFont("Arial", 24)
    clock = pygame.time.Clock()

    som_mover = carregar_som("mover.wav")
    som_selecionar = carregar_som("selecionar.wav")

    volume = pygame.mixer.music.get_volume()
    indice_resolucao = 0
    for i, (l, a) in enumerate(RESOLUCOES):
        if (l, a) == (tela.get_width(), tela.get_height()):
            indice_resolucao = i
            break

    opcoes = ["Volume", "Resolução", "Voltar"]
    selecionado = 0

    esperando = True
    while esperando:
        largura, altura = tela.get_width(), tela.get_height()

        tela.fill(AZUL_ESCURO)

        titulo = fonte_titulo.render("OPÇÕES", True, VERDE)
        tela.blit(titulo, [largura // 2 - titulo.get_width() // 2, altura // 6])

        valores = [
            f"{int(volume * 100)}%",
            f"{RESOLUCOES[indice_resolucao][0]}x{RESOLUCOES[indice_resolucao][1]}",
            "",
        ]

        for i, nome in enumerate(opcoes):
            cor = AMARELO if i == selecionado else CINZA
            prefixo = "> " if i == selecionado else "  "
            linha = f"{prefixo}{nome}  {valores[i]}".rstrip()
            texto = fonte_item.render(linha, True, cor)
            y = altura // 2 - 20 + i * 40
            tela.blit(texto, [largura // 2 - texto.get_width() // 2, y])

        instrucao = fonte_item.render("Setas: navegar/ajustar   ESC: voltar", True, CINZA)
        tela.blit(instrucao, [largura // 2 - instrucao.get_width() // 2, altura - 40])

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selecionado = (selecionado - 1) % len(opcoes)
                    if som_mover:
                        som_mover.play()
                if event.key == pygame.K_DOWN:
                    selecionado = (selecionado + 1) % len(opcoes)
                    if som_mover:
                        som_mover.play()
                if event.key == pygame.K_LEFT:
                    if opcoes[selecionado] == "Volume":
                        volume = max(0.0, volume - 0.1)
                        pygame.mixer.music.set_volume(volume)
                    elif opcoes[selecionado] == "Resolução":
                        indice_resolucao = (indice_resolucao - 1) % len(RESOLUCOES)
                if event.key == pygame.K_RIGHT:
                    if opcoes[selecionado] == "Volume":
                        volume = min(1.0, volume + 0.1)
                        pygame.mixer.music.set_volume(volume)
                    elif opcoes[selecionado] == "Resolução":
                        indice_resolucao = (indice_resolucao + 1) % len(RESOLUCOES)
                confirmou_voltar = event.key == pygame.K_ESCAPE or (
                    event.key == pygame.K_RETURN and opcoes[selecionado] == "Voltar"
                )
                if confirmou_voltar:
                    if som_selecionar:
                        som_selecionar.play()
                    nova_largura, nova_altura = RESOLUCOES[indice_resolucao]
                    if (nova_largura, nova_altura) != (tela.get_width(), tela.get_height()):
                        tela = pygame.display.set_mode((nova_largura, nova_altura))
                    esperando = False

        clock.tick(FPS_PADRAO)

    return tela
