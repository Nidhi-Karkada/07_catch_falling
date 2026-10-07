"""
GameEngine: owns the basket and all falling objects.

Tasks 1-3:

- Catch detection requires actual overlap.
- Caught objects are removed safely.
- The basket stays fully inside the screen.
- Objects use controlled spawning.

Task 4:

- Space activates a temporary basket speed boost.
"""

import random
import pygame
from game.basket import Basket
from game.falling_object import FallingObject
from game.collision import is_caught
from game.renderer import WIDTH, HEIGHT


MIN_SPAWN_DELAY = 35
MAX_SPAWN_DELAY = 65
MIN_HORIZONTAL_SEPARATION = 100
MAX_ACTIVE_OBJECTS = 4
MAX_SPAWN_POSITION_ATTEMPTS = 20

BOOST_DURATION_FRAMES = 300

MAX_MISSES = 5


class GameEngine:
    def __init__(self):
        self.basket = Basket(x=WIDTH / 2, y=HEIGHT - 30)
        self.objects = []
        self.frames_until_spawn = 0
        self.last_spawn_x = None
        self.score = 0
        self.misses = 0
        self.game_over = False

    def _spawn_object(self):
        radius = 14
        min_x = radius
        max_x = WIDTH - radius

        best_x = None
        best_distance = -1

        for _ in range(MAX_SPAWN_POSITION_ATTEMPTS):
            x = random.randint(min_x, max_x)

            if self.last_spawn_x is None:
                best_x = x
                break

            distance = abs(x - self.last_spawn_x)

            if distance > best_distance:
                best_x = x
                best_distance = distance

            if distance >= MIN_HORIZONTAL_SEPARATION:
                best_x = x
                break

        self.objects.append(
            FallingObject(
                x=best_x,
                y=-radius,
                radius=radius,
                speed=3,
            )
        )

        self.last_spawn_x = best_x

    def handle_input(self, keys_pressed):
        if self.game_over:
            return

        if keys_pressed[pygame.K_LEFT]:
            self.basket.x -= self.basket.speed

        if keys_pressed[pygame.K_RIGHT]:
            self.basket.x += self.basket.speed

        half_width = self.basket.width / 2

        self.basket.x = max(
            half_width,
            min(WIDTH - half_width, self.basket.x)
        )

    def handle_keydown(self, key):
        if self.game_over:
            if key == pygame.K_r:
                self.__init__()
            return

        if key == pygame.K_SPACE:
            self.basket.activate_boost(BOOST_DURATION_FRAMES)

    def update(self):
        if self.game_over:
            return

        self.basket.update_boost()

        self.frames_until_spawn -= 1

        if self.frames_until_spawn <= 0:
            if len(self.objects) < MAX_ACTIVE_OBJECTS:
                self._spawn_object()

            self.frames_until_spawn = random.randint(
                MIN_SPAWN_DELAY,
                MAX_SPAWN_DELAY,
            )

        for obj in self.objects:
            obj.update()

        basket_rect = self.basket.get_rect()

        remaining_objects = []

        for obj in self.objects:
            if is_caught(basket_rect, obj):
                self.score += 1
            else:
                remaining_objects.append(obj)

        self.objects = remaining_objects

        missed = [
            o for o in self.objects
            if o.is_past_bottom(HEIGHT)
        ]

        if missed:
            self.objects = [
                o for o in self.objects
                if not o.is_past_bottom(HEIGHT)
            ]

            self.misses += len(missed)

            if self.misses >= MAX_MISSES:
                self.game_over = True

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(
            surface,
            self.basket,
            self.objects,
        )

        renderer.draw_text(
            surface,
            font,
            f"Score: {self.score}",
            (10, 10),
        )

        renderer.draw_text(
            surface,
            font,
            f"Misses: {self.misses}/{MAX_MISSES}",
            (10, 36),
        )

        if self.basket.boosted_frames > 0:
            remaining_seconds = (
                self.basket.boosted_frames + 59
            ) // 60

            renderer.draw_text(
                surface,
                font,
                f"BOOST ACTIVE: {remaining_seconds}s",
                (470, 10),
            )

        if self.game_over:
            renderer.draw_banner(
                surface,
                font,
                f"Game Over! Final score: {self.score}. Press R to restart.",
            )