import pygame
class Player(pygame.sprite.Sprite):
    def __init__(self, image, WIDTH, HEIGHT):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(image)
        self.x=WIDTH//2
        self.y=HEIGHT//2
        self.rect=self.image.get_frect(center=(self.x,self.y))
        self.speed=pygame.math.Vector2(3)

    def movement(self, moving_left, moving_right, moving_up, moving_down):
        dy=0
        dx=0
        
        if moving_left:
            dx=-self.speed.x
        if moving_right:
            dx=self.speed.x
        if moving_up:
            dy=-self.speed.y 
        if moving_down:
            dy=self.speed.y  

        self.rect.x+=dx
        self.rect.y+=dy    

    def draw(self, screen):
        screen.blit(self.image, self.rect)


