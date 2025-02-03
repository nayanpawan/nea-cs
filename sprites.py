import pygame
import os
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.update_time=pygame.time.get_ticks()
        self.x=x
        self.y=y
        self.speed=pygame.math.Vector2(3)
        self.moving_left=False
        self.moving_right=False
        self.moving_up=False
        self.moving_down=False

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


    def movement(self, event):
        dy=0
        dx=0

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_d:
                self.moving_right=True
            if event.key==pygame.K_a:
                self.moving_left=True
            if event.key==pygame.K_w:
                self.moving_up=True
            if event.key==pygame.K_s:
                self.moving_down=True
            if event.key==pygame.K_k:
                if not self.attacking:
                    self.attacking=True
            
            
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_d:
                self.moving_right=False
            if event.key==pygame.K_a:
                self.moving_left=False
            if event.key==pygame.K_w:
                self.moving_up=False             
            if event.key==pygame.K_s:
                self.moving_down=False 
            if event.key==pygame.K_k:
                pass
                #self.attacking=False    


        if self.moving_left:
            dx=-self.speed.x
            self.flip=False
            self.direction=1
        
        if self.moving_right:
            dx=self.speed.x
            self.flip=True
            self.direction=-1
        
        if self.moving_up:
            dy=-self.speed.y 
        
        if self.moving_down:
            dy=self.speed.y 
        
        if self.attacking:
            self.attacking=True     


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
            if self.attacking:
                self.attacking=False
            self.frame_index=0 
        self.image=self.animation_list[self.action][self.frame_index]    

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, cell, CELL_SIZE):
        pygame.sprite.Sprite.__init__(self)
        if cell==1:
            self.image = pygame.Surface((CELL_SIZE, CELL_SIZE)) 
            self.image.fill((136,140,141))
            self.rect=pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        elif cell==2:
            self.image = pygame.Surface((CELL_SIZE, CELL_SIZE)) 
            self.image.fill((250,249,247))
            self.rect=pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        elif cell==3:
            self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))  
            self.image.fill((38,102,145))
            self.rect=pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        else:
            self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))  
            self.image.fill((86,125,70))
            self.rect=pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)  