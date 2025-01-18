import pygame
class Button():
    def __init__(self, image, pos, hov_image):
        self.base_image=pygame.image.load(image)
        self.hov_image=pygame.image.load(hov_image)
        self.image=self.base_image
        self.x=pos[0]
        self.y=pos[1]
        self.rect=self.image.get_rect(center=(self.x, self.y))


    def update(self, screen):
        screen.blit(self.image, self.rect)

    def check_input(self, mouse_position):
        if mouse_position[0] in range(self.rect.left, self.rect.right) and mouse_position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def change_image(self, mouse_position):
        if mouse_position[0] in range(self.rect.left, self.rect.right) and mouse_position[1] in range(self.rect.top, self.rect.bottom):
            self.image=self.hov_image
        else:
            self.image=self.base_image

class Textbox():
    def __init__(self, width, height, pos, placeholder_text):
        self.x=pos[0]
        self.y=pos[1]
        self.rect= pygame.Rect(self.x, self.y, width, height)
        self.font=pygame.font.SysFont('Arial',22)
        self.text_colour=(0,0,0)
        self.active_colour=(135, 206, 235)
        self.inactive_colour=(128, 128, 128)
        self.colour=self.inactive_colour
        self.active=False
        self.placeholder_text=placeholder_text
        self.text=''
        self.show_placeholder=True
        self.placeholder_colour=(192, 192, 192)

    def draw(self, screen):
        if self.text=='':
            display_text= self.placeholder_text
            text_surface=self.font.render(display_text, True, self.placeholder_colour)
        else:
            display_text=self.text
            text_surface=self.font.render(display_text, True, self.text_colour)
        pygame.draw.rect(screen, self.colour, self.rect, 2)  
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))  

    def handle_text(self, event):
        if event.type==pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active=True
                self.show_placeholder=False
                pygame.key.set_repeat(500,200)
            else:
                self.active=False
                pygame.key.set_repeat()

            if self.active:
                self.colour=self.active_colour
            else:
                self.colour=self.inactive_colour

        if event.type==pygame.KEYDOWN and self.active:
            if (event.key==pygame.K_BACKSPACE) and self.text:
                self.text=self.text[:-1]
            elif not (event.key==pygame.K_BACKSPACE) and self.text:
                self.text+= event.unicode       
        

    def get_text(self):
        input=self.text
        self.text=self.placeholder_text
        return input
        