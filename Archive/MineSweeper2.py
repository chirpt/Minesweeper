import pygame
import random
import sys

#Minefield Dimensions
x = 100
y = 50

#Adjust game difficulty
BOMB_COUNT = 3
lives = 1

# Define some colors
BORDER = (75, 75, 75)           # BLACK
WHITE = (200, 200, 200)         #
GRAY = (128, 128, 128)          #
LIGHT_GRAY = (160, 160, 160)    #
RED = (175, 50, 50)             #
GREEN = (50, 130, 50)           #
LP = (175, 100, 100)            #
LG = (100, 175, 100)            #
BLUE = (100, 100, 175)          # BLUE

# Define game constants

MARGIN = 5
FONT_SIZE = 24
lives_used = 1

remaining_cells = x * y - BOMB_COUNT - 10

# Initialize Pygame
pygame.init()



# Create the screen
WIDTH = 0.9*pygame.display.get_desktop_sizes()[0][0]
HEIGHT = 0.9*pygame.display.get_desktop_sizes()[0][1]
GRID_SIZE = round(min((WIDTH-(x+1)*MARGIN)/x, (HEIGHT-30-(y+1)*MARGIN)/y))
screen = pygame.display.set_mode([0.5*WIDTH, 0.5*HEIGHT])
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Set the window title
pygame.display.set_caption("Minesweeper")

# Create the font
font = pygame.font.SysFont(None, FONT_SIZE)

START_SCREEN = 0
IN_GAME = 1
GAME_OVER = 2

# Set initial game state
game_state = START_SCREEN
x_slider_value = 40
y_slider_value = 20
while game_state == START_SCREEN:
    screen.fill(BORDER)

    # Draw the sliders
    x_slider_text = font.render(f"Columns (x): {x_slider_value}", True, WHITE)
    y_slider_text = font.render(f"Rows (y): {y_slider_value}", True, WHITE)

    x_slider_rect = x_slider_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
    y_slider_rect = y_slider_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))

    screen.blit(x_slider_text, x_slider_rect)
    screen.blit(y_slider_text, y_slider_rect)

    # Draw the start screen message
    start_text = font.render("Click to Play", True, RED)
    start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    highlight = LG
    lowlight = WHITE
    border_thickness = 8

    start_text_surf = pygame.Surface((200, 50))
    start_text_surf.fill(lowlight)
    border_rect = pygame.Rect(0, 0, start_text_surf.get_width(), start_text_surf.get_height())
    border_rect_out = pygame.Rect(0, 0, start_text_surf.get_width(), start_text_surf.get_height())
    pygame.draw.rect(start_text_surf, GRAY, border_rect, border_thickness + 2)
    pygame.draw.rect(start_text_surf, highlight, border_rect_out, border_thickness - 2)

    start_text_rect = start_text.get_rect(center=start_text_surf.get_rect().center)
    start_text_rect.move_ip(0, 0)
    start_text_surf.blit(start_text, start_text_rect)

    screen.blit(start_text_surf, ((WIDTH - start_text_surf.get_width()) // 2, (HEIGHT - start_text_surf.get_height()) // 2))

    # Update the screen
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            game_state = IN_GAME
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:  # Scroll up
            x_slider_value = min(50, x_slider_value + 1)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:  # Scroll down
            x_slider_value = max(5, x_slider_value - 1)

        # Draw the sliders on the screen
    x_slider = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 20, 100, 10)
    y_slider = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 40, 100, 10)

    pygame.draw.rect(screen, WHITE, x_slider)
    pygame.draw.rect(screen, WHITE, y_slider)

    x_slider_handle = pygame.Rect(
        WIDTH // 2 - 50 + (x_slider_value - 10) * 2, HEIGHT // 2 - 20, 5, 30
    )
    y_slider_handle = pygame.Rect(
        WIDTH // 2 - 50 + (y_slider_value - 10) * 2, HEIGHT // 2 + 40, 5, 30
    )

    pygame.draw.rect(screen, WHITE, x_slider_handle)
    pygame.draw.rect(screen, WHITE, y_slider_handle)

    # Update the screen
    pygame.display.flip()
x = x_slider_value
screen = pygame.display.set_mode([x*GRID_SIZE+(x+1)*MARGIN, y*GRID_SIZE+(y+1)*MARGIN+30])
revealed = []
flagged = []
revealed_count = 0
for row in range(y):
    revealed.append([False] * x)
    flagged.append([False] * x)

# Create the game grid
grid = []
screen.fill(BORDER)
for row in range(y):
    grid.append([])
    for column in range(x):
        grid[row].append(0)

# Place the bombs randomly
for i in range(BOMB_COUNT):
    while True:
        row = random.randint(0, y-1)
        col = random.randint(0, x-1)
        if grid[row][col] != -1:
            grid[row][col] = -1
            break

# Count the number of bombs adjacent to each cell
for row in range(y):
    for col in range(x):
        if grid[row][col] == -1:
            continue
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if row+i < 0 or row+i > y-1 or col+j < 0 or col+j > x-1:
                    continue
                if grid[row+i][col+j] == -1:
                    count += 1
        grid[row][col] = count

# Define the function to draw a cell
def draw_cell(row, col):
    rect = pygame.Rect(col * (GRID_SIZE + MARGIN) + MARGIN,
                       row * (GRID_SIZE + MARGIN) + MARGIN,
                       GRID_SIZE,
                       GRID_SIZE)
    if revealed[row][col]:
        if grid[row][col] == -1:
            pygame.draw.rect(screen, RED, rect)
        else:
            pygame.draw.rect(screen, WHITE, rect)
            if grid[row][col] > 0:
                text = font.render(str(grid[row][col]), True, BORDER)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
    elif flagged[row][col]:
        pygame.draw.rect(screen, BLUE, rect)
    else:
        pygame.draw.rect(screen, GRAY, rect)

# Create the game loop
done = False
revealed = []
flagged = []
revealed_count = 0
for row in range(y):
    revealed.append([False] * x)
    flagged.append([False] * x)
while not done:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                row = event.pos[1] // max(1, GRID_SIZE + MARGIN)
                col = event.pos[0] // max(1, GRID_SIZE + MARGIN)
                if not revealed[row][col]:
                    revealed[row][col] = True
                    revealed_count += 1  # Update revealed count
                    if grid[row][col] == -1 and lives==lives_used:
                        BOMB_COUNT -= 1
                        done = True
                    elif grid[row][col] == -1:
                        lives_used += 1
                        BOMB_COUNT-=1
                    elif grid[row][col] == 0:
                        queue = [(row, col)]
                        while len(queue) > 0:
                            row, col = queue.pop(0)
                            for i in range(-1, 2):
                                for j in range(-1, 2):
                                    if row+i < 0 or row+i > y-1 or col+j < 0 or col+j > x-1:
                                        continue
                                    if not revealed[row+i][col+j]:
                                        revealed[row+i][col+j] = True
                                        revealed_count += 1  # Update revealed count
                                        if grid[row+i][col+j] == 0:
                                            queue.append((row+i, col+j))
                    if revealed_count == y * x - BOMB_COUNT:
                        done = True
            elif event.button == 3:
                row = event.pos[1] // (GRID_SIZE + MARGIN)
                col = event.pos[0] // (GRID_SIZE + MARGIN)
                if not revealed[row][col]:
                    flagged[row][col] = not flagged[row][col]  # Toggle the flagged state
    # Draw the grid
    screen.fill(BORDER)
    for row in range(y):
        for col in range(x):
            draw_cell(row, col)
    # Draw the revealed cell count
    flagged_count = sum(row.count(True) for row in flagged)
    count_text = font.render("Safe cells left: {}, Bombs left: {}, Lives left: {}".format(
    x*y - revealed_count - BOMB_COUNT, BOMB_COUNT - flagged_count, lives-lives_used+1),
    True, LG)
    screen.blit(count_text, (10, GRID_SIZE * y + (y + 1) * MARGIN + 5))

    # Update the screen
    pygame.display.flip()

# Game over
def reveal_cells(x,y):
    for row in range(y):
        for col in range(x):
            if grid[row][col] == -1:
                revealed[row][col] = True
    for row in range(y):
        for col in range(x):
            draw_cell(row, col)

pygame.display.flip()

if revealed_count >= y * x - BOMB_COUNT:
    reveal_cells(x, y)
    text = font.render("You Win!", True, GREEN)
    highlight = LG
    lowlight = WHITE
else:
    reveal_cells(x, y)
    text = font.render("Game Over", True, RED)
    highlight = LP
    lowlight = WHITE


border_thickness = 8

text_surf = pygame.Surface((200, 50))
text_surf.fill(lowlight)
border_rect = pygame.Rect(0, 0, text_surf.get_width(), text_surf.get_height())
border_rect_out = pygame.Rect(0, 0, text_surf.get_width(), text_surf.get_height())
pygame.draw.rect(text_surf, GRAY, border_rect, border_thickness+2)
pygame.draw.rect(text_surf, highlight, border_rect_out, border_thickness-2)

text_rect = text.get_rect(center=text_surf.get_rect().center)
text_rect.move_ip(0, 0)
text_surf.blit(text, text_rect)

screen.blit(text_surf, ((WIDTH - text_surf.get_width()) // 2, (HEIGHT - text_surf.get_height()) // 2))
pygame.display.flip()

# Wait for the user to close the window

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
