import pygame
import time


def main():
    text = read_text("text_to_read.txt")
    partitioned_text = split_text(text)

    dist_from_left = 900
    dist_from_top = 100
    box_width = 600
    margin = 30

    pygame.init()
    prev_time = time.time()
    FPS = 30
    font = pygame.font.SysFont(None, 24)
    screen = pygame.display.set_mode([1600, 1000])
    running = True
    while running:
        current_time = time.time()
        dt = current_time - prev_time
        prev_time = current_time
        sleep_time = 1. / FPS - dt
        if sleep_time > 0:
            time.sleep(sleep_time)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        text_blocks = text_block_create(partitioned_text, font, box_width, margin, dist_from_top)

        for text_block in text_blocks:
            pygame.draw.rect(screen, (50, 50, 50), (dist_from_left, text_block["y"], box_width, text_block["height"]))
            write_lines(text_block["text"], font, screen, dist_from_left + margin, text_block["y"] + margin)

        # Output what we've drawn to the screen
        pygame.display.flip()

    pygame.quit()


def split_text(text):
    words = text.split(" ")
    segment_end_positions = [
        int(position_string)
        for position_string in read_text("split_positions.txt").split(",")
    ] + [len(words)]

    segment_start_positions = [0] + segment_end_positions[:-1]

    return [
        words[start:end]
        for start, end in zip(segment_start_positions, segment_end_positions)
    ]


def read_text(file_name):
    file = open(file_name, "r")
    content = file.read()
    file.close()
    return content


def text_block_create(split_text, font, box_width, margin, dist_from_top):
    vertical_offset = 0
    text_blocks = []
    for text in split_text:
        lines = wrap_text(words=text, font=font, max_length=box_width - (2 * margin))
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
