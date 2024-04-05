import pygame
from assets.classes import (
    Screen,
    Colour,
    Images,
    Player,
    Floor,
    Objective,
    Platform,
    Font,
)
from assets import check
from assets import levels
from assets import draw

pygame.init()


# initialise screen
screen_dimensions = Screen()
screen = pygame.display.set_mode((screen_dimensions.width, screen_dimensions.height))
pygame.display.set_caption("Belvis go jumpy wooo")

colour = Colour()
images = Images()
floor = Floor(screen_dimensions, 30)
font = Font()

clock = pygame.time.Clock()
FPS = 60

level = 1
change_level = False

time = 0
timer_active = False

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
    10: {"format": levels.stop1, "image": images.calculator},
    11: {"format": levels.stop2, "image": images.calculator},
    12: {"format": levels.end, "image": images.calculator},
}


def init_platforms_position(format):  # closed, but nowhere to put
    platforms = []

    for row_number, row in enumerate(format):
        for column_number, editor_chr in list(enumerate(row)):
            if editor_chr == "x":
                platforms.append(Platform(column_number * 20, row_number * 40))

    return platforms


def init_game_elements(format):  # not closed
    global platforms, change_level

    player.init_position(format)
    objective.init_position(format)
    platforms = init_platforms_position(format)
    change_level = False


def updateScreen():  # not closed
    screen.fill(colour.background)

    if not check.is_end(level, levels):
        draw.level_text(screen, level, font.level, screen_dimensions, colour)
    elif check.is_end(level, levels):
        draw.level_text(screen, "end", font.level, screen_dimensions, colour)
    draw.time(screen, time, timer_active, font.time, colour)

    floor.draw(screen, screen_dimensions, colour)
    objective.draw(screen, levels[level]["image"], colour)
    player.draw(short, screen, images)
    draw.platform(screen, platforms, colour)

    pygame.display.flip()
    pygame.display.update()


def main():
    global change_level, level, platforms, time, timer_active, short

    format = levels[level]["format"]
    init_game_elements(format)

    running = True
    while running:
        clock.tick(FPS)

        # quit button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # change levels
        if change_level and check.touchingObective(player, objective):
            platforms = []
            level += 1

            format = levels[level]["format"]
            init_game_elements(format)

        # player input
        keys = pygame.key.get_pressed()

        # jumping
        if (
            keys[pygame.K_SPACE]
            and not player.is_jump
            and (
                check.onFloor(player, floor, screen_dimensions)
                or check.onPlatform(platforms, player)
            )
        ):
            player.is_jump = True

        # shifting (short)
        if keys[pygame.K_DOWN] or keys[pygame.K_LSHIFT]:
            short = True
        else:
            short = False

        # left-right movement
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

        # start timer on first received input
        if time == 0 and (
            keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_SPACE]
        ):
            time = 1
            timer_active = True

        elif not check.is_end(level, levels) and time > 0:
            time += 1

        # restart when ; pressed
        if keys[pygame.K_SEMICOLON]:
            level = 1
            time = 0

            format = levels[level]["format"]
            init_game_elements(format)

        if keys[pygame.K_r]:
            format = levels[level]["format"]
            init_game_elements(format)

        updateScreen()

    pygame.quit()


if __name__ == "__main__":
    main()
