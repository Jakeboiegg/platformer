import pygame
from classes import Screen, Colour, Images, Player, Floor, Objective, Platform
import check
import levels
import draw

pygame.init()


# initialise screen
screen_dimensions = Screen()
screen = pygame.display.set_mode((screen_dimensions.width, screen_dimensions.height))
pygame.display.set_caption("Belvis go jumpy wooo")

colour = Colour()
images = Images()
floor = Floor(screen_dimensions, 30)

time = 0
clock = pygame.time.Clock()
FPS = 60

level = 1
change_level = False
level_font = pygame.font.Font("Rubik.ttf", 300)
time_font = pygame.font.Font("Rubik.ttf", 75)

platforms = []
player = Player(1000, -500)  # to not make the player touch the objective
objective = Objective(0, -300)

short = False

levels = {
    1: {"format": levels.tutorial, "image": images.dog},
    2: {"format": levels.stairs1, "image": images.can},
    3: {"format": levels.stairs2, "image": images.calculator},
    4: {"format": levels.jump1, "image": images.fan},
    5: {"format": levels.jump2, "image": images.cube},
    6: {"format": levels.jump3, "image": images.miku},
    7: {"format": levels.runup1, "image": images.calculator},
    8: {"format": levels.runup2, "image": images.calculator},
    9: {"format": levels.climb1, "image": images.cube},
    10: {"format": levels.end, "image": images.calculator},
}


def init_platforms_position(format):
    platforms = []

    for row_number, row in enumerate(format):
        for column_number, editor_chr in list(enumerate(row)):
            if editor_chr == "x":
                platforms.append(Platform(column_number * 20, row_number * 40))

    return platforms


def updateScreen():
    screen.fill(colour.background)

    if not check.is_end(level, levels):
        draw.level_text(screen, level, level_font, screen_dimensions, colour)
    elif check.is_end(level, levels):
        draw.level_text(screen, "end", level_font, screen_dimensions, colour)
    draw.time(screen, time, time_font, colour)

    floor.draw(screen, screen_dimensions, colour)
    objective.draw(screen, levels[level]["image"], colour)
    player.draw(short, screen, images)
    draw.platform(screen, platforms, colour)

    pygame.display.flip()
    pygame.display.update()


def main():
    global change_level, level, platforms, time, short

    format = levels[level]["format"]
    player.init_position(format)
    objective.init_position(format)
    platforms = init_platforms_position(format)

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if change_level and check.touchingObective(player, objective):
            platforms = []
            level += 1

            format = levels[level]["format"]
            player.init_position(format)
            objective.init_position(format)
            platforms = init_platforms_position(format)
            change_level = False

        keys = pygame.key.get_pressed()
        if (
            keys[pygame.K_SPACE]
            and not player.is_jump
            and (
                check.onFloor(player, floor, screen_dimensions)
                or check.onPlatform(platforms, player)
            )
        ):
            player.is_jump = True

        if keys[pygame.K_DOWN] or keys[pygame.K_LSHIFT]:
            short = True
        else:
            short = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.move("left", short, screen_dimensions)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_e]:
            player.move("right", short, screen_dimensions)
        else:
            player.move("no_input", short, screen_dimensions)

        player.floorCollision(floor, screen_dimensions)
        player.platformCollision(platforms)

        objective.vibrate()

        touching_objective = check.touchingObective(player, objective)
        if touching_objective:
            change_level = True

        if not check.is_end(level, levels):
            time += 1

        updateScreen()

    pygame.quit()


if __name__ == "__main__":
    main()
