import pygame
import level_formats

pygame.init()


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

    def draw(self, screen):
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

        rect = pygame.rect.Rect((self.x, self.y, 60, 60))
        screen.blit(image, rect)

    def move(self, direction):
        self.bottom = {
            "x": player.x + (player.width / 2),
            "y": player.y + player.height,
        }

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
        self.width = 30
        self.height = 10

    def draw(self, screen):
        pygame.draw.rect(
            screen, colour.lavender, (self.x, self.y, self.width, self.height)
        )


class Objective:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = 60
        self.width = 60

    def draw(self, screen):
        pygame.draw.rect(
            screen, colour.green, (self.x, self.y, self.width, self.height)
        )


screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Basic Platformer")

colour = Colour()
images = Images()
floor = Floor(screen_width, screen_height, 30)

platforms = []  # 40 x 15 , 800 x 600, 1 = 20, 1 = 30
o_count = 0
player_initial_position = []
e_count = 0
objective_initial_position = []

for row_number, row in enumerate(level_formats.level1):
    for column_number, editor_chr in list(enumerate(row)):
        if editor_chr == "o":
            o_count += 1
            player_initial_position.append(column_number)
            player_initial_position.append(row_number)
        if editor_chr == "x":
            platforms.append(Platform(column_number * 20, row_number * 40))
        if editor_chr == "e":
            e_count += 1
            objective_initial_position.append(column_number)
            objective_initial_position.append(row_number)

if o_count == 1:
    player = Player(player_initial_position[0] * 20, player_initial_position[1] * 40)
else:
    print("""
    invalid character placement
    """)
    player = Player(screen_width / 2, 0)
    player.x -= player.width / 2

if e_count == 1:
    objective = Objective(
        objective_initial_position[0] * 20, objective_initial_position[1] * 40
    )
else:
    print("""
    invalid objective placement
    """)
    objective = Objective(screen_width / 2, screen_height - floor.height)
    objective.x -= objective.width / 2

level_font = pygame.font.Font("Rubik.ttf", 300)
level_text_surface = level_font.render("1", True, colour.level_text)
level_text_rect = level_text_surface.get_rect()

clock = pygame.time.Clock()
FPS = 60


def updateScreen():
    screen.fill(colour.background)
    screen.blit(
        level_text_surface,
        (
            (screen_width / 2) - (level_text_rect.width / 2),
            (screen_height / 2) - (level_text_rect.height / 2),
        ),
    )
    floor.draw(screen)
    objective.draw(screen)
    player.draw(screen)
    for platform in platforms:
        platform.draw(screen)
    pygame.display.flip()
    pygame.display.update()


def floorCollision():
    if onFloor():
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


def main():
    running = True
    while running:
        clock.tick(FPS)

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


if __name__ == "__main__":
    main()
