import pygame
from classes import Screen, Colour, Images, Player, Floor, Objective
from functions import (
    init_player_position,
    init_objective_position,
    init_platforms_position,
    floorCollision,
    onFloor,
    keepInWindow,
    platformCollision,
    onPlatform,
    touchingObective,
    vibrate,
    end,
)

pygame.init()


# initialise screen
screen_dimensions = Screen()
screen = pygame.display.set_mode((screen_dimensions.width, screen_dimensions.height))
pygame.display.set_caption("Basic Platformer")

colour = Colour()
images = Images()
floor = Floor(screen_dimensions.width, screen_dimensions.height, 30)

time = 0
clock = pygame.time.Clock()
FPS = 60

level = 0
change_level = True
level_font = pygame.font.Font("Rubik.ttf", 300)
time_font = pygame.font.Font("Rubik.ttf", 75)

platforms = []
player = Player(0, -500)  # to not make the player touch the objective
objective = Objective(0, -300)

short = False


def updateLevel():
    global platforms, player, objective, level
    player_position = init_player_position(level)
    objective_position = init_objective_position(level)

    player.x = player_position[0]
    player.y = player_position[1]

    objective.x = objective_position[0]
    objective.y = objective_position[1]
    objective.initialx = objective_position[0]
    objective.initialy = objective_position[1]

    platforms = init_platforms_position(level)


def level_text_draw(number):
    number = str(number)
    level_text_surface = level_font.render(number, True, colour.level_text)
    level_text_rect = level_text_surface.get_rect()
    screen.blit(
        level_text_surface,
        (
            (screen_dimensions.width / 2) - (level_text_rect.width / 2),
            (screen_dimensions.height / 2) - (level_text_rect.height / 2),
        ),
    )


def end_time_text_draw(number):
    number = int(number)

    minutes = time // 3600
    seconds = (time // 60) - (minutes * 60)

    if seconds < 10:
        time_formatted = f"{minutes}:0{seconds}"
    else:
        time_formatted = f"{minutes}:{seconds}"

    time_text_surface = time_font.render(time_formatted, True, colour.level_text)
    time_text_rect = time_text_surface.get_rect()
    screen.blit(
        time_text_surface,
        (
            (screen_dimensions.width / 2) - (time_text_rect.width / 2),
            (screen_dimensions.height / 2) - (time_text_rect.height / 2),
        ),
    )


def platform_draw():
    for platform in platforms:
        platform.draw(screen, colour)


def time_draw(time):
    time = int(time)
    minutes = time // 3600
    seconds = (time // 60) - (minutes * 60)

    if seconds < 10:
        time_formatted = f"{minutes}:0{seconds}"
    else:
        time_formatted = f"{minutes}:{seconds}"

    time_text_surface = time_font.render(time_formatted, True, colour.level_text)
    screen.blit(time_text_surface, (30, 30))


def updateScreen():
    global short
    screen.fill(colour.background)

    if not end(level):
        level_text_draw(level)
    elif end(level):
        level_text_draw("end")
    time_draw(time)

    floor.draw(screen, screen_dimensions, colour)
    objective.draw(screen, colour)
    player.draw(short, screen, images)
    platform_draw()

    pygame.display.flip()
    pygame.display.update()


def main():
    running = True
    global change_level, level, platforms, time, short
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if change_level:
            platforms = []
            level += 1
            updateLevel()
            change_level = False

        keys = pygame.key.get_pressed()
        if (
            keys[pygame.K_SPACE]
            and not player.is_jump
            and (
                onFloor(player, floor, screen_dimensions)
                or onPlatform(platforms, player)
            )
        ):
            player.is_jump = True

        if keys[pygame.K_DOWN] or keys[pygame.K_LSHIFT]:
            short = True
        else:
            short = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.move("left", short)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_e]:
            player.move("right", short)
        else:
            player.move("no_input", short)

        floorCollision(player, floor, screen_dimensions)
        keepInWindow(player, screen_dimensions)
        platformCollision(platforms, player)

        vibrate(objective, time)

        touching_objective = touchingObective(player, objective)
        if touching_objective:
            change_level = True

        if not end(level):
            time += 1

        updateScreen()

    pygame.quit()


if __name__ == "__main__":
    main()
