import pygame
from classes import Screen, Colour, Images, Player, Floor, Objective, Platform
import check
import levels

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


def init_player_position(level):
    global levels
    o_count = 0
    player_initial_position = []

    for row_number, row in enumerate(levels[level]["format"]):
        for column_number, editor_chr in list(enumerate(row)):
            if editor_chr == "o":
                o_count += 1
                player_initial_position.append(column_number * 20)
                player_initial_position.append(row_number * 40)

    if o_count == 1:
        return player_initial_position
    else:
        return [0, -300]


def init_objective_position(level):
    global levels
    e_count = 0
    objective_initial_position = []

    for row_number, row in enumerate(levels[level]["format"]):
        for column_number, editor_chr in list(enumerate(row)):
            if editor_chr == "e":
                e_count += 1
                objective_initial_position.append(column_number * 20)
                objective_initial_position.append(row_number * 40)

    if e_count == 1:
        return objective_initial_position
    else:
        return [0, -500]


def init_platforms_position(level):
    global levels
    platforms = []

    for row_number, row in enumerate(levels[level]["format"]):
        for column_number, editor_chr in list(enumerate(row)):
            if editor_chr == "x":
                platforms.append(Platform(column_number * 20, row_number * 40))

    return platforms


def is_end(level):
    global levels

    if level == len(levels):
        return True
    else:
        return False


def updateLevel():
    global platforms, player, objective, level

    format = levels[level]["format"]

    player.init_position(format)
    objective.init_position(format)

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

    if not is_end(level):
        level_text_draw(level)
    elif is_end(level):
        level_text_draw("end")
    time_draw(time)

    floor.draw(screen, screen_dimensions, colour)
    objective.draw(screen, levels[level]["image"], colour)
    player.draw(short, screen, images)
    platform_draw()

    pygame.display.flip()
    pygame.display.update()


def main():
    updateLevel()
    running = True
    global change_level, level, platforms, time, short
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if change_level and check.touchingObective(player, objective):
            platforms = []
            level += 1
            updateLevel()
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

        if not is_end(level):
            time += 1

        updateScreen()

    pygame.quit()


if __name__ == "__main__":
    main()
