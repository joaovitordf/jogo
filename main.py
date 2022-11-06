import threading
import time

import pygame
from pygame.locals import *
from sys import exit
import threading

class Sapo(pygame.sprite.Sprite):

    def __init__(self, tela, dimensao_sapo, x_sapo, y_sapo):
        pygame.sprite.Sprite.__init__(self)
        self.tela = tela
        self.dimensao_sapo = dimensao_sapo
        self.x = x_sapo
        self.y = y_sapo
        self.sprites = []
        for i in range(1, 11):
            path_name = "sprite_sapo/attack_" + str(i) + ".png"
            image = pygame.image.load(path_name)
            self.sprites.append(image)
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image, self.dimensao_sapo)
        self.rect = self.image.get_rect()
        self.render()
        self.animar = False

    def atacar(self):
        self.animar = True

    def render(self):
        pygame.draw.rect(self.tela, (255, 0, 0),
                         pygame.Rect(self.x, self.y + 64, self.dimensao_sapo[0] - 128, self.dimensao_sapo[1] - 64))
        self.tela.blit(self.image, (self.x, self.y))

    def update(self):
        self.render()
        if self.animar:
            self.atual = self.atual + 0.5
            if self.atual >= len(self.sprites):
                self.atual = 0
                self.animar = False
            self.image = self.sprites[int(self.atual)]
            self.image = pygame.transform.scale(self.image, self.dimensao_sapo)


class Fogueira(pygame.sprite.Sprite):
    def __init__(self, dimensao):
        pygame.sprite.Sprite.__init__(self)
        self.dimensao = dimensao
        self.sprites = []
        for i in range(1, 5):
            path_name = "sprite_fogueira/Fogueira" + str(i) + ".png"
            image = pygame.image.load(path_name)
            self.sprites.append(image)
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image, self.dimensao)
        self.rect = self.image.get_rect()
        self.animar = True

    def update(self):
        self.atual = self.atual + 0.5
        if self.atual >= len(self.sprites):
            self.atual = 0
        self.image = self.sprites[int(self.atual)]
        self.image = pygame.transform.scale(self.image, self.dimensao)


class Personagem(pygame.sprite.Sprite):
    def __init__(self, tela, dimensao, estado, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.tela = tela
        self.dimensao = dimensao
        self.sprites = []
        self.estado = estado
        self.estado_personagem()
        self.ataque = self.estado_personagem()
        self.lado = self.estado_personagem()
        self.parado()
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image, self.dimensao)
        self.rect = self.image.get_rect()
        self.contador_atq = 0
        self.contador_andar = 0
        self.pos = (x, y)
        self.render()

    def estado_personagem(self):
        if self.estado == 'a':
            return 'esquerdo'
        elif self.estado == 'd':
            return 'direito'
        elif self.estado == 'j' or self.estado == 'w' or self.estado == 's':
            if self.ataque == 'esquerdo':
                return 'esquerdo'
            elif self.ataque == 'direito':
                return 'direito'


    def parado(self):
        if self.lado == "esquerdo":
            self.parado_esquerda()
        elif self.lado == "direito":
            self.parado_direita()
        else:
            self.parado_direita()

    def parado_direita(self):
        for i in range(1, 11):
            path_name = "Principal_parado/_Idle" + str(i) + ".png"
            image = pygame.image.load(path_name)
            self.sprites.append(image)

    def parado_esquerda(self):
        for i in range(1, 11):
            path_name = "Principal_parado_esquerda/_Idle" + str(i) + ".png"
            image = pygame.image.load(path_name)
            self.sprites.append(image)

    def atacarEsquerda(self):
        for i in range(1, 5):
            path_name = "Principal_ataqueDireita/_Attack" + str(i) + ".png"
            image = pygame.image.load(path_name)
            self.sprites.append(image)

    def atacarDireita(self):
        for i in range(1, 5):
            path_name = "Principal_ataquebasico/_Attack" + str(i) + ".png"
            image = pygame.image.load(path_name)
            self.sprites.append(image)

    def andar_direita(self):
        for i in range(1, 11):
            path_name = "Principal_direita/_Run" + str(i) + ".png"
            image = pygame.image.load(path_name)
            self.sprites.append(image)
        self.parado()

    def andar_esquerda(self):
        for i in range(1, 11):
            path_name = "Principal_esquerda/_Run" + str(i) + ".png"
            image = pygame.image.load(path_name)
            self.sprites.append(image)
        self.parado()

    def render(self):
        pygame.draw.rect(self.tela, (255, 0, 0),
                         pygame.Rect(self.pos[0], self.pos[1], self.dimensao[0], self.dimensao[1]))
        self.tela.blit(self.image, self.pos)

    def update(self):
        if self.estado == 'j' and self.ataque == "esquerdo" and self.contador_atq < 5:
            self.sprites = []
            self.atacarEsquerda()
            self.contador_atq += 1
            self.atual = self.atual + 0.4

        elif self.estado == 'j' and self.ataque == "direito" and self.contador_atq < 5:
            self.sprites = []
            self.atacarDireita()
            self.contador_atq += 1
            self.atual = self.atual + 0.4

        elif self.estado == 'w' and self.contador_andar < 11:
            self.sprites = []
            self.andar_direita()
            self.contador_andar += 1
            self.atual = self.atual + 1.75
        elif self.estado == 'd' and self.contador_andar < 11:
            self.sprites = []
            self.andar_direita()
            self.contador_andar += 1
            self.atual = self.atual + 1.75
            self.lado = "direito"

        elif self.estado == 'a' and self.contador_andar < 11:
            self.sprites = []
            self.andar_esquerda()
            self.contador_andar += 1
            self.atual = self.atual + 1.75
            self.lado = "esquerdo"

        elif self.estado == 's' and self.contador_andar < 11:
            self.sprites = []
            self.andar_esquerda()
            self.contador_andar += 1
            self.atual = self.atual + 1.75
        else:
            self.sprites = []
            self.parado()
            self.atual = self.atual + 0.5
        if self.atual >= len(self.sprites):
            self.atual = 0
        self.image = self.sprites[int(self.atual)]
        self.image = pygame.transform.scale(self.image, self.dimensao)

class Boss(pygame.sprite.Sprite):
    def __init__(self, tela, dimensao, x_boss, y_boss):
        pygame.sprite.Sprite.__init__(self)
        self.tela = tela
        self.dimensao = dimensao
        self.sprites = []
        self.atual = 0
        self.parado()
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image, self.dimensao)
        self.rect = self.image.get_rect()
        self.contador_atq = 0
        self.contador_andar = 0
        self.pos = (x_boss, y_boss)
        self.render()

    def parado(self):
        for i in range(1, 9):
            path_name = "Boss1/Individual_sprite/Idle/Bringer-of-Death_Idle_" + str(i) + ".png"
            image = pygame.image.load(path_name)
            self.sprites.append(image)

    def atacar(self):
        for i in range(1, 11):
            path_name = "Boss1/Individual_sprite/Attack/Bringer-of-Death_Attack_" + str(i) + ".png"
            image = pygame.image.load(path_name)
            self.sprites.append(image)

    def render(self):
        pygame.draw.rect(self.tela, (255, 0, 0),
                         pygame.Rect(self.pos[0], self.pos[1], self.dimensao[0], self.dimensao[1]))
        self.tela.blit(self.image, self.pos)

    def update(self):
        self.parado()
        self.atacar()

        self.atual = self.atual + 0.5
        if self.atual >= len(self.sprites):
            self.atual = 0
        self.image = self.sprites[int(self.atual)]
        self.image = pygame.transform.scale(self.image, self.dimensao)


def initialize_window():
    pygame.init()
    largura = 1280
    altura = 720
    fonte = pygame.font.SysFont('arial', 50, True, False)
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Jogao')
    return largura, altura, tela, fonte


def status_personagem():
    vida = 100
    ataque = 10
    defesa = 50
    return vida, ataque, defesa


def status_inimigo():
    vida = 100
    ataque = 10
    defesa = 50
    return vida, ataque, defesa


def main():
    clock = pygame.time.Clock()
    grupo_Sprite = pygame.sprite.Group()

    TESTE = []

    # Declarando dados da tela como a resolucao 1280x720
    largura, altura, tela, fonte = initialize_window()

    # Dados do personagem
    dimensao_personagem = (160, 160)
    x_personagem = 200
    y_personagem = 200
    velocidade = 40
    personagem_vida, persoangem_ataque, personagem_defesa = status_personagem()
    personagem = Personagem(tela, dimensao_personagem, 'p', x_personagem, y_personagem)
    personagem.rect = x_personagem, y_personagem
    grupo_Sprite.add(personagem)

    # Dados do sapo
    dimensao_sapo = (256, 128)
    sapo_vida, sapo_ataque, sapo_defesa = status_inimigo()
    x_sapo = int(500 - dimensao_sapo[0] / 2)
    y_sapo = int(500 - dimensao_sapo[1] / 2)
    sapo = Sapo(tela, dimensao_sapo, x_sapo, y_sapo)
    sapo.rect.topleft = x_sapo, y_sapo
    grupo_Sprite.add(sapo)

    # Dados da fogueira
    dimensao_fogueira = (128, 128)
    x_fogueira = int(largura / 2 - dimensao_fogueira[0] / 2)
    y_fogueira = int(altura / 2 - dimensao_fogueira[1] / 2)
    fogueira = Fogueira(dimensao_fogueira)
    fogueira.rect = x_fogueira, y_fogueira
    grupo_Sprite.add(fogueira)

    # Dados da boss
    dimensao_boss = (280, 186)
    x_boss = 300
    y_boss = 230
    boss = Boss(tela, dimensao_boss, x_boss, y_boss)
    boss.rect = x_boss, y_boss
    grupo_Sprite.add(boss)

    # Imagem de fundo
    imagem_fundo = pygame.image.load('Fundoinicial.png').convert()

    pygame.display.flip()

    while True:
        clock.tick(20)
        tela.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_l:
                    sapo.atacar()
                if event.key == K_a or event.key == K_LEFT:
                    if x_personagem > -30:
                        x_personagem -= velocidade
                    personagem.__init__(tela, dimensao_personagem, 'a', x_personagem, y_personagem)
                if event.key == K_d or event.key == K_RIGHT:
                    if x_personagem < largura - 100:
                        x_personagem += velocidade
                    personagem.__init__(tela, dimensao_personagem, 'd', x_personagem, y_personagem)

                if event.key == K_w or event.key == K_UP:
                    if y_personagem > -30:
                        y_personagem -= velocidade
                    personagem.__init__(tela, dimensao_personagem, 'w', x_personagem, y_personagem)
                if event.key == K_s or event.key == K_DOWN:
                    if y_personagem < altura - 100:
                        y_personagem += velocidade
                    personagem.__init__(tela, dimensao_personagem, 's', x_personagem, y_personagem)
                if event.key == K_j:
                    personagem.__init__(tela, dimensao_personagem, 'j', x_personagem, y_personagem)
                    area_personagem = pygame.Rect(x_personagem, y_personagem, dimensao_personagem[0],
                                                  dimensao_personagem[1])
                    area_sapo = pygame.Rect(x_sapo, y_sapo + 64, dimensao_sapo[0] - 128, dimensao_sapo[1] - 64)
                    if area_personagem.colliderect(area_sapo):
                        sapo_vida -= persoangem_ataque
                    TESTE = []
                if event.key == K_k:
                    TESTE.append('k')
                if event.key == K_i:
                    if len(TESTE) != 0 and TESTE[0] == 'k':
                        TESTE.append('i')
                        sapo_vida -= 90
                        print(TESTE)
                    else:
                        print('a')

        # Morte do sapo
        if sapo_vida <= 0:
            grupo_Sprite.remove(sapo)

        # Atualiza dados do personagem
        personagem.rect = x_personagem, y_personagem
        grupo_Sprite.add(personagem)

        # Atualiza imagem de fundo
        tela.blit(imagem_fundo, (0, 0))

        grupo_Sprite.draw(tela)
        grupo_Sprite.update()
        pygame.display.flip()
        pygame.display.update()


if __name__ == '__main__':
    main()
