"""
Basket: the player-controlled catcher at the bottom of the screen.
"""

import pygame


class Basket:
    def __init__(self, x, y, width=90, height=24, speed=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

        self.boosted_frames = 0
        self.normal_speed = speed
        self.boost_speed = 10

    def activate_boost(self, duration_frames):
        if self.boosted_frames > 0:
            return

        self.boosted_frames = duration_frames
        self.speed = self.boost_speed

    def update_boost(self):
        if self.boosted_frames > 0:
            self.boosted_frames -= 1

            if self.boosted_frames == 0:
                self.speed = self.normal_speed

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2),
            int(self.y - self.height / 2),
            self.width,
            self.height,
        )