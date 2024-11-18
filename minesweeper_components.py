import pygame
import random
from config import *

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # Globalis valtozokent a foprogram megkapja a jatekteret (meg a tovabbi pitty-puttyokat is alatta)

game_over = False
won = False
left_click_held = False
remaining_flags = BOMB_COUNT    # Ezt importbol megkapja a configtol
elapsed_time = 0
start_time = None
end_time = None
field = None


class Cell:                                                                                 # Jatekmezok tulajdonsagai
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.state = "0"
        self.hidden = True
        self.flagged = False

    def draw(self, screen):
        if self.flagged:
            image = cell_images["flagged"]
        elif self.hidden:
            image = cell_images["hidden"]
        else:
            image = cell_images[self.state]
        screen.blit(image, (self.col * CELL_SIZE, HEADER_HEIGHT + self.row * CELL_SIZE))


def place_bombs(field, num_bombs):                                                          # Bombak kisorsolasa
    total_cells = HORIZONTAL_CELLS * VERTICAL_CELLS
    if total_cells < num_bombs:
        raise ValueError("A játéktér nem elég nagy a bombákhoz.")

    bomb_positions = set()

    while len(bomb_positions) < num_bombs:
        row = random.randint(0, VERTICAL_CELLS - 1)
        col = random.randint(0, HORIZONTAL_CELLS - 1)
        bomb_positions.add((row, col))

    for row, col in bomb_positions:
        field[row][col].state = "mine"
        for i in range(max(0, row - 1), min(VERTICAL_CELLS, row + 2)):
            for j in range(max(0, col - 1), min(HORIZONTAL_CELLS, col + 2)):
                if (i, j) != (row, col):
                    if field[i][j].state != "mine":
                        if field[i][j].state == "hidden":
                            field[i][j].state = "0"
                        field[i][j].state = str(int(field[i][j].state) + 1)                 # Beallitjuk a bombak koruli mezok szamait is


def create_field(vertical_cells, horizontal_cells):                                         # Jatekter meghatarozasa megadott meretek alapjan (beginner: 9x9)
    field = []
    for row in range(vertical_cells):
        field_row = []
        for col in range(horizontal_cells):
            field_row.append(Cell(row, col))
        field.append(field_row)
    return field


def draw_field():                                                                           # Jatekter kirajzolasa
    for row in field:
        for cell in row:
            cell.draw(screen)


def draw_header():                                                                          # Fejlec (ido es hatralevo zaszlok kijelzese)
    pygame.draw.rect(screen, GRAY, (0, 0, WINDOW_WIDTH, HEADER_HEIGHT))

    flags_text = font.render(f'Flags: {remaining_flags}', True, BLACK)
    screen.blit(flags_text, (10, 30))

    smiley_rect = pygame.Rect(WINDOW_WIDTH // 2 - 25, 25, 50, 50)

    if game_over:
        if won:
            screen.blit(smiley_winner_image, smiley_rect)
        else:
            screen.blit(smiley_dead_image, smiley_rect)
    elif left_click_held:
        screen.blit(smiley_O_O_image, smiley_rect)
    else:
        screen.blit(smiley_image, smiley_rect)

    timer_text = font.render(f'Time: {elapsed_time}', True, BLACK)
    timer_x_position = WINDOW_WIDTH - 100 - (len(str(elapsed_time)) - 1) * 15
    screen.blit(timer_text, (timer_x_position, 30))


def handle_events():                                                                        # Esemenykezeles (pl kattintasok)
    global game_over, field, end_time, won, left_click_held, remaining_flags

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if y > HEADER_HEIGHT:
                if game_over:
                    continue

                col = x // CELL_SIZE
                row = (y - HEADER_HEIGHT) // CELL_SIZE
                if 0 <= row < VERTICAL_CELLS and 0 <= col < HORIZONTAL_CELLS:
                    handle_mouse_click(event, row, col)
            else:
                handle_header_click(event)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                left_click_held = False

    return True


def handle_mouse_click(event, row, col):                                                    # Kattintaskezeles
    global left_click_held, won, game_over

    if event.button == 1:
        if field[row][col].hidden and not field[row][col].flagged:
            left_click_held = True
            reveal_cell(row, col)
            if check_win_condition():
                won = True
                game_over = True
                end_time = pygame.time.get_ticks()
    elif event.button == 3:
        if field[row][col].hidden:
            toggle_flag(row, col)


def toggle_flag(row, col):                                                                  # Jobb egergombbal megjelolhetjuk zaszloval a gyanus mezoket (felteve, hogy megy a jatek, es nem fogytak el zaszloink)
    global remaining_flags

    if not field[row][col].flagged and remaining_flags > 0:
        field[row][col].flagged = True
        remaining_flags -= 1
    elif field[row][col].flagged:
        field[row][col].flagged = False
        remaining_flags += 1


def reveal_cell(row, col):                                                                  # Kattintaskor a cellat felfedjuk, ha 0, akkor a kornyezo 0kra is meghivjuk
    global game_over, end_time, won

    if not field[row][col].hidden or field[row][col].flagged or game_over:
        return

    field[row][col].hidden = False

    if field[row][col].state == "mine":
        field[row][col].state = "killer_mine"
        game_over = True
        end_time = pygame.time.get_ticks()
        reveal_all_cells()
    elif field[row][col].state == "0":
        for i in range(max(0, row - 1), min(VERTICAL_CELLS, row + 2)):
            for j in range(max(0, col - 1), min(HORIZONTAL_CELLS, col + 2)):
                if field[i][j].hidden and not field[i][j].flagged:
                    reveal_cell(i, j)

    if check_win_condition():
        won = True
        game_over = True
        end_time = pygame.time.get_ticks()
        reveal_all_cells()


def reveal_all_cells():                                                                     # GameOverkor a cellak felfedesre kerulnek
    for row in field:
        for cell in row:
            if cell.flagged and cell.state != "mine":
                cell.state = "incorrectly_flagged"
                cell.flagged = False
            cell.hidden = False                                                             # Kulonben nem jelezne ki


def check_win_condition():                                                                  # Ha epp annyi mezo maradt "fedett", amennyi bomba van, akkor nyertunk!
    hidden_count = sum(1 for row in field for cell in row if cell.hidden)
    return hidden_count == BOMB_COUNT


def update_elapsed_time():                                                                  # A fejlecben az ido kijelzesehez
    global elapsed_time, game_over, end_time, start_time
    if not game_over:
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    else:
        if end_time is None:
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        else:
            elapsed_time = (end_time - start_time) // 1000


def initialize_game():                                                                      # Alaphelyzetbe rakja a jatekot
    global game_over, field, end_time, won, left_click_held, start_time, remaining_flags

    start_time = pygame.time.get_ticks()
    remaining_flags = BOMB_COUNT
    game_over = False
    end_time = None
    won = False
    left_click_held = False

    # A bombalehelyezessel kezdjuk
    field = create_field(VERTICAL_CELLS, HORIZONTAL_CELLS)
    try:
        place_bombs(field, BOMB_COUNT)
    except ValueError as e:
        print(e)
        pygame.quit()
        sys.exit()


def handle_header_click(event):                                                             # Az emojira kattintassal torteno uj jatek kezdesehez
    global game_over

    smiley_rect = pygame.Rect(WINDOW_WIDTH // 2 - 25, 25, 50, 50)
    if smiley_rect.collidepoint(event.pos) and game_over:
        initialize_game()
