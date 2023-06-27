import pygame
from pygame.locals import *
from sys import exit

pygame.init()

#Definir as Taxa de FPS, a largura, altura e a cor de fundo do projeto
FPS = 15  
WIDTH = 1080  
HEIGHT = 720  
BLACK = (20, 100, 20)  

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Criação da janela do jogo
pygame.display.set_caption('Testador de Sprit')  # Define o título da janela


#Classe do Personagem "Dio"
class Dio(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        # Carrega as imagens dos sprites de transformação, giro e pose do personagem
        self.dio_transform_sprites = [pygame.image.load(f'Dio_transformação/{i}.png') for i in range(0, 24)]
        self.dio_spin_sprites = [pygame.image.load(f'Dio_giro/{i}.png') for i in range(0, 8)]
        self.dio_pose_sprites = [pygame.image.load(f'Dio_pose/{i}.png') for i in range(0, 11)]

        self.atual = 0  # Índice do sprite atual
        self.image = self.dio_transform_sprites[self.atual]  # Define a primeira imagem de transformação
        self.image = pygame.transform.scale(self.image, (128 * 3, 64 * 3))  # Redimensiona a imagem
        
        self.rect = self.image.get_rect()  # Obtém o retângulo de colisão do sprite
        self.rect.center = (WIDTH // 2, HEIGHT // 2)  # Posiciona o sprite no centro da tela

        self.animate_transform  = False  # Controle de animação de transformação
        self.animate_spin = False  # Controle de animação de giro
        self.animate_pose = False  # Controle de animação de pose


#Campo onde vai definir qual animação vai ser ativada 
    def transform(self):
        self.animate_transform  = True
        self.animate_spin = False
        self.animate_pose = False

    def spin(self):
        self.animate_spin = True
        self.animate_transform  = False
        self.animate_pose = False

    def pose(self):
        self.animate_pose = True
        self.animate_transform  = False
        self.animate_spin = False

#Os eventos da animação
    def update(self):
        if self.animate_transform :  # Animação de transformação
            self.atual += 0.5
            if self.atual >= len(self.dio_transform_sprites):
                self.atual = 0
                self.animate_transform  = False
            self.image = self.dio_transform_sprites[int(self.atual)]
            self.image = pygame.transform.scale(self.image, (128 * 3, 64 * 3))
        elif self.animate_spin:  # Animação de giro
            self.atual += 0.5
            if self.atual >= len(self.dio_spin_sprites):
                self.atual = 0
                self.animate_spin = False
            self.image = self.dio_spin_sprites[int(self.atual)]
            self.image = pygame.transform.scale(self.image, (128 * 3, 64 * 3))
        elif self.animate_pose:  # Animação de pose
            self.atual += 0.5
            if self.atual >= len(self.dio_pose_sprites):
                self.atual = 0
                self.animate_pose = False
            self.image = self.dio_pose_sprites[int(self.atual)]
            self.image = pygame.transform.scale(self.image, (128 * 3, 64 * 3))


class FPSCounter:
    def __init__(self):
        self.font = pygame.font.SysFont('Arial', 20)

    def render(self, clock):
        fps_text = self.font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))


class KeyWordText:
    def __init__(self):
        self.font = pygame.font.SysFont('Arial', 20)
        self.text = "Pressione 'A' para Transformação, 'D' para Giro, 'E' para JOJOPose Pressione K_UP para aumentar FPS Pressione K_DOWN para diminuir FPS"

    def render(self):
        teclas_text = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(teclas_text, (10, 40))


all_sprites = pygame.sprite.Group()
dio = Dio()
all_sprites.add(dio)

clock = pygame.time.Clock()

fps_counter = FPSCounter()
teclas_texto = KeyWordText()

while True:
    clock.tick(FPS)
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_a:
                dio.transform()
            elif event.key == K_d:
                dio.spin()
            elif event.key == K_e:
                dio.pose()
            elif event.key == K_UP:
                FPS += 5
            elif event.key == K_DOWN:
                FPS -= 5

    fps_counter.render(clock)
    teclas_texto.render()
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
