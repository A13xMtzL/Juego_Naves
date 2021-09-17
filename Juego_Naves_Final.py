import pygame, random

class Laser(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("laser.png").convert()
        self.image.set_colorkey(negro)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y -= 7


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.yy = 2
        self.image = pygame.image.load('meteoro1.png').convert()
        self.image.set_colorkey(negro)
        self.rect = self.image.get_rect()
        
        self.rect.x = random.randrange(WIDTH - self.rect.width) #Rengo en el que aparecerá el meteorito 
        self.rect.y = random.randrange(-100, -40)  #Crea el efecto de que los meteoros están cayendo 
       #Declaramos velocidades de moviemento en ambos ejes
        self.speedy = random.randrange(1, 10) 
        self.speedx = random.randrange(-5, 5)
        
    def update(self):
      #Cada meterotio adquiere su propia velocidad
      self.rect.x += random.randint(-3,3) 
      
      
      self.rect.y += self.speedy
      self.rect.x += self.speedx
      #Revisamos si el meteorito ha salido de la pantalla y si es el caso, este se reseteará en la pantalla
      if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 25:
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 10)

      if self.rect.y > 600 - self.rect.height or self.rect.y < 0:
        self.yy = -self.yy

      self.rect.y += self.yy


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("nave2.png").convert()
        self.image.set_colorkey(negro)
        self.rect = self.image.get_rect()
    
    def  update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.rect.x = mouse_pos[0]
        self.rect.y = mouse_pos[1]
      

    
negro = 0,0,0
blanco = 255,255,255
verde_a= 1,218,158
WIDTH=900
HEIGHT=600

def draw_text(surface, text, size, x, y): #Función que mostrará el contador de puntos en pantalla
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, verde_a)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode([WIDTH,HEIGHT])

    
    clock = pygame.time.Clock()
    run = True
    score = 0

    #Textos
    fuente = pygame.font.Font(None, 50)
    texto = fuente.render('Score: ', 0, (255, 255, 255))
    
    fuenteSistema = pygame.font.SysFont("Castellar", 50)
    
    
    width=900
    height=600
    i=0
    
    fondo = pygame.image.load('fondo1.jpg')
    fondorect = fondo.get_rect();
    bg=pygame.transform.scale(fondo,(900,600))




    all_sprite_list = pygame.sprite.Group()
    meteor_list = pygame.sprite.Group()
    laser_list = pygame.sprite.Group()

    for i in range(20):
        meteor = Meteor()
        all_sprite_list.add(meteor)
        meteor_list.add(meteor)
        meteor.rect.x = random.randrange(800)
        meteor.rect.y = random.randrange(400)

    player = Player()
    all_sprite_list.add(player)

    sound = pygame.mixer.Sound('laser5.ogg')
    pygame.mixer.Sound.set_volume(sound,0.3)  #Definimos el volumen de los sonidos 
    
    explosion_sound=pygame.mixer.Sound('explosion.wav')
    pygame.mixer.Sound.set_volume(explosion_sound,0.1)
    
    pygame.mixer.music.load('musica.mp3') #Se carga la mussica a utilizar 
    pygame.mixer.music.set_volume(0.1)  #Definimos el volumen del sonido
    pygame.mixer.music.play(2)  #el numero indica el numero de veces que se repite la música 


    while run:
        for event in pygame.event.get(): #se captura el evento que se produce
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                laser = Laser()
                laser.rect.x = player.rect.x + 20
                laser.rect.y = player.rect.y - 24

                all_sprite_list.add(laser)
                laser_list.add(laser)
                sound.play()


    
        all_sprite_list.update() #actualiza el movimiento de los sprite
        #se definen las colisiones
        for laser in laser_list:
            meteor_hit_list = pygame.sprite.spritecollide(laser, meteor_list, True) # el true es para que desaparezcan
            
            #para eliminar el laser en las colisiones
            for meteor in meteor_hit_list:
                all_sprite_list.remove(laser)
                laser_list.remove(laser)
                score += 1
                texto2 = fuenteSistema.render(str(score), True, (255, 255, 255))
                screen.blit(texto2, (700,550))
                print(score)
                explosion_sound.play()
            if laser.rect.y < 0:
                all_sprite_list.remove(laser)
                laser_list.remove(laser)        
        
        #nuevo
        screen.fill((negro))
        screen.blit(bg,(i,0))
        screen.blit(bg,(height+i,0))

        if i==-height:
          screen.blit(bg,(height+i,0))
          i=0
        i-=1        

        all_sprite_list.draw(screen) #se pintan todos los sprites

        ##Marcador
        draw_text(screen, str(score), 25, 830, 553) #Se llama a la función que imprimirá el score en pantalla 


        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
