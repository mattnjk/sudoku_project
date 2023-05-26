# import pygame library
import pygame
#importing other file
import solver 
# initialise the pygame font
import pygame
import sys
import time
import random

# Set up the pygame window
pygame.init()
window_width = 700
window_height = 900
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Sudoku Solver")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Define grid properties
grid_size = 9
cell_size = window_width // grid_size

def reset():
    for row in range(9):
        for col in range(9):
            grid[row][col] = 0

    window.fill(WHITE)
    draw_grid()
    draw_numbers()
    display_text("Grid Reset")
    pygame.display.update()
    time.sleep(.1)  # Add a small delay for visualization


def generate_sudoku_puzzle():
    reset()

    # Solve the empty grid to generate a solved Sudoku puzzle
    solver.solve_sudoku(grid)

    # Remove some numbers from the solved puzzle to create a playable puzzle
    num_removed = random.randint(30, 40)  # Number of cells to remove (adjust as desired)

    # Remove numbers randomly while ensuring the puzzle remains solvable
    while num_removed > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)

        if grid[row][col] != 0:
            # Temporarily store the number
            temp = grid[row][col]
            grid[row][col] = 0

            # Check if the puzzle is still solvable after removing the number
            temp_grid = [row[:] for row in grid]
            if solver.solve_sudoku(temp_grid):
                # The puzzle is still solvable, keep the number removed
                num_removed -= 1
            else:
                # The puzzle is not solvable, restore the number
                grid[row][col] = temp
    # Create a copy of the original grid for solving
    solve_grid = [row[:] for row in grid]
    return grid

##Funtion for solving puzzle
#
def check_grid():
    for row in range(9):
        for col in range(9):
            if grid[row][col]!=solvedPuzzle[row][col]:
                #if grid[row][col]!=0:
                    #display_text("The value "+str(grid[row][col])+" is an invalid input for row "+str(row+1)+" and column "+str(col+1)+"so it was deleted to solve puzzle")
                    #pygame.display.update()
                display_text("checking input")
                delete_value(row, col, 0)
                pygame.draw.rect(window, BLUE, (col* cell_size, row * cell_size, cell_size, cell_size), 2)
                pygame.display.update()
                time.sleep(.2)
    bool=solve_sudoku()
    return bool
#
def solve_sudoku():
    if is_complete(grid):
        return True
    
    row, col = find_empty_cell(grid)
    
    for num in range(1, 10):
        if is_valid(grid, row, col, num):
            grid[row][col] = num
            # Update the grid and display it
            window.fill(WHITE)
            draw_grid()
            draw_numbers()
            pygame.draw.rect(window, BLUE, (col * cell_size, row * cell_size, cell_size, cell_size), 2)
            font = pygame.font.Font(None, 24)
            number = font.render(str(grid[row][col]), True, BLUE)
            number_rect = number.get_rect(center=(col * cell_size + cell_size // 2, row * cell_size + cell_size // 2))
            window.blit(number, number_rect)

            display_text("Solving...")
            pygame.display.update()
            time.sleep(0.1)  # Add a small delay for visualization

            if solve_sudoku():
                return True

            # Clear the number from the grid
            grid[row][col] = 0

         

    return False

def is_complete(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return False
    return True

def find_empty_cell(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return row, col
    return None, None

def is_valid(grid, row, col, num):
    # Check row
    for i in range(9):
        if grid[row][i] == num:
            return False
    
    # Check column
    for i in range(9):
        if grid[i][col] == num:
            return False
    
    # Check subgrid
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if grid[i][j] == num:
                return False
    
    return True




# Create a function to draw the Sudoku grid
def draw_grid():
    for i in range(grid_size + 1):
        if i % 3 == 0:
            line_thickness = 4
        else:
            line_thickness = 1

        pygame.draw.line(window, BLACK, (0, i * cell_size), (window_width, i * cell_size), line_thickness)
        pygame.draw.line(window, BLACK, (i * cell_size, 0), (i * cell_size, window_height-200), line_thickness)

# Create a function to draw the numbers on the grid
def draw_numbers():
    font = pygame.font.Font(None, 36)

    for row in range(grid_size):
        for col in range(grid_size):
            if grid[row][col] != 0:
                if user_input[row][col]:
                    text_color = BLUE
                else:
                    text_color = BLACK

                number = font.render(str(grid[row][col]), True, text_color)
                number_rect = number.get_rect(center=(col * cell_size + cell_size // 2, row * cell_size + cell_size // 2))
                window.blit(number, number_rect)

# Create a function to handle mouse clicks
def handle_mouse_click(position):
    row = position[1] // cell_size
    col = position[0] // cell_size

    if row < grid_size and col < grid_size:
        if user_input[row][col]:
            user_input[row][col] = 0
        else:
            user_input[row][col] = 1
# Create a function to update the grid with user input
def update_grid(row, col, value):
    if row < grid_size and col < grid_size:
        if solver.is_valid(grid, row, col, value):
            grid[row][col] = value
            return True
        else:
            return False
# Create a function to update the grid with user input
def delete_value(row, col, value):
    if solve_grid[row][col]==value:
        grid[row][col] = value
        

# Create a function to display text in the response area
def display_text(text):
    font = pygame.font.Font(None, 24)
    text_render = font.render(text, True, RED)
    text_rect = text_render.get_rect(center=(window_width // 2, window_height - 100))
    window.blit(text_render, text_rect)

def handle_button_click():
    
    if position[0] >= window_width - 120 and position[1] >= window_height - 50:
        # New Game button clicked
        #reset()
        generate_sudoku_puzzle()
        window.fill(WHITE)
        draw_grid()
        draw_numbers()
        display_text("New Game Started")
        pygame.display.update()
        time.sleep(1)  # Add a small delay for visualization
        


    elif position[0] >= window_width - 400 and position[1] >= window_height - 50:
        # Solve button clicked
        solved=check_grid()
        #solved = solve_sudoku()
        if solved:
            # Puzzle solved, update the grid and display it
            window.fill(WHITE)
            draw_grid()
            draw_numbers()
            display_text("Puzzle Solved!")
            pygame.display.update()
            time.sleep(1)  # Add a small delay for visualization
        else:
            # Puzzle unsolvable, display error message
            display_text("Puzzle is Unsolvable!")
            pygame.display.update()
            time.sleep(1)  # Add a small delay for visualization

    elif position[0] >= window_width - 675 and position[1] >= window_height - 50:
        # Quit button clicked
        pygame.quit()
        sys.exit()


# Set up the Sudoku grid
user_input = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
grid  = [[0] * 9 for _ in range(9)]
solve_grid=[[0] * 9 for _ in range(9)]

generate_sudoku_puzzle()
solvedPuzzle=solver.solve_sudoku(solve_grid)
# Create a copy of the original grid for solving
solve_grid = [row[:] for row in grid]

# Create a 2D list to store the user input

# Run the Pygame event loop
running = True
selected_cell = None
response_text = ""
solve_button_clicked = False
complete=False
position = pygame.mouse.get_pos()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                position = pygame.mouse.get_pos()
                selected_cell = position[1] // cell_size, position[0] // cell_size
                handle_button_click()
                
        elif event.type == pygame.KEYDOWN:
            if selected_cell is not None:
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    delete_value(selected_cell[0], selected_cell[1], 0)
                elif event.key >= pygame.K_1 and event.key <= pygame.K_9:
                    number = int(event.unicode)
                    response_text=""
                    update=update_grid(selected_cell[0], selected_cell[1], number)
                    if update == False:
                        response_text="The value "+str(number)+" is an invalid input for row "+str(selected_cell[0]+1)+" and column "+str(selected_cell[1]+1)

    window.fill(WHITE)
    draw_grid()
    draw_numbers()

    if selected_cell is not None:
        pygame.draw.rect(window, BLUE, (selected_cell[1] * cell_size, selected_cell[0] * cell_size, cell_size, cell_size), 2)


    # Draw the Solve button
    solve_button_rect = pygame.Rect(window_width - 400, window_height - 50, 100, 40)
    font = pygame.font.Font(None, 24)
    pygame.draw.rect(window, BLUE, solve_button_rect)
    solve_button_text = font.render("Solve", True, WHITE)
    solve_button_text_rect = solve_button_text.get_rect(center=solve_button_rect.center)
    window.blit(solve_button_text, solve_button_text_rect)

    # Draw the quit button
    quit_button_rect = pygame.Rect(window_width - 675, window_height - 50, 100, 40)
    font = pygame.font.Font(None, 24)
    pygame.draw.rect(window, RED, quit_button_rect)
    quit_button_text = font.render("Quit", True, WHITE)
    quit_button_text_rect = quit_button_text.get_rect(center=quit_button_rect.center)
    window.blit(quit_button_text, quit_button_text_rect)

    # Draw the new game button
    new_game_button_rect = pygame.Rect(window_width - 120, window_height - 50, 100, 40)
    font = pygame.font.Font(None, 24)
    pygame.draw.rect(window, GRAY, new_game_button_rect)
    new_game_button_text = font.render("New Game", True, WHITE)
    new_game_button_text_rect = new_game_button_text.get_rect(center=new_game_button_rect.center)
    window.blit(new_game_button_text, new_game_button_text_rect)

    display_text(response_text)

    pygame.display.update() 
pygame.quit()