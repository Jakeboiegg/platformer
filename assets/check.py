import pygame
import json


def onFloor(y, player, floor, screen_dimensions):
    if y + player.height >= screen_dimensions.height - floor.height:
        return True
    else:
        return False


def inFloor(y, player, floor, screen_dimensions):
    if y + player.height > screen_dimensions.height - floor.height:
        return True
    else:
        return False


def onPlatform(x, y, player, platforms):
    for platform in platforms:
        player_left = x
        player_right = x + player.width
        platform_left = platform.x
        platform_right = platform.x + platform.width
        platform_top = platform.y
        player_bottom = y + player.height
        if (
            platform_top <= player_bottom <= platform_top + player.gravity
            and player_left <= platform_right
            and player_right >= platform_left
        ):
            return True
    return False


def inPlatform(x, y, player, platforms):
    for platform in platforms:
        player_left = x
        player_right = x + player.width
        platform_left = platform.x
        platform_right = platform.x + platform.width
        platform_top = platform.y
        player_top = y
        player_bottom = y + player.height
        if (
            (
                platform_top < player_bottom < platform_top + player.gravity
                or platform_top < player_top < platform_top + player.gravity
            )
            and player_left < platform_right
            and player_right > platform_left
        ):
            return True
    return False


def touchingObective(player, objective):
    player_rect = pygame.rect.Rect((player.x, player.y, player.width, player.height))
    objective_rect = pygame.rect.Rect(
        (objective.x, objective.y, objective.width, objective.height)
    )
    if player_rect.colliderect(objective_rect):
        return True
    else:
        return False


def new_score(time):
    with open("assets/data.json", "r") as file:
        time_data_raw = json.load(file)

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
            return True
        else:
            return False


def is_end(level, levels):
    if level == len(levels):
        return True
    else:
        return False
