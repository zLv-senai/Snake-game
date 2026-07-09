import pygame
import os


from config import ( AMARELO, AZUL_ESCURO, BRANCO, CINZA, FPS_PADRAO,  PRETO,
                     TAMANHO, VERMELHO, ALTURA_principal, LARGURA_principal, calcular_fps, PASTA_SONS
)
from cobra import Cobra
from planeta import Planeta
from menu import tela_menu, carregar_som, tela_opcoes

def mostrar_pontuacao(tela, fonte, pontos):
    texto = fonte.render(f"Pontos: {pontos}", True, CINZA)
    tela.blit(texto, [10, 10])


def tela_game_over(tela, fonte, pontos, tempo_segundos):

    """Exibe a tela de game over com pontuação e tempo gastos na partida.
    da opção de jogar de novo, voltar ao menu, ir para opções ou sair do jogo.
    Navegação fluida pelas setas do teclado, contendo sons de movimentação e seleção"""



    fonte_titulo = pygame.font.SysFont("Arial", 42, bold=True)
    fonte_item = pygame.font.SysFont("Arial", 26)
    clock = pygame.time.Clock()

    som_mover = carregar_som("mover.ogg")
    som_selecionar = carregar_som("selecionar.ogg")

    pygame.mixer.music.load(os.path.join(PASTA_SONS, "musica_menu.mp3"))
    pygame.mixer.music.play(-1)

    pontuacao = fonte.render(f"Pontos: {pontos}", True, BRANCO)
    tempo = fonte.render(f"Tempo: {tempo_segundos:.2f} s", True, BRANCO)

    itens = ["Jogar de novo", "Voltar ao menu", "Opções", "Sair"]
    selecionado = 0

    esperando = True
    while esperando:
        largura, altura = tela.get_width(), tela.get_height()

        tela.fill(AZUL_ESCURO)

        titulo = fonte_titulo.render("Game Over", True, VERMELHO)
        tela.blit(titulo, [largura // 2 - titulo.get_width() // 2, altura // 4])    

        for i, item in enumerate(itens):
            cor = AMARELO if i == selecionado else CINZA
            prefixo = "> " if i == selecionado else "  "
            texto = fonte_item.render(prefixo + item, True, cor)
            y = altura // 2 + i * 40
            tela.blit(texto, [largura // 2 - texto.get_width() // 2, y])    

        tela.blit(tempo, [10, 40])
        tela.blit(pontuacao, [10, 10])

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
                    if itens[selecionado] == "Jogar de novo":
                        rodada(tela, fonte, clock)
                        esperando = False
                    elif itens[selecionado] == "Voltar ao menu":
                        tela_menu(tela)
                        esperando = False
                    elif itens[selecionado] == "Opções":
                        tela = tela_opcoes(tela)
                    elif itens[selecionado] == "Sair":
                        pygame.quit()
                        exit()

        clock.tick(FPS_PADRAO)


def rodada(tela, fonte, clock):
    """Executa uma partida até o jogador colidir. Retorna True se ele
    quiser jogar de novo (escolhido na tela de game over) e False se
    ele quiser sair.
    """
    largura, altura = tela.get_width(), tela.get_height()

    cobra = Cobra(largura // 2, altura // 2)
    planeta = Planeta(tipo="pequeno")

    inicio = pygame.time.get_ticks()

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

        if cobra.colidiu_com_borda(largura, altura) or cobra.colidiu_com_proprio_corpo():
            fim = pygame.time.get_ticks()
            tempo_segundos = (fim - inicio) / 1000
            return tela_game_over(tela, fonte, cobra.comprimento - 1, tempo_segundos)
            

        tela.fill(AZUL_ESCURO)
        planeta.desenhar(tela)
        cobra.desenhar(tela)
        mostrar_pontuacao(tela, fonte, cobra.comprimento - 1)
        pygame.display.update()

        if planeta.foi_comido_por(cobra.x, cobra.y):
            cobra.cresce()
            planeta.reposicionar()

        clock.tick(calcular_fps(tela.get_width(), tela.get_height()))


def jogo(tela):
    fonte = pygame.font.SysFont("Arial", 25)
    clock = pygame.time.Clock()

    jogar_de_novo = True
    while jogar_de_novo:
        jogar_de_novo = rodada(tela, fonte, clock)


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()

    tela = pygame.display.set_mode((LARGURA_principal, ALTURA_principal))
    pygame.display.set_caption("Snake Game - Devorar Planetas")

    from cobra import Cobra, carregar_imagens_cobra
    carregar_imagens_cobra()

    tela_menu(tela)
    jogo(tela)

    pygame.quit()