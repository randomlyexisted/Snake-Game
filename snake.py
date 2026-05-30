import pygame
import random

pygame.init()

def spawn_food():
    cols = play_width // cell_size
    rows = play_height // cell_size
    while True:
        food_x = play_x + random.randint(0, cols -1) * cell_size
        food_y = play_y + random.randint(0, rows-1) * cell_size
        if [food_x,food_y] not in snake:
            return [food_x, food_y]
        
def reset_game():
    global snake, snake_length, dir, score, game_over, food
    snake = [[play_x+10*cell_size, play_y+10*cell_size]]
    snake_length = 1
    dir = "right"
    score = 0
    game_over = False
    started = False
    food = spawn_food()

def draw_menu():
    window.fill(base_color)
    title_font = pygame.font.SysFont("arial", 60, bold=True)
    title_text = title_font.render("SNAKE", True, text_color)
    window.blit(title_text, (screen_width//2-title_text.get_width()//2, screen_height//2 - 100))

    sub_text = font.render("Press Enter to start", True, text_color)
    window.blit(sub_text, (screen_width//2 - sub_text.get_width()//2, screen_height//2))

    hint_text = font.render("Use Arrow Keys to move", True, text_color)
    window.blit(hint_text, (screen_width//2 - hint_text.get_width()//2, screen_height//2+50))
    pygame.display.update()

font = pygame.font.SysFont("arial", 30)
score = 0
try:
    with open("high_score.txt", "r") as f:
        high_score = int(f.read())
except:
    high_score =0


# Colors
base_color   = (13, 33, 55)
grid_color   = (26, 58, 82)
snake_color  = (0, 207, 255)
food_color   = (255, 107, 53)
text_color   = (224, 244, 255)

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
snake = [[play_x+10*cell_size, play_y+10*cell_size]]
snake_length = 1
dir = "right"
fps = 10

food = spawn_food()

clock = pygame.time.Clock()

while not exit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game = True;
        
    
        # Input update
        if event.type == pygame.KEYDOWN:
            # Start game from menu
            if event.key == pygame.K_RETURN and not started:
                started = True
            # Direction controls
            if event.key == pygame.K_RIGHT and dir in ("up", "down"):
                dir = "right"
            elif event.key == pygame.K_LEFT and dir in ("up", "down"):
                dir = "left"
            elif event.key == pygame.K_UP and dir in ("right", "left"):
                dir = "up"
            elif event.key == pygame.K_DOWN and dir in ("right", "left"):
                dir = "down"
            # Restart from game over
            elif event.key == pygame.K_r and game_over:
                # Reset
                reset_game()
                started = False # go back to menu

    if not started:
        draw_menu()
    elif not game_over:
        # Movement
        snake_x = snake[0][0]
        snake_y = snake[0][1]

        if dir == "right": 
            snake_x += cell_size
        elif dir == "left":
            snake_x -= cell_size
        elif dir == "up":
            snake_y -= cell_size
        elif dir == "down":
            snake_y += cell_size

        # Self collision
        if [snake_x, snake_y] in snake[1:]:
            game_over = True;
            if score > high_score:
                high_score = score
                with open("high_score.txt", "w") as f:
                    f.write(str(high_score))
        

        # Horizontal Wrap
        if snake_x >= play_x+play_width:
            snake_x = play_x
        elif snake_x < play_x:
            snake_x = play_x+play_width-cell_size

        # Vertical Wrap
        if snake_y >= play_y + play_height:
            snake_y = play_y
        elif snake_y < play_y:
            snake_y = play_y + play_height - cell_size
        
        snake.insert(0, [snake_x, snake_y])
        if len(snake) > snake_length:
            snake.pop()

        window.fill(base_color)

        # Food collision
        if [snake_x , snake_y] == food:
            snake_length += 1
            score += 1
            food = spawn_food()
        
        #Play Area
        pygame.draw.rect(window, grid_color, [play_x, play_y, play_width, play_height],3)
        
        # Vertical Lines
        for y in range(play_x, play_x+play_width, cell_size):
            pygame.draw.line(window, grid_color, (y, play_y), (y, play_y+play_height))
        # Horizontal Lines
        for x in range(play_y, play_y+play_height, cell_size):
            pygame.draw.line(window, grid_color, (play_x ,x), (play_x+play_width, x))
        # Snake
        for segment in snake:
            pygame.draw.rect(window, snake_color, [segment[0], segment[1], cell_size, cell_size])
        # Food
        pygame.draw.rect(window, food_color, [food[0], food[1], cell_size, cell_size])
        # Score
        score_text = font.render(f"Score: {score}", True, text_color)
        high_score_text = font.render(f"High Score: {high_score}", True, text_color)
        window.blit(score_text, (play_x, 10))
        window.blit(high_score_text,(play_x + play_width-high_score_text.get_width(), 10))
        pygame.display.update()
        

    else:
        window.fill(base_color)
        over_text = font.render(f"Game Over! Score: {score}", True, text_color)
        high_score_text = font.render(f"High Score: {high_score}", True, text_color)
        restart_text = font.render("Press R to Restart", True, text_color)
        window.blit(over_text, (screen_width//2 - over_text.get_width()//2, screen_height//2 -50))
        window.blit(high_score_text, (screen_width//2 -high_score_text.get_width()//2, screen_height//2 - 10))
        window.blit(restart_text, (screen_width//2 - restart_text.get_width()//2, screen_height//2 + 30))
        pygame.display.update()
    
    clock.tick(fps)
