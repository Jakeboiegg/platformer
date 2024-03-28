import pygame

pygame.init()


class Colour:
    def __init__(self):
        self.background = (36, 39, 58)
        self.white = (202, 211, 245)
        self.sky = (145, 215, 227)
        self.red = (237, 135, 150)
        self.lavender = (183, 189, 248)


class Player:
    def __init__(self):
        self.x = (screen_width // 2) - 25
        self.y = (screen_height // 2) - 25
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

    def draw(self, screen):
        pygame.draw.rect(screen, colour.red, (self.x, self.y, self.width, self.height))

    def move(self, direction):
        # move left / right
        if direction == "left":
            self.velocity -= player.acceleration

        elif direction == "right":
            self.velocity += player.acceleration

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
        if self.velocity > player.max_speed:
            self.velocity = player.max_speed
        if self.velocity < player.max_speed * -1:
            self.velocity = player.max_speed * -1

        # update player position
        self.x += player.velocity

        # keep player in the window
        if self.x < 0:
            self.x = 0
        if self.x > screen_width - self.width:
            self.x = screen_width - self.width

        # gravity
        self.y += self.gravity

        # floor collision
        bottom_player = self.y + self.height
        top_floor = screen_height - floor.height

        if bottom_player > top_floor:
            self.y = top_floor - self.height


class Floor:
    def __init__(self, screen_width, screen_height, height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.height = height

    def draw(self, screen):
        x = 0
        y = screen_height - self.height
        pygame.draw.rect(screen, colour.sky, (x, y, self.screen_width, self.height))


class Platform:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 150
        self.height = 10

    def draw(self, screen):
        pygame.draw.rect(
            screen, colour.lavender, (self.x, self.y, self.width, self.height)
        )


screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Basic Platformer")

colour = Colour()
floor = Floor(screen_width, screen_height, 30)
player = Player()
platforms = [
    Platform(80, 470),
    Platform(325, 420),
    Platform(570, 470),
]
font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()
FPS = 60


def updateScreen():
    screen.fill(colour.background)
    player.draw(screen)
    floor.draw(screen)
    for platform in platforms:
        platform.draw(screen)
    pygame.display.flip()
    pygame.display.update()


def floorCollision():
    if player.y + player.height >= screen_height - floor.height:
        player.y = screen_height - floor.height - player.height


def onFloor():
    if player.y + player.height >= screen_height - floor.height:
        return True
    else:
        return False


def platformCollision():
    for platform in platforms:
        player_left = player.x
        player_right = player.x + player.width
        platform_left = platform.x
        platform_right = platform.x + platform.width
        platform_top = platform.y
        player_bottom = player.y + player.height
        if (
            platform_top <= player_bottom <= platform_top + player.gravity
            and player_left <= platform_right
            and player_right >= platform_left
        ):
            player.y = platform.y - player.height


def onPlatform():
    for platform in platforms:
        player_left = player.x
        player_right = player.x + player.width
        platform_left = platform.x
        platform_right = platform.x + platform.width
        platform_top = platform.y
        player_bottom = player.y + player.height
        if (
            platform_top <= player_bottom <= platform_top + player.gravity
            and player_left <= platform_right
            and player_right >= platform_left
        ):
            return True
    return False


running = True
while running:
    clock.tick(FPS)
    player.bottom = {"x": player.x + (player.width / 2), "y": player.y + player.height}

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not player.is_jump and (onFloor() or onPlatform()):
        player.is_jump = True

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.move("left")
    elif keys[pygame.K_RIGHT] or keys[pygame.K_e]:
        player.move("right")
    else:
        player.move("no_input")

    floorCollision()
    platformCollision()
    updateScreen()

pygame.quit()
