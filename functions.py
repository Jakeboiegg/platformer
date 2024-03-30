import pygame
from levels import levels
from classes import Platform

pygame.init()


def init_player_position(level):
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
        return []


def init_objective_position(level):
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
        return []


def init_platforms_position(level):
    platforms = []
    for row_number, row in enumerate(levels[level]["format"]):
        for column_number, editor_chr in list(enumerate(row)):
            if editor_chr == "x":
                platforms.append(Platform(column_number * 20, row_number * 40))

    return platforms


def floorCollision(player, floor, screen_dimensions):
    if onFloor(player, floor, screen_dimensions):
        player.y = screen_dimensions.height - floor.height - player.height


def onFloor(player, floor, screen_dimensions):
    if player.y + player.height >= screen_dimensions.height - floor.height:
        return True
    else:
        return False


def keepInWindow(player, screen_dimensions):
    if player.x < 0:
        player.x = 0
    if player.x > screen_dimensions.width - player.width:
        player.x = screen_dimensions.width - player.width


def platformCollision(platforms, player):
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


def onPlatform(platforms, player):
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


def touchingObective(player, objective):
    player_rect = pygame.rect.Rect((player.x, player.y, player.width, player.height))
    objective_rect = pygame.rect.Rect(
        (objective.x, objective.y, objective.width, objective.height)
    )
    if player_rect.colliderect(objective_rect):
        return True
    else:
        return False
