import pygame
import random
import sys
import json
from test import get_selected_config
selected_config = get_selected_config()
with open('colours.json', 'r') as json_file:
    COLOURS = json.load(json_file)

# Minefield Dimensions
x = selected_config[0]
y = selected_config[1]

# Adjust game difficulty
if selected_config[2]<1:
    BOMB_COUNT = int(round(x*y*selected_config[2]))
else:
    BOMB_COUNT = selected_config[2]
if selected_config[3]<1:
    lives = int(round(x*y*selected_config[3]))
else:
    lives = selected_config[3]
print(x, y, lives, BOMB_COUNT)
# Define game constants
MARGIN = 5
FONT_SIZE = 24
lives_used = 1

# Initialize Pygame
pygame.init()

# Create the screen
WIDTH = 0.95 * pygame.display.get_desktop_sizes()[0][0]
HEIGHT = 0.95 * pygame.display.get_desktop_sizes()[0][1]
GRID_SIZE = round(min((WIDTH - (x + 1) * MARGIN) / x, (HEIGHT - 30 - (y + 1) * MARGIN) / y))
WIDTH = x * GRID_SIZE + (x + 1) * MARGIN
HEIGHT = y * GRID_SIZE + (y + 1) * MARGIN + 30
screen = pygame.display.set_mode([WIDTH, HEIGHT])

# Set the window title
pygame.display.set_caption("Minesweeper")

# Create the font
font = pygame.font.SysFont(None, FONT_SIZE)

# Define game state
START_SCREEN = 0
IN_GAME = 1
GAME_OVER = 2

# Set initial game state
game_state = START_SCREEN
while game_state == START_SCREEN:
    screen.fill(COLOURS['BORDER'])

    # Draw the start screen message
    start_text = font.render("Click to Play", True, COLOURS['RED'])
    start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    highlight = COLOURS['LG']
    lowlight = COLOURS['WHITE']
    border_thickness = 8

    start_text_surf = pygame.Surface((200, 50))
    start_text_surf.fill(lowlight)
    border_rect = pygame.Rect(0, 0, start_text_surf.get_width(), start_text_surf.get_height())
    border_rect_out = pygame.Rect(0, 0, start_text_surf.get_width(), start_text_surf.get_height())
    pygame.draw.rect(start_text_surf, COLOURS['GRAY'], border_rect, border_thickness + 2)
    pygame.draw.rect(start_text_surf, highlight, border_rect_out, border_thickness - 2)

    start_text_rect = start_text.get_rect(center=start_text_surf.get_rect().center)
    start_text_rect.move_ip(0, 0)
    start_text_surf.blit(start_text, start_text_rect)

    screen.blit(start_text_surf,
                ((WIDTH - start_text_surf.get_width()) // 2, (HEIGHT - start_text_surf.get_height()) // 2))

    # Update the screen
    pygame.display.flip()

    # Wait for the user to click to start the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            game_state = IN_GAME
revealed = []
flagged = []
revealed_count = 0
for row in range(y):
    revealed.append([False] * x)
    flagged.append([False] * x)

# Create the game grid
grid = []
screen.fill(COLOURS['BORDER'])
for row in range(y):
    grid.append([])
    for column in range(x):
        grid[row].append(0)

# Place the bombs randomly
for i in range(BOMB_COUNT):
    while True:
        row = random.randint(0, y - 1)
        col = random.randint(0, x - 1)
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
                if row + i < 0 or row + i > y - 1 or col + j < 0 or col + j > x - 1:
                    continue
                if grid[row + i][col + j] == -1:
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
            pygame.draw.rect(screen, COLOURS['RED'], rect)
        else:
            pygame.draw.rect(screen, COLOURS['WHITE'], rect)
            if grid[row][col] > 0:
                text = font.render(str(grid[row][col]), True, COLOURS['BORDER'])
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
    elif flagged[row][col]:
        pygame.draw.rect(screen, COLOURS['BLUE'], rect)
    else:
        pygame.draw.rect(screen, COLOURS['GRAY'], rect)


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
            # Click empty tile
            if event.button == 1:
                row = event.pos[1] // max(1, GRID_SIZE + MARGIN)
                col = event.pos[0] // max(1, GRID_SIZE + MARGIN)
                if not revealed[row][col] and not flagged[row][col]:
                    revealed[row][col] = True
                    revealed_count += 1  # Update revealed count
                    if grid[row][col] == -1 and lives == lives_used:
                        BOMB_COUNT -= 1
                        done = True
                    elif grid[row][col] == -1:
                        lives_used += 1
                        BOMB_COUNT -= 1
                    elif grid[row][col] == 0:
                        queue = [(row, col)]
                        while len(queue) > 0:
                            row, col = queue.pop(0)
                            for i in range(-1, 2):
                                for j in range(-1, 2):
                                    if row + i < 0 or row + i > y - 1 or col + j < 0 or col + j > x - 1:
                                        continue
                                    if not revealed[row + i][col + j]:
                                        revealed[row + i][col + j] = True
                                        revealed_count += 1  # Update revealed count
                                        if grid[row + i][col + j] == 0:
                                            queue.append((row + i, col + j))
                    # End game if all empty cells revealed
                    if revealed_count == y * x - BOMB_COUNT:
                        done = True
            # Flag function by right click
            elif event.button == 3:
                row = event.pos[1] // (GRID_SIZE + MARGIN)
                col = event.pos[0] // (GRID_SIZE + MARGIN)
                if not revealed[row][col]:
                    flagged[row][col] = not flagged[row][col]  # Toggle the flagged state

    # Draw the grid
    screen.fill(COLOURS['BORDER'])
    for row in range(y):
        for col in range(x):
            draw_cell(row, col)

    # Draw the revealed cell count
    flagged_count = sum(row.count(True) for row in flagged)
    count_text = font.render("Safe cells left: {}, Bombs left: {}, Lives left: {}".format(
        x * y - revealed_count - BOMB_COUNT, BOMB_COUNT - flagged_count, (lives - lives_used + 1)*" <3 "),
        True, COLOURS['LG'])
    screen.blit(count_text, (10, GRID_SIZE * y + (y + 1) * MARGIN + 5))

    # Update the screen
    pygame.display.flip()


# Game over - Reveal all bombs
def reveal_cells(x, y):
    for row in range(y):
        for col in range(x):
            if grid[row][col] == -1:
                revealed[row][col] = True
            if grid[row][col] != -1 and flagged[row][col] == True:
                flagged[row][col] = False
    for row in range(y):
        for col in range(x):
            draw_cell(row, col)


# Update the screen
pygame.display.flip()


# Determine win or loss
def end_condition(revealed_count, x, y, BOMB_COUNT):
    if revealed_count >= y * x - BOMB_COUNT:
        reveal_cells(x, y)
        text = font.render("You Win!", True, COLOURS['GREEN'])
        highlight = COLOURS['LG']
        lowlight = COLOURS['WHITE']
    else:
        reveal_cells(x, y)
        text = font.render("Game Over", True, COLOURS['RED'])
        highlight = COLOURS['LP']
        lowlight = COLOURS['WHITE']
    return (highlight, lowlight, text)


# Display message
def end_message(highlight, lowlight, text):
    border_thickness = 8

    text_surf = pygame.Surface((200, 50))
    text_surf.fill(lowlight)
    border_rect = pygame.Rect(0, 0, text_surf.get_width(), text_surf.get_height())
    border_rect_out = pygame.Rect(0, 0, text_surf.get_width(), text_surf.get_height())
    pygame.draw.rect(text_surf, COLOURS['GRAY'], border_rect, border_thickness + 2)
    pygame.draw.rect(text_surf, highlight, border_rect_out, border_thickness - 2)

    text_rect = text.get_rect(center=text_surf.get_rect().center)
    text_rect.move_ip(0, 0)
    text_surf.blit(text, text_rect)

    screen.blit(text_surf, ((WIDTH - text_surf.get_width()) // 2, (HEIGHT - text_surf.get_height()) // 2))
    pygame.display.flip()

end_condition = end_condition(revealed_count, x, y, BOMB_COUNT)
end_message(end_condition[0], end_condition[1], end_condition[2])


# Wait for user to close the window
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()