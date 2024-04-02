import pygame


def onFloor(player, floor, screen_dimensions):
    if player.y + player.height >= screen_dimensions.height - floor.height:
        return True
    else:
        return False


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
