import pygame
from pygame.math import Vector2
import sys
from random import randint, choice
from math import sin, cos, atan2, radians, degrees, hypot


class Simulation:
    FPS = 60
    BALL_RADIUS = 15

    def __init__(self):
        self.screen = pygame.display.set_mode((1200, 700))
        self.clock = pygame.time.Clock()

        self.ball_group = pygame.sprite.Group()
        self.limit_bound = (self.screen.get_width(), self.screen.get_height())
        self.delta = 0

        self.font = pygame.font.SysFont(None, 50)
        self.angle = 0

        self.origin_pos = Vector2(0, self.limit_bound[1])

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                horizontal_distance = event.pos[0]
                vertical_distance = self.limit_bound[1] - event.pos[1]
                self.angle = degrees(atan2(vertical_distance, horizontal_distance))

            if event.type == pygame.MOUSEBUTTONUP:
                ball = Ball(self.origin_pos, self.BALL_RADIUS, 60, self.angle)
                self.ball_group.add(ball)

    def draw_line(self):
        pygame.draw.line(self.screen, "white", self.origin_pos, pygame.mouse.get_pos())

    def run(self):
        while True:
            self.delta = self.clock.tick(self.FPS)
            self.handle_event()
            self.screen.fill((0, 0, 0))

            angle = self.font.render(f"{self.angle}", True, "white")
            self.screen.blit(angle, (0, 0))

            self.draw_line()
            self.ball_group.update(self.screen, self.limit_bound, self.delta)
            self.ball_group.draw(self.screen)

            pygame.display.update()


import pygame
import math


class Ball(pygame.sprite.Sprite):
    GRAVITY = 10

    def __init__(self, pos: tuple[int, int], radius: int, speed: int, degree: float):
        super().__init__()
        self.image = pygame.Surface((radius * 2, radius * 2))
        pos = pos[0], pos[1] - radius * 2
        self.rect = self.image.get_rect(center=pos)
        self.initial_position = Vector2(pos)
        self.direction = 1
        self.radius = radius
        self.speed = speed
        self.angle = math.radians(degree)
        self.time = 0

    def update(
        self,
        display_surface: pygame.Surface,
        limit_bound: tuple[int, int],
        delta: float,
    ):
        if self.rect.x >= limit_bound[0] or self.rect.y >= limit_bound[1]:
            self.kill()

        self.time += delta / 100.0
        self.rect.y = self.initial_position.y - (
            self.speed * math.sin(self.angle) * self.time
            - 0.5 * self.GRAVITY * self.time**2
        )
        self.rect.x += self.direction * self.speed * math.cos(self.angle)
        pygame.draw.circle(
            self.image, (255, 0, 0), (self.radius, self.radius), self.radius
        )


def get_random_rgb() -> tuple[int, int]:
    return (randint(0, 255), randint(0, 255), randint(0, 255))


def main():
    pygame.init()
    pygame.font.init()

    simulation = Simulation()
    simulation.run()


if __name__ == "__main__":
    main()
