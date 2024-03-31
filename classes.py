import pygame


class Screen:
    def __init__(self):
        self.width = 800
        self.height = 600


class Colour:
    def __init__(self):
        self.background = (36, 39, 58)
        self.white = (202, 211, 245)
        self.sky = (145, 215, 227)
        self.red = (237, 135, 150)
        self.green = (166, 218, 149)
        self.lavender = (183, 189, 248)
        self.level_text = (73, 77, 100)


class Images:
    def __init__(self):
        self.left = pygame.image.load("images/left.png").convert_alpha()
        self.left_jump = pygame.image.load("images/left_jump.png").convert_alpha()
        self.right = pygame.image.load("images/right.png").convert_alpha()
        self.right_jump = pygame.image.load("images/right_jump.png").convert_alpha()
        self.idle = pygame.image.load("images/idle.png").convert_alpha()
        self.idle_jump = pygame.image.load("images/idle_jump.png").convert_alpha()


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 60

        self.bottom = {"x": self.x + (self.width / 2), "y": self.y + self.height}

        self.acceleration = 0.5
        self.velocity = 0
        self.speed_decay = 1
        self.max_speed = 12
        self.gravity = 14

        self.jump_power = 25
        self.is_jump = False
        self.jump_count = 0

    def draw(self, screen, images):
        facing = "idle"
        if self.velocity == 0:
            facing = "idle"
        elif self.velocity < 0:
            facing = "left"
        elif self.velocity > 0:
            facing = "right"

        image = images.idle
        if facing == "idle" and not self.is_jump:
            image = images.idle
        elif facing == "idle" and self.is_jump:
            image = images.idle_jump

        elif facing == "left" and not self.is_jump:
            image = images.left
        elif facing == "left" and self.is_jump:
            image = images.left_jump

        elif facing == "right" and not self.is_jump:
            image = images.right
        elif facing == "right" and self.is_jump:
            image = images.right_jump

        rect = pygame.rect.Rect((self.x, self.y, self.width, self.height))
        screen.blit(image, rect)

    def move(self, direction):
        self.bottom = {
            "x": self.x + (self.width / 2),
            "y": self.y + self.height,
        }

        # move left / right
        if direction == "left":
            self.velocity -= self.acceleration

        elif direction == "right":
            self.velocity += self.acceleration

        else:
            # speed_decay when no input
            if self.velocity > 0:
                if (self.velocity - self.speed_decay) < 0:
                    self.velocity = 0
                else:
                    self.velocity -= self.speed_decay

            if self.velocity < 0:
                if (self.velocity + self.speed_decay) > 0:
                    self.velocity = 0
                else:
                    self.velocity += self.speed_decay

        # jummping
        if self.is_jump:
            self.y -= self.jump_power
            self.jump_count += 1
            if self.jump_count == 9:
                self.is_jump = False
                self.jump_count = 0

        # set the max speed
        if self.velocity > self.max_speed:
            self.velocity = self.max_speed
        if self.velocity < self.max_speed * -1:
            self.velocity = self.max_speed * -1

        # update self position
        self.x += self.velocity

        # gravity
        self.y += self.gravity


class Floor:
    def __init__(self, screen_width, screen_height, height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.height = height

    def draw(self, screen, screen_dimensions, colour):
        x = 0
        y = screen_dimensions.height - self.height
        pygame.draw.rect(screen, colour.sky, (x, y, self.screen_width, self.height))


class Platform:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 10

    def draw(self, screen, colour):
        pygame.draw.rect(
            screen, colour.lavender, (self.x, self.y, self.width, self.height)
        )


class Objective:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.initialx = x
        self.initialy = y
        self.height = 60
        self.width = 60

    def draw(self, screen, colour):
        pygame.draw.rect(
            screen, colour.green, (self.x, self.y, self.width, self.height)
        )
