import pygame
class Button():
    def __init__(self, image, pos, hov_image):
        self.image=pygame.image.load(image)
        self.hov_image=pygame.image.load(hov_image)
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
            self.image=self.image

class Textbox():
    def __init__(self, width, height, pos, font, text_colour, active_colour, inactive_colour, placeholder_text):
        self.rect= pygame.Rect(pos, width, height)
        self.x=pos[0]
        self.y=pos[1]
        self.font=pygame.font.Font(font,22)
        self.text_colour=text_colour
        self.active_colour=active_colour
        self.inactive_colour=inactive_colour
        self.colour=self.inactive_colour
        self.active=False
        self.placeholder_text=placeholder_text
        self.text=''
        self.show_placeholder=True

    def draw(self, screen):
        if self.show_placeholder:
            display_text= self.placeholder_text
        else:
            display_text=self.text
        if not self.show_placeholder:
            text_surface=self.font.render(display_text, True, self.text_colour)
        else:
            text_surface=self.font.render(display_text, True, self.colour)
        pygame.draw.rect(screen, self.colour, self.rect, 2)  
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))  

    def handle_text(self, event):
        if event.type==pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active=True
                self.show_placeholder=False
            else:
                self.active=False
            if self.active:
                self.colour=self.active_colour
            else:
                self.colour=self.inactive_colour

        if event.type==pygame.KEYDOWN and self.active:
            if event.key==pygame.K_BACKSPACE:
                self.text=self.text[:-1]
            else:
                self.text+= event.unicode    

    def get_text(self):
        return self.text            