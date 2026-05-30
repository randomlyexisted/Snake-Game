import pygame
import random

pygame.init()

def spawn_food():
    cols = play_width // cell_size
    rows = play_height // cell_size
    while True:
        food_x = play_x + random.randint(0, cols -1) * cell_size
        food_y = play_y + random.randint(0, rows-1) * cell_size
        if [food_x,food_y] not in snake1 and [food_x, food_y] not in snake2:
            return [food_x, food_y]
        
def reset_game():
    global snake1, snake2, snake1_length, snake2_length, dir1, dir2, score1, score2, game_over, started, food
    snake1 = [[play_x+5*cell_size, play_y+12*cell_size]]
    snake1_length = 1
    snake2 = [[play_x + 24 * cell_size, play_y + 12*cell_size]]
    snake2_length = 1
    dir1 = "right"
    dir2 = "left"
    score1 = 0
    score2 = 0
    game_over = False
    started = True
    food = spawn_food()

def draw_menu():
    window.fill(base_color)
    title_font = pygame.font.SysFont("arial", 60, bold=True)
    title_text = title_font.render("SNAKE", True, text_color)
    window.blit(title_text, (screen_width//2-title_text.get_width()//2, screen_height//2 - 100))

    sub_text = font.render("Press Enter to start", True, text_color)
    window.blit(sub_text, (screen_width//2 - sub_text.get_width()//2, screen_height//2))

    hint1_text = font.render("Use Arrow Keys to move Snake1", True, text_color)
    window.blit(hint1_text, (screen_width//2 - hint1_text.get_width()//2, screen_height//2+50))
    
    hint2_text = font.render("Use WASD keys to move Snake2", True, text_color)
    window.blit(hint2_text, (screen_width//2 - hint2_text.get_width()//2, screen_height//2+80))
    pygame.display.update()

font = pygame.font.SysFont("arial", 30)

base_color    = (13, 33, 55)
grid_color    = (26, 58, 82)
snake1_color  = (0, 207, 255)
snake2_color  = (123, 47, 255)
food_color    = (255, 107, 53)
text_color    = (224, 244, 255)

screen_width = 800
screen_height = 600
window = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Snake")
pygame.display.update()

exit_game = False
game_over = False
started = False
play_x = 100
play_y = 50
play_width = 600
play_height = 500
cell_size = 20

snake1 = [[play_x+5*cell_size, play_y+12*cell_size]]
snake1_length = 1
snake2 = [[play_x+24*cell_size, play_y+12*cell_size]]
snake2_length = 1

dir1 = "right"
dir2 = "left"

score1 =0
score2 = 0

winner = ""

fps = 10

food = spawn_food()

clock = pygame.time.Clock()

while not exit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game = True;

        if event.type == pygame.KEYDOWN:
            # Start game from menu
            if event.key == pygame.K_RETURN and not started:
                started = True
            # Restart from game over
            elif event.key == pygame.K_r and game_over:
                # Reset
                reset_game()
            
            # Direction controls for Snake1
            if event.key == pygame.K_RIGHT and dir1 in ("up", "down"):
                dir1 = "right"
            elif event.key == pygame.K_LEFT and dir1 in ("up", "down"):
                dir1 = "left"
            elif event.key == pygame.K_UP and dir1 in ("right", "left"):
                dir1 = "up"
            elif event.key == pygame.K_DOWN and dir1 in ("right", "left"):
                dir1 = "down"
            


            # Direction controls for snake2
            if event.key == pygame.K_d and dir2 in ("up", "down"):
                dir2 = "right"
            elif event.key == pygame.K_a and dir2 in ("up", "down"):
                dir2 = "left"
            elif event.key == pygame.K_w and dir2 in ("right", "left"):
                dir2 = "up"
            elif event.key == pygame.K_s and dir2 in ("right", "left"):
                dir2 = "down"

    if not started:
        draw_menu()

    elif not game_over:
        # Movement
        snake1_x = snake1[0][0]
        snake1_y = snake1[0][1]
        snake2_x = snake2[0][0]
        snake2_y = snake2[0][1]

        if dir1 == "right": 
            snake1_x += cell_size
        elif dir1 == "left":
            snake1_x -= cell_size
        elif dir1 == "up":
            snake1_y -= cell_size
        elif dir1 == "down":
            snake1_y += cell_size
        
        if dir2 == "right": 
            snake2_x += cell_size
        elif dir2 == "left":
            snake2_x -= cell_size
        elif dir2 == "up":
            snake2_y -= cell_size
        elif dir2 == "down":
            snake2_y += cell_size

        # Collision
        s1_dead = (snake1_x < play_x or snake1_x >= play_x+play_width or
           snake1_y < play_y or snake1_y >= play_y+play_height or
           [snake1_x, snake1_y] in snake1[1:] or [snake1_x, snake1_y] in snake2)

        s2_dead = (snake2_x < play_x or snake2_x >= play_x+play_width or
                snake2_y < play_y or snake2_y >= play_y+play_height or
                [snake2_x, snake2_y] in snake2[1:] or [snake2_x, snake2_y] in snake1)

        if s1_dead and s2_dead:
            game_over = True
            winner = "Draw"
        elif s1_dead:
            game_over = True
            winner = "Player 2"
        elif s2_dead:
            game_over = True
            winner = "Player 1"

        snake1.insert(0, [snake1_x, snake1_y])
        if len(snake1) > snake1_length:
            snake1.pop()
        
        snake2.insert(0, [snake2_x, snake2_y])
        if len(snake2) > snake2_length:
            snake2.pop()
        
        window.fill(base_color)

        # Food collision
        if [snake1_x , snake1_y] == food:
            snake1_length += 1
            score1 += 1
            food = spawn_food()
        elif [ snake2_x, snake2_y] == food:
            snake2_length += 1
            score2 += 1
            food = spawn_food()

        #Play Area
        pygame.draw.rect(window, grid_color, [play_x, play_y, play_width, play_height],3)
            
        # Vertical Lines
        for y in range(play_x, play_x+play_width, cell_size):
            pygame.draw.line(window, grid_color, (y, play_y), (y, play_y+play_height))
        # Horizontal Lines
        for x in range(play_y, play_y+play_height, cell_size):
            pygame.draw.line(window, grid_color, (play_x ,x), (play_x+play_width, x))
        # Snake1
        for segment in snake1:
            pygame.draw.rect(window, snake1_color, [segment[0], segment[1], cell_size, cell_size])
        # Snake2
        for segment in snake2:
            pygame.draw.rect(window, snake2_color, [segment[0], segment[1], cell_size, cell_size])
        # Food
        pygame.draw.rect(window, food_color, [food[0], food[1], cell_size, cell_size])
        score1_text = font.render(f"P1: {score1}",True, snake1_color)
        score2_text = font.render(f"P2: {score2}", True, snake2_color)
        window.blit(score1_text, (play_x, 10))
        window.blit(score2_text, (play_x + play_width - score2_text.get_width(), 10))
        pygame.display.update()
    else:
        window.fill(base_color)
        win_text = font.render(f"{winner} Wins!" if winner != "Draw" else "It's a Draw!", True, text_color)
        score_text = font.render(f"P1: {score1} | P2: {score2}", True, text_color)
        restart_text = font.render("Press R to restart", True, text_color)
        window.blit(win_text, (screen_width//2 - win_text.get_width()//2, screen_height//2 - 50))
        window.blit(score_text, (screen_width//2 - score_text.get_width()//2, screen_height//2))
        window.blit(restart_text, (screen_width//2-restart_text.get_width()//2, screen_height//2 + 50))
        pygame.display.update()
    
    clock.tick(fps)