#Imports
import pygame
from pygame.locals import *
from sys import exit
from abc import ABC, abstractmethod

#pygame initialization
pygame.init()

#settings
FPS = 15
WIDTH = 1080
HEIGHT = 720
BLACK = (20, 100, 20)

#window settings
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Testador de Sprit')


#Define the abstract interfaces
class Transformable(ABC):
    @abstractmethod
    def transform(self):
        pass


class Spinable(ABC):
    @abstractmethod
    def spin(self):
        pass


class Posable(ABC):
    @abstractmethod
    def pose(self):
        pass


#Class Dio
class Dio(pygame.sprite.Sprite): #Inherits the pygame.sprite.Sprite class
    def __init__(self): #loads the transform, spin and pose images
        super().__init__()

        self.dio_transform_sprites = [pygame.image.load(f'Dio_transformação/{i}.png') for i in range(0, 24)]
        self.dio_spin_sprites = [pygame.image.load(f'Dio_giro/{i}.png') for i in range(0, 8)]
        self.dio_pose_sprites = [pygame.image.load(f'Dio_pose/{i}.png') for i in range(0, 11)]

        self.atual = 0
        self.image = self.dio_transform_sprites[self.atual]
        self.image = pygame.transform.scale(self.image, (128 * 3, 64 * 3))

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

        #State variables to control animations
        self.animate_transform = False
        self.animate_spin = False
        self.animate_pose = False

    #methods to enable animations
    def transform(self):
        self.animate_transform = True
        self.animate_spin = False
        self.animate_pose = False

    def spin(self):
        self.animate_spin = True
        self.animate_transform = False
        self.animate_pose = False

    def pose(self):
        self.animate_pose = True
        self.animate_transform = False
        self.animate_spin = False

    #method to call each frame to update the image
    def update(self):
        self._update_transform()
        self._update_spin()
        self._update_pose()

    #These methods Update the character image according to the activated animation
        def _update_transform(self):
            if self.animate_transform:
                self.atual += 0.5
                if self.atual >= len(self.dio_transform_sprites):
                    self.atual = 0
                    self.animate_transform = False
                self.image = self.dio_transform_sprites[int(self.atual)]
                self.image = pygame.transform.scale(self.image, (128 * 3, 64 * 3))

        def _update_spin(self):
            if self.animate_spin:
                self.atual += 0.5
                if self.atual >= len(self.dio_spin_sprites):
                    self.atual = 0
                    self.animate_spin = False
                self.image = self.dio_spin_sprites[int(self.atual)]
                self.image = pygame.transform.scale(self.image, (128 * 3, 64 * 3))

        def _update_pose(self):
            if self.animate_pose:
                self.atual += 0.5
                if self.atual >= len(self.dio_pose_sprites):
                    self.atual = 0
                    self.animate_pose = False
                self.image = self.dio_pose_sprites[int(self.atual)]
                self.image = pygame.transform.scale(self.image, (128 * 3, 64 * 3))


#Class FPSCounter
class FPSCounter:
    def __init__(self): #It will display the FPS counter
        self.font = pygame.font.SysFont('Arial', 20)

    def render(self, clock): #Will render the FPS in text
        fps_text = self.font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))


#Class KeyWordText
class KeyWordText:
    def __init__(self):  #Will display text with on-screen control keys
        self.font = pygame.font.SysFont('Arial', 20)
        self.text = "Pressione 'A' para Transformação, 'D' para Giro, 'E' para JOJOPose Pressione K_UP para aumentar FPS Pressione K_DOWN para diminuir FPS"

    def render(self): #Will render the keys to text
        teclas_text = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(teclas_text, (10, 40))


#Groups of sprites used to store them and facilitate their updates and renderings
all_sprites = pygame.sprite.Group()
transformable_sprites = pygame.sprite.Group()
spinable_sprites = pygame.sprite.Group()
posable_sprites = pygame.sprite.Group()

#Instantiate the character "Dio"
dio = Dio()
all_sprites.add(dio)
transformable_sprites.add(dio)
spinable_sprites.add(dio)
posable_sprites.add(dio)

#Configure the clock to control the frames per second rate
clock = pygame.time.Clock()

fps_counter = FPSCounter()
teclas_texto = KeyWordText()

#Project main loop 
while True:
    clock.tick(FPS) #Control FPS rate
    screen.fill(BLACK) #Sets the background

    #Events needed to process the desired animation according to the pressed key
    for event in pygame.event.get(): 
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_a:
                for sprite in transformable_sprites:
                    sprite.transform()
            elif event.key == K_d:
                for sprite in spinable_sprites:
                    sprite.spin()
            elif event.key == K_e:
                for sprite in posable_sprites:
                    sprite.pose()
            elif event.key == K_UP:
                FPS += 5
            elif event.key == K_DOWN:
                FPS -= 5

    #FPS, keys, sprites and screen update
    fps_counter.render(clock)
    teclas_texto.render()
    all_sprites.draw(screen)
    all_sprites.update()  
    pygame.display.flip() 
