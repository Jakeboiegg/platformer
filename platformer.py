import pygame
import random
import json
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
end_text = None

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


def format_time(time):  # closed
    time = int(time)
    minutes = time // 3600
    seconds = (time // 60) - (minutes * 60)
    milliseconds = (time // (60 / 100)) - (seconds * 100) - (minutes * 60 * 100)
    milliseconds = int(milliseconds)

    if seconds < 10 and milliseconds < 10:
        time_formatted = f"{minutes}:0{seconds}.0{milliseconds}"
    elif seconds < 10 and milliseconds >= 10:
        time_formatted = f"{minutes}:0{seconds}.{milliseconds}"
    elif seconds >= 10 and milliseconds < 10:
        time_formatted = f"{minutes}:{seconds}.0{milliseconds}"
    elif seconds >= 10 and milliseconds >= 10:
        time_formatted = f"{minutes}:{seconds}.{milliseconds}"
    else:
        print("error")
        time_formatted = 0

    return time_formatted


def end_text_generator(time, best_time_check):  # closed
    seconds = time // 60
    if best_time_check:
        ans = "new best time!!1!!1"
    elif seconds <= 50:
        ans = random.choice(["wowwowowo soo cool", "too fast."])
    elif 50 < seconds <= 75:
        ans = random.choice(["kinda mid tho", "meh.", "its okay ig", "nah id win"])
    elif 75 < seconds <= 90:
        ans = random.choice(["slowing down", "bad run?"])
    elif 90 < seconds <= 120:
        ans = random.choice(
            [
                "kinda a jake timing there",
                "kinda an alethea timing there",
                "not a ying bing timing there",
            ]
        )
    else:
        ans = random.choice(["think you broke my timer :("])
    return ans


def update_best_time(time):
    with open("assets/data.json", "r") as file:
        time_data_raw = json.load(file)

    if time_data_raw["time_set"]:
        best_minutes = time_data_raw["minutes"]
        best_seconds = time_data_raw["seconds"]
        best_milliseconds = time_data_raw["milliseconds"]
        best_milliseconds = int(best_milliseconds)
        best_time = (
            (best_minutes * 60 * 60)
            + (best_seconds * 60)
            + (best_milliseconds // (100 / 60))
        )

        if time < best_time:
            current_minutes = time // 3600
            current_seconds = (time // 60) - (current_minutes * 60)
            current_milliseconds = (
                (time // (60 / 100))
                - (current_seconds * 100)
                - (current_minutes * 60 * 100)
            )
            current_milliseconds = int(current_milliseconds)

            time_data_raw["minutes"] = current_minutes
            time_data_raw["seconds"] = current_seconds
            time_data_raw["milliseconds"] = current_milliseconds

            with open("assets/data.json", "w") as file:
                json.dump(time_data_raw, file)

    elif not time_data_raw["time_set"]:
        current_minutes = time // 3600
        current_seconds = (time // 60) - (current_minutes * 60)
        current_milliseconds = (
            (time // (60 / 100))
            - (current_seconds * 100)
            - (current_minutes * 60 * 100)
        )
        current_milliseconds = int(current_milliseconds)

        time_data_raw["minutes"] = current_minutes
        time_data_raw["seconds"] = current_seconds
        time_data_raw["milliseconds"] = current_milliseconds
        time_data_raw["time_set"] = True

        with open("assets/data.json", "w") as file:
            json.dump(time_data_raw, file)


def init_game_elements(format):  # not closed
    global platforms, change_level

    player.init_position(format)
    objective.init_position(format)
    platforms = init_platforms_position(format)
    change_level = False


def updateScreen():  # not closed
    screen.fill(colour.background)

    if not check.is_end(level, levels):
        draw.level_text(screen, level)

        time_formatted = format_time(time)
        draw.time(screen, time_formatted, timer_active)

    elif check.is_end(level, levels):
        time_formatted = format_time(time)
        draw.end_time(screen, time_formatted)
        draw.end_text(screen, end_text)

    floor.draw(screen, screen_dimensions, colour)
    objective.draw(screen, levels[level]["image"], colour)
    player.draw(short, screen, images)
    draw.platform(screen, platforms)

    pygame.display.flip()
    pygame.display.update()


def main():
    global change_level, level, platforms, time, timer_active, short, end_text

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
        if keys[pygame.K_LEFT]:
            player.move("left", short, screen_dimensions)
        elif keys[pygame.K_RIGHT]:
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

        # hard restart when ; pressed
        if keys[pygame.K_SEMICOLON]:
            level = 1
            time = 0

            format = levels[level]["format"]
            init_game_elements(format)

        # soft restart wher r pressed
        if keys[pygame.K_r]:
            format = levels[level]["format"]
            init_game_elements(format)

        # set end message when at end screen
        if check.is_end(level, levels) and end_text is None:
            end_text = end_text_generator(time, check.new_score(time))

        # write score is new best score
        if check.is_end(level, levels):
            update_best_time(time)

        updateScreen()

    pygame.quit()


if __name__ == "__main__":
    main()
