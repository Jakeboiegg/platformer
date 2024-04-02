def level_text(screen, number, level_font, screen_dimensions, colour):
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


def platform(screen, platforms, colour):
    for platform in platforms:
        platform.draw(screen, colour)


def time(screen, time, time_font, colour):
    time = int(time)
    minutes = time // 3600
    seconds = (time // 60) - (minutes * 60)

    if seconds < 10:
        time_formatted = f"{minutes}:0{seconds}"
    else:
        time_formatted = f"{minutes}:{seconds}"

    time_text_surface = time_font.render(time_formatted, True, colour.level_text)
    screen.blit(time_text_surface, (30, 30))
