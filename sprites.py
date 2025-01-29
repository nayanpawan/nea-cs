import pygame
import os
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
        self.attacking=False

        self.animation_list=[]
        self.frame_index=0
        self.action=0

        animations=['idle', 'walking', 'attack']
        for animation in animations:
            temp_list=[]
            frames=len(os.listdir(f'luffy {animation}'))
            for i in range(frames):
                img=pygame.image.load(f'luffy {animation}/{animation}{i}.png')
                original_width, original_height = img.get_size()
                new_width = int(original_width * (0.66))
                new_height = int(original_height * (0.66))
                img = pygame.transform.scale(img, (new_width, new_height))
                temp_list.append(img)
            self.animation_list.append(temp_list)  

        self.image=self.animation_list[self.frame_index][0]
        self.rect=self.image.get_rect(center=(self.x,self.y))    


    def movement(self, moving_left, moving_right, moving_up, moving_down, attacking, walls):
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
        if attacking:
            self.attacking=True     

        
        self.rect.x+=dx
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.x-=dx
        self.rect.y+=dy
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.y-=dy

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
            if self.attacking:
                self.attacking=False
            self.frame_index=0 
        self.image=self.animation_list[self.action][self.frame_index]    

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, colour):
        pygame.sprite.Sprite.__init__(self)
        self.colour=colour
        self.rect=pygame.Rect(x,y,width,height)
