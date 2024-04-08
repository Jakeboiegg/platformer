from platformer import (
    screen_dimensions,
    colour,
    font,
)


def level_text(screen, number):
    number = str(number)
    level_text_surface = font.level.render(number, True, colour.level_text)
    level_text_rect = level_text_surface.get_rect()
    screen.blit(
        level_text_surface,
        (
            (screen_dimensions.width / 2) - (level_text_rect.width / 2),
            (screen_dimensions.height / 2) - (level_text_rect.height / 2),
        ),
    )


def platform(screen, platforms):
    for platform in platforms:
        platform.draw(screen, colour)


def time(screen, time_formatted, timer_active):
    if not timer_active:
        time_text_surface = font.time.render(time_formatted, True, colour.time_text)
        screen.blit(time_text_surface, (30, 30))
    elif timer_active:
        time_text_surface = font.time.render(time_formatted, True, colour.time_text)
        screen.blit(time_text_surface, (30, 30))


def end_time(screen, time_formatted):
    time_surface = font.endscreen_time.render(time_formatted, True, colour.time_text)
    time_width, time_height = time_surface.get_size()
    screen.blit(
        time_surface,
        (
            (screen_dimensions.width / 2) - (time_width / 2),
            (screen_dimensions.height / 2) - (time_height / 2) - (20),
        ),
    )


def end_text(screen, text):
    text_surface = font.endscreen_text.render(text, True, colour.time_text)
    text_width, text_height = text_surface.get_size()
    screen.blit(
        text_surface,
        (
            (screen_dimensions.width / 2) - (text_width / 2),
            (screen_dimensions.height / 2) - (text_height / 2) + (60),
        ),
    )


def best_time(screen, text):
    text_surface = font.endscreen_best_time.render(text, True, colour.time_text)
    text_width, text_height = text_surface.get_size()
    screen.blit(
        text_surface,
        (
            (screen_dimensions.width / 2) - (text_width / 2),
            (screen_dimensions.height / 2) - (text_height / 2) - (90),
        ),
    )
