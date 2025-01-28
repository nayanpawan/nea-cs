import pygame
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.update_time=pygame.time.get_ticks()
        self.x=x
        self.y=y
        self.speed=pygame.math.Vector2(3)

        self.health=True
        self.direction=1
        self.flip=False

        self.animation_list=[]
        self.frame_index=0
        self.action=0

        temp_list=[]
        for i in range(7):
            img=pygame.image.load(f'luffy idle/idle{i}.png')
            temp_list.append(img)
        self.animation_list.append(temp_list)  

        temp_list=[]
        for i in range(5):
            img=pygame.image.load(f'luffy walking/walking{i}.png')
            temp_list.append(img)
        self.animation_list.append(temp_list)   

        self.image=self.animation_list[self.frame_index][0]
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

    def update_action(self, new_action):
        if new_action != self.action:
            self.action=new_action
            self.frame_index=0
            self.update_time=pygame.time.get_ticks()
        else:
            self.action=self.action
    
    def update_animation(self):
        ANIMATION_COOLDOWN=125
        if pygame.time.get_ticks()-self.update_time>ANIMATION_COOLDOWN:
            self.update_time=pygame.time.get_ticks()
            self.frame_index+=1
        if self.frame_index> len(self.animation_list[self.action])-1:
            self.frame_index=0 
        self.image=self.animation_list[self.action][self.frame_index]    

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


