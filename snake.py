import pygame
import random

pygame.init()

# Screen size
WIDTH = 600
HEIGHT = 400
BLOCK_SIZE = 20

# Colors
WHITE = (255, 255, 255)
GRAY = (160, 160, 160)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game 🐍")

# Clock
clock = pygame.time.Clock()

# Fonts
menu_font = pygame.font.SysFont("Futura", 24, bold=True)
small_font = pygame.font.SysFont("Futura", 14)
score_font = pygame.font.SysFont("Futura", 18)
game_over_font = pygame.font.SysFont("Futura", 48, bold=True)
sub_font = pygame.font.SysFont("Futura", 22)

# Global unlock flag
impossible_unlocked = False


def draw_snake(snake_list):
    for x, y in snake_list:
        pygame.draw.rect(screen, GREEN, [x, y, BLOCK_SIZE, BLOCK_SIZE])


def show_score(score):
    score_text = score_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH - 120, 10))


def game_loop(fps, mode):
    global impossible_unlocked
    game_over = False

    # Snake start position
    x = WIDTH // 2
    y = HEIGHT // 2
    dx = 0
    dy = 0

    snake_list = []
    snake_length = 1

    # Food position
    food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

    while True:
        if game_over:
            screen.fill(BLACK)

            # Main "GAME OVER!" text
            over_text = game_over_font.render("GAME OVER!", True, RED)
            over_rect = over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
            screen.blit(over_text, over_rect)

            # Restart instructions
            sub_text = sub_font.render("Press space to return to menu", True, WHITE)
            sub_rect = sub_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
            screen.blit(sub_text, sub_rect)

            pygame.display.update()

            # Unlock check
            if mode == "Hard" and snake_length - 1 >= 30:
                impossible_unlocked = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return  # return to menu

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and dx == 0:
                        dx = -BLOCK_SIZE
                        dy = 0
                    elif event.key == pygame.K_RIGHT and dx == 0:
                        dx = BLOCK_SIZE
                        dy = 0
                    elif event.key == pygame.K_UP and dy == 0:
                        dx = 0
                        dy = -BLOCK_SIZE
                    elif event.key == pygame.K_DOWN and dy == 0:
                        dx = 0
                        dy = BLOCK_SIZE

            # Move snake
            x += dx
            y += dy

            # Check boundaries
            if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
                game_over = True

            screen.fill(BLACK)
            pygame.draw.rect(screen, RED, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])

            snake_head = [x, y]
            snake_list.append(snake_head)
            if len(snake_list) > snake_length:
                del snake_list[0]

            # Check self collision
            for segment in snake_list[:-1]:
                if segment == snake_head:
                    game_over = True

            draw_snake(snake_list)
            show_score(snake_length - 1)

            pygame.display.update()

            # Food collision
            if x == food_x and y == food_y:
                food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
                food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
                snake_length += 1

            clock.tick(fps)


def menu():
    while True:
        screen.fill(BLACK)

        # Title
        title_text = pygame.font.SysFont("Futura", 56, bold=True).render("SNAKE", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 50))
        screen.blit(title_text, title_rect)

        subtitle_text = pygame.font.SysFont("Futura", 20).render("Remade by Luke Labib", True, WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(WIDTH // 2, 90))
        screen.blit(subtitle_text, subtitle_rect)

        # Menu option boxes
        easy_box = pygame.Rect(200, 120, 200, 40)
        amat_box = pygame.Rect(200, 180, 200, 40)
        hard_box = pygame.Rect(200, 240, 200, 40)
        imp_box = pygame.Rect(200, 300, 200, 40)

        # Draw outlines (transparent inside)
        pygame.draw.rect(screen, WHITE, easy_box, 2)
        pygame.draw.rect(screen, WHITE, amat_box, 2)
        pygame.draw.rect(screen, WHITE, hard_box, 2)

        if impossible_unlocked:
            pygame.draw.rect(screen, WHITE, imp_box, 2)
        else:
            pygame.draw.rect(screen, GRAY, imp_box, 2)

        # Text labels INSIDE boxes
        easy_text = menu_font.render("Easy Mode", True, WHITE)
        amat_text = menu_font.render("Amateur Mode", True, WHITE)
        hard_text = menu_font.render("Hard Mode", True, WHITE)
        imp_text = menu_font.render("Impossible Mode", True, WHITE if impossible_unlocked else GRAY)

        screen.blit(easy_text, easy_text.get_rect(center=easy_box.center))
        screen.blit(amat_text, amat_text.get_rect(center=amat_box.center))
        screen.blit(hard_text, hard_text.get_rect(center=hard_box.center))
        screen.blit(imp_text, imp_text.get_rect(center=imp_box.center))

        # Subtext under Impossible box
        if not impossible_unlocked:
            imp_sub = small_font.render("Unlocked after reaching score 30 in Hard Mode", True, WHITE)
            screen.blit(imp_sub, imp_sub.get_rect(center=(WIDTH // 2, imp_box.bottom + 20)))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_box.collidepoint(event.pos):
                    game_loop(5, "Easy")
                elif amat_box.collidepoint(event.pos):
                    game_loop(10, "Amateur")
                elif hard_box.collidepoint(event.pos):
                    game_loop(15, "Hard")
                elif imp_box.collidepoint(event.pos) and impossible_unlocked:
                    game_loop(25, "Impossible")


# Run
menu()
