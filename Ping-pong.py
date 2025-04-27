import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 700, 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 15

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пинг-Понг")

font = pygame.font.Font(None, 74)
menu_font = pygame.font.Font(None, 50)

ball_speed = 5


class Paddle:
    def __init__(self, x):
        self.rect = pygame.Rect(x, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, dy):
        self.rect.y += dy
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT


class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2,
                                HEIGHT // 2 - BALL_SIZE // 2,
                                BALL_SIZE,
                                BALL_SIZE)
        self.dx = ball_speed * (-1) ** (pygame.time.get_ticks() % 2)
        self.dy = ball_speed * (-1) ** (pygame.time.get_ticks() % 2)

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.dy *= -1


def reset_game():
    global score_left, score_right
    score_left = score_right = 0
    ball.reset()


def show_message(message, color=WHITE):
    text = font.render(message, True, color)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)


def check_win():
    global score_left, score_right
    if score_left >= 6:
        show_message('Победил левый игрок!', GREEN)
    elif score_right >= 6:
        show_message('Победил правый игрок!', RED)

    if score_left >= 6 or score_right >= 6:
        reset_game()


def show_menu():
    options = ["Играть", "Настройки", "Выход"]
    selected_option = 0

    while True:
        screen.fill(BLACK)

        title_text = font.render("Пинг-Понг", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

        for i, option in enumerate(options):
            color = WHITE if i == selected_option else (150, 150, 150)
            option_text = menu_font.render(option, True, color)
            screen.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, HEIGHT // 2 + i * 50 - 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_UP:
                    selected_option -= 1
                    if selected_option < 0:
                        selected_option = len(options) - 1
                elif event.key == pygame.K_DOWN:
                    selected_option += 1
                    if selected_option >= len(options):
                        selected_option = 0
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        return 'play'
                    elif selected_option == len(options) - 1:
                        pygame.quit()
                        sys.exit()
                    elif selected_option == 1:
                        show_settings()

        pygame.display.flip()


def show_settings():
    global ball_speed

    while True:
        screen.fill(BLACK)

        title_text = font.render("Настройки", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

        speed_text = menu_font.render(f"Скорость мяча: {ball_speed}", True, WHITE)
        screen.blit(speed_text, (WIDTH // 2 - speed_text.get_width() // 2, HEIGHT // 3))

        back_text = menu_font.render("Назад", True, WHITE)
        screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT // 3 + 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 50)).collidepoint(event.pos):
                    return
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    ball_speed += 1
                elif event.y < 0:
                    ball_speed = max(ball_speed - 1, 1)

        pygame.display.flip()


paddle_left = Paddle(30)
paddle_right = Paddle(WIDTH - PADDLE_WIDTH - 30)
ball = Ball()

score_left = score_right = 0

clock = pygame.time.Clock()

running = True
while running:

    action = show_menu()

    if action == 'play':
        playing = True
        while playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        playing = False
                        break

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                paddle_left.move(-10)
            if keys[pygame.K_s]:
                paddle_left.move(10)
            if keys[pygame.K_UP]:
                paddle_right.move(-10)
            if keys[pygame.K_DOWN]:
                paddle_right.move(10)

            ball.move()

            if ball.rect.colliderect(paddle_left.rect) or ball.rect.colliderect(paddle_right.rect):
                ball.dx *= -1

            if ball.rect.left <= 0:
                score_right += 1
                ball.reset()
            elif ball.rect.right >= WIDTH:
                score_left += 1
                ball.reset()


            check_win()

            screen.fill(BLACK)

            score_text = font.render(f"{score_left} : {score_right}", True, WHITE)
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

            pygame.draw.rect(screen, WHITE, paddle_left.rect)
            pygame.draw.rect(screen, WHITE, paddle_right.rect)
            pygame.draw.ellipse(screen, WHITE, ball.rect)

            pygame.display.flip()

            clock.tick(60)

pygame.quit()
sys.exit()