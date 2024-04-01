import pygame
import math

pygame.init()


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
        player.velocity = 0
    if player.x > screen_dimensions.width - player.width:
        player.x = screen_dimensions.width - player.width
        player.velocity = 0


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


def vibrate(objective, time):
    offset = 5 * math.sin(time / 15)
    objective.y = objective.initialy + offset
