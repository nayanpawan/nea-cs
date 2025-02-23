import pygame
import os
import random

pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.update_time=pygame.time.get_ticks()

        self.x=x
        self.y=y
        self.speed=pygame.math.Vector2(4)
        self.moving_left=False
        self.moving_right=False
        self.moving_up=False
        self.moving_down=False
        self.dx=0
        self.dy=0

        self.health=True
        self.max_hp=100
        self.hp=self.max_hp
        self.max_stamina=100
        self.stamina=self.max_stamina

        self.direction=1
        self.flip=False
        self.attacking=False
        self.in_water=False
        self.water_damage_timer = 0 
        self.heal_timer=0

        self.animation_list=[]
        self.frame_index=0
        self.action=0
        self.scale=0.7

        animations=['idle', 'walking', 'attack','dying']
        for animation in animations:
            temp_list=[]
            frames=len(os.listdir(f'luffy {animation}'))
            for i in range(frames):
                img=pygame.image.load(f'luffy {animation}/{animation}{i}.png').convert_alpha()
                original_width, original_height = img.get_size()
                new_width = int(original_width * (self.scale))
                new_height = int(original_height * (self.scale))
                img = pygame.transform.scale(img, (new_width, new_height))
                temp_list.append(img)
            self.animation_list.append(temp_list)  

        self.image=self.animation_list[self.frame_index][0]
        self.rect=self.image.get_rect(topleft=(self.x,self.y))    


    def movement(self, events, collideable_terrain, all_terrain_group, CELL_SIZE, GRID_SIZE, WORLD_SIZE):

        self.dx=0
        self.dy=0 

        for event in events:
            if event.type==pygame.QUIT:
                pygame.quit()

            if self.health:    

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
                            self.stamina-=2
                            if self.stamina>2:
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

        self.check_terrain(all_terrain_group)

        if self.moving_left:
            self.dx=-self.speed.x
            self.flip=False
            self.direction=1
        
        if self.moving_right:
            self.dx=self.speed.x
            self.flip=True
            self.direction=-1
        
        if self.moving_up:
            self.dy=-self.speed.y
        
        if self.moving_down:
            self.dy=self.speed.y
             


        self.rect.x+=self.dx
        self.handle_collisions(collideable_terrain, CELL_SIZE, GRID_SIZE, WORLD_SIZE)
        self.rect.y+=self.dy
        self.handle_collisions(collideable_terrain, CELL_SIZE, GRID_SIZE, WORLD_SIZE)


    def handle_collisions(self, collideable_terrain, CELL_SIZE, GRID_SIZE, WORLD_SIZE):
        for tile in collideable_terrain:
            if self.rect.colliderect(tile.rect):  
                if self.moving_right:
                    self.rect.x-=self.dx
                if self.moving_left:
                    self.rect.x-=self.dx
                if self.moving_up:
                    self.rect.y-=self.dy
                if self.moving_down:
                    self.rect.y-=self.dy
        if self.rect.x<0 or self.rect.x>CELL_SIZE*GRID_SIZE*WORLD_SIZE-self.rect.width:
            self.rect.x-=self.dx
        if self.rect.y<0 or self.rect.y>CELL_SIZE*GRID_SIZE*WORLD_SIZE-self.rect.height:
            self.rect.y-=self.dy
    
    def check_terrain(self, all_terrain_group):
        self.in_water=False
        for block in all_terrain_group:
            if self.rect.colliderect(block.rect):
                if block.cell==3: #3:water#
                    self.in_water=True
                    self.speed=pygame.math.Vector2(2)
                else:
                    self.speed=pygame.math.Vector2(4)  

        if self.in_water:
            self.water_damage_timer += 1
            if self.water_damage_timer % 60 == 0:
                self.hp -= 5    
        else:
            self.speed = pygame.math.Vector2(4)   
            self.water_damage_timer = 0                  

    def heal(self):
        if self.hp<100 and self.stamina>40 and self.health:
            self.heal_timer+=1
            if self.heal_timer % 120==0:
                self.hp+=5
                self.stamina-=5
        else:
            self.heal_timer=0        


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
            if self.action == 3: 
                self.frame_index = len(self.animation_list[self.action]) - 1 
            else:
                self.frame_index = 0  
        self.image=self.animation_list[self.action][self.frame_index]    

    def draw(self, screen, camera_x, camera_y):
        screen.blit(pygame.transform.flip(self.image, self.flip, False),(self.rect.x + camera_x, self.rect.y + camera_y))
        #pygame.draw.rect(screen, (255, 0, 0), self.rect.move(camera_x, camera_y), 2) 

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, cell, CELL_SIZE,a,b,GRID_SIZE):
        pygame.sprite.Sprite.__init__(self)
        self.cell=cell
        if cell==1:
            self.image = pygame.Surface((CELL_SIZE, CELL_SIZE)) 
            self.image.fill((136,140,141))
            self.rect=pygame.Rect(a*GRID_SIZE*CELL_SIZE+x * CELL_SIZE,b*GRID_SIZE*CELL_SIZE+ y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        elif cell==2:
            self.image = pygame.Surface((CELL_SIZE, CELL_SIZE)) 
            self.image.fill((250,249,247))
            self.rect=pygame.Rect(a*GRID_SIZE*CELL_SIZE+x * CELL_SIZE,b*GRID_SIZE*CELL_SIZE+ y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        elif cell==3:
            self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))  
            self.image.fill((38,102,145))
            self.rect=pygame.Rect(a*GRID_SIZE*CELL_SIZE+x * CELL_SIZE,b*GRID_SIZE*CELL_SIZE+ y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        elif cell==4:
            self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))  
            self.image.fill((248,240,164))
            self.rect=pygame.Rect(a*GRID_SIZE*CELL_SIZE+x * CELL_SIZE,b*GRID_SIZE*CELL_SIZE+ y * CELL_SIZE, CELL_SIZE, CELL_SIZE)    
        else:
            self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))  
            self.image.fill((86,125,70))
            self.rect=pygame.Rect(a*GRID_SIZE*CELL_SIZE+x * CELL_SIZE,b*GRID_SIZE*CELL_SIZE+ y * CELL_SIZE, CELL_SIZE, CELL_SIZE)  


class Enemies(pygame.sprite.Sprite):

    def __init__(self, enemy_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.update_time=pygame.time.get_ticks()

        self.enemy_type=enemy_type
        self.x=x
        self.y=y

        self.speed=pygame.math.Vector2(1)
        self.moving_left=False
        self.moving_right=False
        self.dx=0

        self.health=True
        self.max_hp=100
        self.attacking=False
        self.direction=1
        self.flip=False

        self.move_counter=0
        self.stopped=False
        self.stop_counter=0

        self.animation_list=[]
        self.frame_index=0
        self.action=0
        self.scale=1.2
        animations=['idle','walking']
        for animation in animations:
            temp_list=[]
            frames=len(os.listdir(f'{self.enemy_type} {animation}'))
            for i in range(frames):
                img=pygame.image.load(f'{self.enemy_type} {animation}/{animation}{i}.png').convert_alpha()
                img = img.subsurface(img.get_bounding_rect())
                original_width, original_height = img.get_size()
                new_width = int(original_width * (self.scale))
                new_height = int(original_height * (self.scale))
                img = pygame.transform.scale(img, (new_width, new_height))
                temp_list.append(img)
            self.animation_list.append(temp_list)  

        self.image=self.animation_list[self.frame_index][0]
        self.rect=self.image.get_rect(topleft=(self.x,self.y)) 

    def patrol(self,collideable_terrain, CELL_SIZE, GRID_SIZE, WORLD_SIZE):
        if self.health:
            if self.stopped==False and random.randint(1,500)==5:
                    self.stopped=True
                    self.stop_counter=0
            if self.stopped==False:
                if self.direction==1 :
                    self.moving_left=True
                    self.moving_right=False
                else:
                    self.moving_left=False
                    self.moving_right=True

                self.movement(collideable_terrain, CELL_SIZE, GRID_SIZE, WORLD_SIZE)
                self.update_action(1)
                self.move_counter+=1

                if self.move_counter>CELL_SIZE*4:
                    self.direction*=-1
                    self.move_counter*=-1
            else:
                self.moving_left=False
                self.moving_right=True
                self.update_action(0)
                self.stop_counter+=1
                if self.stop_counter>200:
                    self.stopped=False        

    def movement(self,collideable_terrain, CELL_SIZE, GRID_SIZE, WORLD_SIZE):

        self.dx=0
        self.dy=0 

        if self.moving_left:
            self.dx=-self.speed.x
            self.flip=False
            self.direction=1
        
        if self.moving_right:
            self.dx=self.speed.x
            self.flip=True
            self.direction=-1
        
        if self.attacking:
            self.attacking=True     


        self.rect.x+=self.dx
        self.handle_collisions(collideable_terrain, CELL_SIZE, GRID_SIZE, WORLD_SIZE)

    def handle_collisions(self, collideable_terrain, CELL_SIZE, GRID_SIZE, WORLD_SIZE):
        for tile in collideable_terrain:
            if self.rect.colliderect(tile.rect):  
                if self.moving_right:
                    self.rect.x-=self.dx
                    self.stopped=True
                    self.direction*=-1
                if self.moving_left:
                    self.rect.x-=self.dx
                    self.stopped=True
                    self.direction*=-1
        if self.rect.x<0 or self.rect.x>CELL_SIZE*GRID_SIZE*WORLD_SIZE-self.rect.width:
            self.rect.x-=self.dx
        if self.rect.y<0 or self.rect.y>CELL_SIZE*GRID_SIZE*WORLD_SIZE-self.rect.height:
            self.rect.y-=self.dy    

    def update_action(self, new_action):
        if new_action != self.action:
            self.action=new_action
            self.frame_index=0
            self.update_time=pygame.time.get_ticks()
        else:
            self.action=self.action
    
    def update_animation(self):
        ANIMATION_COOLDOWN=150
        if pygame.time.get_ticks()-self.update_time>ANIMATION_COOLDOWN:
            self.update_time=pygame.time.get_ticks()
            self.frame_index+=1
        if self.frame_index> len(self.animation_list[self.action])-1:    
            if self.attacking:
                self.attacking=False
            if self.action == 3: 
                self.frame_index = len(self.animation_list[self.action]) - 1 
            else:
                self.frame_index = 0  
        self.image=self.animation_list[self.action][self.frame_index]    

    def draw(self, screen, camera_x, camera_y):
        screen.blit(pygame.transform.flip(self.image, self.flip, False),(self.rect.x + camera_x, self.rect.y + camera_y))
        #pygame.draw.rect(screen, (255, 0, 0), self.rect.move(camera_x, camera_y), 2) 


