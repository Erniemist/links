import pygame


def main():
    pygame.init()
    screen = pygame.display.set_mode([1600, 1000])
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        dist_from_left = 900
        dist_from_top = 100
        box_width = 600
        margin = 30

        font = pygame.font.SysFont(None, 24)

        text = "I want you to know, brothers, that what has happened to me has really served to advance the gospel, so that it has become known throughout the whole imperial guard and to all the rest that my imprisonment is for Christ. And most of the brothers, having become confident in the Lord by my imprisonment, are much more bold to speak the word without fear."
        split_text = []
        pre, mid, post = text.partition("gospel")
        split_text.append(pre + mid)
        split_text.append(post)

        text_blocks = text_block_create(split_text, font, box_width, margin, dist_from_top)

        for text_block in text_blocks:
            pygame.draw.rect(screen, (50, 50, 50), (dist_from_left, text_block["y"], box_width, text_block["height"]))
            write_lines(text_block["text"], font, screen, dist_from_left + margin, text_block["y"] + margin)

        # Output what we've drawn to the screen
        pygame.display.flip()

    pygame.quit()


def text_block_create(split_text, font, box_width, margin, dist_from_top):
    vertical_offset = 0
    text_blocks = []
    for text in split_text:
        lines = wrap_text(words=text.split(" "), font=font, max_length=box_width - (2 * margin))
        box_height = wrapped_text_height(lines, font) + 2 * margin

        text_blocks.append({
            "y": dist_from_top + vertical_offset,
            "height": box_height,
            "text": lines,
        })

        vertical_offset += box_height
    return text_blocks


def wrap_text(words, font, max_length):
    lines = []
    line = ""
    ghostline = ""

    for word in words:
        ghostline += word + " "
        ghostline_length, _ = font.size(ghostline)
        if ghostline_length > max_length:
            lines.append(line)
            line = ""
            ghostline = word + " "
        else:
            line = ghostline
    lines.append(line)

    return lines


def write_lines(lines, font, screen, x, y):
    total_line_height = 0
    for line in lines:
        write_line(line, font, screen, x, y + total_line_height)
        _, line_height = font.size(line)
        total_line_height += line_height


def write_line(line, font, screen, x, y):
    text_block = font.render(line, True, (255, 255, 255))
    screen.blit(text_block, (x, y))


def wrapped_text_height(lines, font):
    total_line_height = 0
    for line in lines:
        _, line_height = font.size(line)
        total_line_height += line_height

    return total_line_height


if __name__ == "__main__":
    main()
