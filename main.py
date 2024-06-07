import pygame
from pygame.math import Vector2
import sys
from random import randint, choice
from math import sin, cos, atan2, radians, degrees, hypot

SCREEN_COLOR = (100, 100, 100)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


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

        self.origin_pos = Vector2(0, self.limit_bound[1] - 200)

        # text input
        self.input_field = pygame.Surface((250, 50), pygame.SRCALPHA)
        self.input_field.fill(BLACK)
        self.input_field_rect = self.input_field.get_rect(
            topright=(self.limit_bound[0], 0)
        )
        self.input_active = False

        self.velocity_text = ""
        self.velocity = 0

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                direction = 1
                if event.pos[1] > self.origin_pos[1]:
                    direction = -1
                horizontal_distance = event.pos[0]
                vertical_distance = self.limit_bound[1] - event.pos[1]
                self.angle = direction * degrees(
                    atan2(vertical_distance, horizontal_distance)
                )
            if event.type == pygame.MOUSEBUTTONUP and not self.input_active:
                ball = Ball(
                    self.origin_pos,
                    self.BALL_RADIUS,
                    self.velocity,
                    self.angle,
                )
                self.ball_group.add(ball)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_field_rect.collidepoint(event.pos):
                    self.input_active = True
                    self.velocity_text = ""
                    self.input_field.fill(BLACK)
                else:
                    self.input_active = False
                    self.velocity = int(self.velocity_text) if self.velocity_text else 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.input_active = False
                    if self.velocity_text:
                        try:
                            self.velocity = int(self.velocity_text)
                        except ValueError:
                            print("Invalid velocity input!")
                    else:
                        print("Please enter a velocity value!")

                if event.key == pygame.K_BACKSPACE:
                    self.velocity_text = self.velocity_text[:-1]

                if str(event.unicode).isnumeric() and self.input_active:
                    if self.velocity_text == "0":
                        self.velocity_text = ""
                    self.velocity_text += str(event.unicode)

    def text_input(self, char: str):
        pass

    def draw_line(self):
        pygame.draw.line(self.screen, WHITE, self.origin_pos, pygame.mouse.get_pos())

    def run(self):
        while True:
            self.delta = self.clock.tick(self.FPS)
            self.handle_event()
            self.screen.fill(SCREEN_COLOR)
            self.input_field.fill(BLACK)

            angle = self.font.render(f"{self.angle}", True, WHITE)
            self.screen.blit(angle, (0, 0))
            self.input_field.blit(
                self.font.render(self.velocity_text, True, WHITE), (0, 0)
            )

            if not self.input_active:
                self.draw_line()
            self.ball_group.update(self.screen, self.limit_bound, self.delta)
            self.ball_group.draw(self.screen)

            self.screen.blit(self.input_field, self.input_field_rect.topleft)

            pygame.display.update()


class Ball(pygame.sprite.Sprite):
    GRAVITY = 10

    def __init__(self, pos: tuple[int, int], radius: int, speed: int, degree: float):
        super().__init__()
        self.image = pygame.Surface((radius * 2, radius * 2))
        self.image.fill(SCREEN_COLOR)
        pos = pos[0], pos[1] - radius
        self.rect = self.image.get_rect(center=pos)
        self.initial_position = Vector2(pos)
        self.direction = 1
        self.radius = radius
        self.speed = speed
        self.angle = radians(degree)
        self.time = 0
        self.color = get_random_rgb()

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
            self.speed * sin(self.angle) * self.time - 0.5 * self.GRAVITY * self.time**2
        )
        self.rect.x += self.direction * self.speed * cos(self.angle)

        pygame.draw.circle(
            self.image, self.color, (self.radius, self.radius), self.radius
        )
        pygame.draw.circle(
            self.image, (0, 0, 0), (self.radius, self.radius), self.radius, 5
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
