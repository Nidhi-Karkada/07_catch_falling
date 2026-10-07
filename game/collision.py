"""
collision: figures out whether a falling object is within the basket.
"""
import pygame
def is_caught(basket_rect, obj):
    obj_rect = pygame.Rect(
        int(obj.x - obj.radius),
        int(obj.y - obj.radius),
        obj.radius * 2,
        obj.radius * 2,
)
    return obj_rect.colliderect(basket_rect)