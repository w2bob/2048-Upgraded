import pygame
import random
import sys

# specs
WIDTH, HEIGHT = 400, 500
BOARD_SIZE = 4
TILE_SIZE = WIDTH // BOARD_SIZE
FPS = 60
BACKGROUND_COLOR = (187, 173, 160)
EMPTY_TILE_COLOR = (205, 193, 180)
FONT_COLOR = (119, 110, 101)
FONT = None

# start
pygame.init()
FONT = pygame.font.SysFont("arial", 40)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 Game")

# Predefined colors for dynamic assignment
COLOR_PALETTE = [
    (238, 228, 218), (237, 224, 200), (242, 177, 121), (245, 149, 99),
    (246, 124, 95), (246, 94, 59), (237, 207, 114), (237, 204, 97),
    (237, 200, 80), (237, 197, 63), (237, 194, 46), (60, 58, 50)
]
TILE_COLORS = {}

# Function to assign colors dynamically
def assign_colors(value):
    if value not in TILE_COLORS:
        if len(TILE_COLORS) < len(COLOR_PALETTE):
            TILE_COLORS[value] = COLOR_PALETTE[len(TILE_COLORS)]
        else:
            TILE_COLORS[value] = COLOR_PALETTE[-1]  # Use a default color if palette is exhausted

# drawing
def draw_board(board, mode):
    SCREEN.fill(BACKGROUND_COLOR)
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            value = board[row][col]
            assign_colors(value)
            color = TILE_COLORS.get(value, (0, 0, 0))
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE + TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(SCREEN, color, rect)
            if value != 0:
                text = FONT.render(str(value), True, FONT_COLOR)
                text_rect = text.get_rect(center=(col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2 + TILE_SIZE))
                SCREEN.blit(text, text_rect)
    pygame.display.update()

# tile generation
def add_new_tile(board, mode):
    empty_tiles = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if board[r][c] == 0]
    if empty_tiles:
        row, col = random.choice(empty_tiles)
        board[row][col] = mode

# legal move or not
def can_move(board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 0:
                return True
            if col < BOARD_SIZE - 1 and board[row][col] == board[row][col + 1]:
                return True
            if row < BOARD_SIZE - 1 and board[row][col] == board[row + 1][col]:
                return True
    return False

# movement
def move(board, direction, mode):
    def merge(row):
        merged_row = [i for i in row if i != 0]
        for i in range(len(merged_row) - 1):
            if merged_row[i] == merged_row[i + 1]:
                merged_row[i] = merged_row[i] * (2 if mode == 2 else 3)
                merged_row[i + 1] = 0
        merged_row = [i for i in merged_row if i != 0]
        while len(merged_row) < BOARD_SIZE:
            merged_row.append(0)
        return merged_row

    moved = False

    if direction == 'left':
        for r in range(BOARD_SIZE):
            new_row = merge(board[r])
            if new_row != board[r]:
                moved = True
            board[r] = new_row
    elif direction == 'right':
        for r in range(BOARD_SIZE):
            new_row = merge(board[r][::-1])[::-1]
            if new_row != board[r]:
                moved = True
            board[r] = new_row
    elif direction == 'up':
        for c in range(BOARD_SIZE):
            col = merge([board[r][c] for r in range(BOARD_SIZE)])
            if col != [board[r][c] for r in range(BOARD_SIZE)]:
                moved = True
            for r in range(BOARD_SIZE):
                board[r][c] = col[r]
    elif direction == 'down':
        for c in range(BOARD_SIZE):
            original_col = [board[r][c] for r in range(BOARD_SIZE)]
            new_col = merge(original_col[::-1])[::-1]
            if new_col != original_col:
                moved = True
            for r in range(BOARD_SIZE):
                board[r][c] = new_col[r]

    return moved

# game over
def game_over_screen(win, mode):
    SCREEN.fill(BACKGROUND_COLOR)
    message = "You Win!" if win else "You Lose"
    text = FONT.render(message, True, FONT_COLOR)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    SCREEN.blit(text, text_rect)

    button_text = FONT.render("Play Again", True, FONT_COLOR)
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    pygame.draw.rect(SCREEN, (0, 0, 0), button_rect)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    SCREEN.blit(button_text, button_text_rect)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False
                    main()

def input_box(rect, label):
    font = pygame.font.SysFont("arial", 20)
    input_text = ""
    active = False
    while True:
        pygame.draw.rect(SCREEN, EMPTY_TILE_COLOR, rect)
        text = font.render(input_text, True, FONT_COLOR)
        label_text = font.render(label, True, FONT_COLOR)
        SCREEN.blit(label_text, (rect.x, rect.y - 25))
        SCREEN.blit(text, (rect.x + 5, rect.y + 5))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            elif event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN:
                    return int(input_text)
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

def welcome_screen():
    SCREEN.fill(BACKGROUND_COLOR)
    title_font = pygame.font.SysFont("arial", 20)
    title_text = title_font.render("Type in the base number and to", True, FONT_COLOR)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 205))
    SCREEN.blit(title_text, title_rect)
    title_text2 = title_font.render("what power you want to win", True, FONT_COLOR)
    title_rect2 = title_text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 185))
    SCREEN.blit(title_text2, title_rect2)


    base_number = input_box(pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 105, 200, 50), "Base Number")
    #win_power = input_box(pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 40, 200, 50), "Win Power")

    #(attempt at difficulty buttons)
    button_text_1 = FONT.render("Baby Mode", True, FONT_COLOR) # button difficulty
    button_rect_1 = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
    pygame.draw.rect(SCREEN, (0, 0, 0), button_rect_1)
    button_text_1_rect = button_text_1.get_rect(center=button_rect_1.center)
    SCREEN.blit(button_text_1, button_text_1_rect)

    button_text_2 = FONT.render("Easy", True, FONT_COLOR)
    button_rect_2 = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 25, 200, 50)
    pygame.draw.rect(SCREEN, (0, 0, 0), button_rect_2)
    button_text_2_rect = button_text_2.get_rect(center=button_rect_2.center)
    SCREEN.blit(button_text_2, button_text_2_rect)

    button_text_3 = FONT.render("Normal", True, FONT_COLOR)
    button_rect_3 = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 75, 200, 50)
    pygame.draw.rect(SCREEN, (0, 0, 0), button_rect_3)
    button_text_3_rect = button_text_3.get_rect(center=button_rect_3.center)
    SCREEN.blit(button_text_3, button_text_3_rect)
    pygame.display.update()

    button_text_4 = FONT.render("Hard", True, FONT_COLOR)
    button_rect_4= pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 125, 200, 50)
    pygame.draw.rect(SCREEN, (0, 0, 0), button_rect_4)
    button_text_4_rect = button_text_4.get_rect(center=button_rect_4.center)
    SCREEN.blit(button_text_4, button_text_4_rect)
    pygame.display.update()

    button_text_5 = FONT.render("Super Hard", True, FONT_COLOR)
    button_rect_5= pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 175, 200, 50)
    pygame.draw.rect(SCREEN, (0, 0, 0), button_rect_5)
    button_text_5_rect = button_text_5.get_rect(center=button_rect_5.center)
    SCREEN.blit(button_text_5, button_text_5_rect)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect_1.collidepoint(event.pos):
                    win_power = 9
                    waiting = False
                elif button_rect_2.collidepoint(event.pos):
                    win_power = 10
                    waiting = False
                elif button_rect_3.collidepoint(event.pos):
                    win_power = 11
                    waiting = False
                elif button_rect_4.collidepoint(event.pos):
                    win_power = 12
                    waiting = False
                elif button_rect_5.collidepoint(event.pos):
                    win_power = 13
                    waiting = False
    return base_number, win_power


def main():
    base_number, win_power = welcome_screen()
    win_value = base_number ** win_power
    board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    add_new_tile(board, base_number)
    add_new_tile(board, base_number)
    clock = pygame.time.Clock()

    while True:
        moved = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    moved = move(board, 'left', base_number)
                elif event.key == pygame.K_RIGHT:
                    moved = move(board, 'right', base_number)
                elif event.key == pygame.K_UP:
                    moved = move(board, 'up', base_number)
                elif event.key == pygame.K_DOWN:
                    moved = move(board, 'down', base_number)
        
        if moved:
            add_new_tile(board, base_number)

        if any(any(tile == win_value for tile in row) for row in board):
            game_over_screen(True, base_number)
            return
        if not can_move(board):
            game_over_screen(False, base_number)
            return

        draw_board(board, base_number)
        clock.tick(FPS)

if __name__ == "__main__":
    main()
