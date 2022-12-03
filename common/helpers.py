import pygame


def draw_text(text, color, surface, x, y, text_size=30):
    font = pygame.font.SysFont(None, text_size)
    obj = font.render(text, True, color)
    rect = obj.get_rect()
    rect.topleft = (x, y)
    surface.blit(obj, rect)


def new_button(screen: pygame.Surface, position: tuple, size: tuple, picture: str = None, color: tuple = None):
    button = pygame.Rect(*position, *size)
    if color:
        pygame.draw.rect(screen, color, button, 0, 2)
    if picture:
        screen.blit(pygame.image.load(picture), position)
    return button
