import pygame
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.update_time=pygame.time.get_ticks()
        self.x=x
        self.y=y
        self.speed=pygame.math.Vector2(3)

        self.direction=1
        self.flip=False

        self.idle_animation_list=[]
        self.frame_index=0
        for i in range(7):
            img=pygame.image.load(f'luffy idle/idle{i}.png')
            self.idle_animation_list.append(img)
        self.image=self.idle_animation_list[self.frame_index]
        self.rect=self.image.get_frect(center=(self.x,self.y))    


    def movement(self, moving_left, moving_right, moving_up, moving_down):
        dy=0
        dx=0
        
        if moving_left:
            dx=-self.speed.x
            self.flip=False
            self.direction=1
        if moving_right:
            dx=self.speed.x
            self.flip=True
            self.direction=-1
        if moving_up:
            dy=-self.speed.y 
        if moving_down:
            dy=self.speed.y  

        self.rect.x+=dx
        self.rect.y+=dy    

    def update_animation(self):
        ANIMATION_COOLDOWN=165
        if pygame.time.get_ticks()-self.update_time>ANIMATION_COOLDOWN:
            self.update_time=pygame.time.get_ticks()
            self.frame_index+=1
        if self.frame_index> len(self.idle_animation_list)-1:
            self.frame_index=0 
        self.image=self.idle_animation_list[self.frame_index]    

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


