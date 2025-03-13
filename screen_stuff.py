import pygame
import sys
from perlin_noise import PerlinNoise
from sprites import *
import random

WIDTH, HEIGHT= 1080, 600
WORLD_SIZE=2
GRID_SIZE = 60
CELL_SIZE = WIDTH // GRID_SIZE

def generate_dungeon(level):
        ##each chunk is procedurally generated using perlin noise##
        seed=random.randint(0,10000)
        noise1=PerlinNoise(2,seed)
        noise2=PerlinNoise(4,seed)
        noise3=PerlinNoise(8,seed)
        dungeon=[]
        for y in range (GRID_SIZE):
            row=[]
            for x in range (GRID_SIZE):
                tile=noise1((x/GRID_SIZE, y/GRID_SIZE))
                tile+=noise2((x/GRID_SIZE, y/GRID_SIZE))*0.5
                tile+=noise3((x/GRID_SIZE, y/GRID_SIZE))*0.25
                if tile>-0.2 and tile<0.15 or tile>0.45 and tile<0.6:
                    spawn_chance = max(3000 - (level * 50), 500)
                    if random.randint(1,spawn_chance)==2:
                        if random.randint(1,2)==1:
                             row.append(5)#food
                        else:
                             row.append(6)#medkit
                    else:          
                        row.append(0)#ground
                elif tile<-0.4:
                    row.append(2)#snow
                elif tile>0.2 and tile<0.45:
                    row.append(3)#water  
                elif tile>0.15 and tile<0.2:
                    row.append(4)  #sand
                elif tile<-0.2 and tile>-0.4 or tile>0.6:
                    row.append(1)#stone   
            dungeon.append(row) 
        return dungeon ##stored as a 2d list##

def generate_world(world,level):
        world.clear()
        ##world is certain chunkxchunk##
        for y in range(WORLD_SIZE):
            row=[]
            for x in range(WORLD_SIZE):
                row.append(generate_dungeon(level))
            world.append(row) 
        return world    
    
    
def draw_dungeon(world,all_terrain_group,all_sprites,collideable_terrain,consumable_group):
        ##drawing world and ading blocks to appopirted groups##
        for b in range(WORLD_SIZE):
            for a in range(WORLD_SIZE):
                dungeon=world[a][b]
                for y, row in enumerate(dungeon):
                    for x, cell in enumerate(row):
                        terrain=Block(x,y,cell,CELL_SIZE,a,b,GRID_SIZE)
                        all_terrain_group.add(terrain)
                        all_sprites.add(terrain)

                        if cell==1 or cell==2 :
                            collideable_terrain.add(terrain)
                        elif cell==5 or cell==6:
                             consumable_group.add(terrain)


def random_spawn(world):
        ##randomly spawning player somehwre in the world on grass##
        spawn_x, spawn_y = None, None
        a=random.randint(0,1)
        b=random.randint(0,1)
        chunk_x_offset=a*GRID_SIZE*CELL_SIZE
        chunk_y_offset=b*GRID_SIZE*CELL_SIZE
        dungeon=world[a][b]
        spawn_found=False
        while not spawn_found:
            x=random.randint(0,GRID_SIZE-1)
            y=random.randint(0,GRID_SIZE-1)
            cell=dungeon[x][y]
            if cell == 0:  
                spawn_x = x * CELL_SIZE+chunk_x_offset
                spawn_y = y * CELL_SIZE+chunk_y_offset
                spawn_found=True
            else:
                spawn_found=False 
        return spawn_x, spawn_y   

def enemy_random_spawn(num_enemies,enemy_type,collideable_terrain,enemy_group,all_sprites):
        ##scattering enemies throughout the owrld##
        for i in range(0,num_enemies+3):
            spawn_x, spawn_y = None, None
            a=random.randint(0,1)
            b=random.randint(0,1)
            chunk_x_offset=a*GRID_SIZE*CELL_SIZE
            chunk_y_offset=b*GRID_SIZE*CELL_SIZE
            spawn_found=False
            attempts=0
            while not spawn_found and attempts<21:
                attempts+=1
                x=random.randint(0,GRID_SIZE-1)
                y=random.randint(0,GRID_SIZE-1)
                spawn_x = x * CELL_SIZE+chunk_x_offset
                spawn_y = y * CELL_SIZE+chunk_y_offset
                enemy=Enemies(enemy_type,spawn_x, spawn_y)
                collision = False  
                ##preventing from spawing on rocks and water##
                for block in collideable_terrain:
                    if enemy.rect.colliderect(block.rect) or block.cell==3 :
                        collision = True 
                        break  
            
                if not collision:  
                    enemy_group.add(enemy)
                    all_sprites.add(enemy)
                    spawn_found = True
                else:
                    enemy.kill() 

def boss_random_spawn(level,enemy_type,collideable_terrain,enemy_group,all_sprites):
        ##randomly spawing the boss somehwre in the owrld very 10th level##
        for i in range(0,int(level/10)):
            spawn_x, spawn_y = None, None
            a=random.randint(0,1)
            b=random.randint(0,1)
            chunk_x_offset=a*GRID_SIZE*CELL_SIZE
            chunk_y_offset=b*GRID_SIZE*CELL_SIZE
            spawn_found=False
            attempts=0
            while not spawn_found and attempts<21:
                attempts+=1
                x=random.randint(0,GRID_SIZE-1)
                y=random.randint(0,GRID_SIZE-1)
                spawn_x = x * CELL_SIZE+chunk_x_offset
                spawn_y = y * CELL_SIZE+chunk_y_offset
                enemy=Enemies(enemy_type,spawn_x, spawn_y)
                collision = False  
                for block in collideable_terrain:
                    if enemy.rect.colliderect(block.rect) or block.cell==3 :
                        collision = True 
                        break  
            
                if not collision:  
                    enemy_group.add(enemy)
                    all_sprites.add(enemy)
                    spawn_found = True
                else:
                    enemy.kill() 

def draw_healthbar(SCREEN,player):
        ratio=player.hp/player.max_hp
        pygame.draw.rect(SCREEN,(0,0,0),(10, 10, 300, 40))
        pygame.draw.rect(SCREEN,(255,0,0),(10, 10, 295, 35))
        pygame.draw.rect(SCREEN,(0,255,0),(10, 10, ratio*295, 35)) 

def draw_hungerbar(SCREEN,player):
        ratio=player.stamina/player.max_stamina
        pygame.draw.rect(SCREEN,(0,0,0),(10, 60, 300, 40))
        pygame.draw.rect(SCREEN,(211,211,211),(10, 60, 295, 35))
        pygame.draw.rect(SCREEN,(128,84,47),(10, 60, ratio*295, 35))   

def draw_haki_counter(SCREEN,player):
        current_time = pygame.time.get_ticks()
        time_since_haki = current_time - player.last_haki_time
        
        if time_since_haki < player.haki_cooldown:
            ratio = time_since_haki / player.haki_cooldown
        else:
            ratio = 1
        pygame.draw.rect(SCREEN,(0,0,0),(10, 110, 300, 7))
        pygame.draw.rect(SCREEN,(211,211,211),(10, 110, 297, 5))
        pygame.draw.rect(SCREEN,(255,0,0),(10, 110, ratio*297, 5))          

def draw_score(SCREEN, bounty,font,highscore):
    text_surface_1 = font.render(f"P.B.: ${highscore}", True, (255,165,0))   
    text_rect_1 = text_surface_1.get_rect(topright=(WIDTH-10 , 10))
    SCREEN.blit(text_surface_1, text_rect_1)

    text_surface_2 = font.render(f"BOUNTY: ${bounty}", True, (255,165,0))   
    text_rect_2 = text_surface_2.get_rect(topright=(WIDTH-10 , 60))
    SCREEN.blit(text_surface_2, text_rect_2)

def error_message(SCREEN,font,result):
        ##all the error  message for register##
        if result==1:
            message='Missing Fields'
        elif result==2:
            message='Username Taken' 
        elif result==3:
            message='Username has to be atleast 5 characters'
        elif result==4:
            message='Password has to be atleast 5 characters'  
        elif result==5:
            message='Password must contain atleast 1 number'  
        elif result==6:
            message='Password must contain upper and lowercase' 
        elif result==7:
            message='Username and Password do not match'
        elif result==8:
            message='Key bind is set for another key'              
        text_surface = font.render(message, True, (255,0,0))   
        text_rect = text_surface.get_rect(midtop=(WIDTH//2 , 200))
        SCREEN.blit(text_surface, text_rect)
        pygame.display.update()

def sort_score(highscores:list,score):
    ##insertion sort to sort scores in descing order##
    ## and poping 6th highscore so only 5 kept##
    highscores.append(score)
    for i in range (1,len(highscores)):
        check=highscores[i]
        pos=i
        while pos>0 and highscores[pos-1]<check:
            highscores[pos]=highscores[pos-1]
            pos-=1
        highscores[pos]=check
    highscores.pop()
    return highscores    