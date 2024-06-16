from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP: tuple = (0, -1)
DOWN: tuple = (0, 1)
LEFT: tuple = (-1, 0)
RIGHT: tuple = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR: tuple = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR: tuple = (93, 216, 228)

# Цвет яблока
APPLE_COLOR: tuple = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR: tuple = (0, 255, 0)

# Скорость движения змейки:
SPEED: int = 5

# Настройка игрового окна:
screen: object = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock: object = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Base class for game objects."""

    def __init__(self, body_color=None):
        self.body_color: tuple = body_color
        self.position: tuple = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        """Initialize a game object with a color and a position."""

    def draw(self):
        """Method to draw the game object. To be implemented in subclasses."""
        pass


class Snake(GameObject):
    """Class representing the snake in the game."""

    def __init__(self) -> None:
        """
        Initialize a snake
        with a color, length, positions, direction, and next direction.
        """
        super().__init__(body_color=SNAKE_COLOR)
        self.length: int = 1
        self.positions: list = [self.position]
        self.last: None = None
        self.direction: tuple = RIGHT
        self.next_direction: None = None
        self.body_color: tuple = SNAKE_COLOR
        self.last: None = None

    def update_direction(self) -> None:
        """Update the direction of the snake if there is a next direction."""
        if self.next_direction:
            self.direction: tuple = self.next_direction
            self.next_direction: None = None

    def get_head_position(self) -> tuple:
        """Get the position of the head of the snake."""
        return self.positions[0]

    def move(self) -> None:
        """Move the snake in the current direction."""
        x, y = self.get_head_position()
        dx, dy = self.direction
        x += dx * GRID_SIZE
        y += dy * GRID_SIZE
        x = x % SCREEN_WIDTH
        y = y % SCREEN_HEIGHT
        for i in range(2, len(self.positions)):
            if self.positions[i] == (x, y):
                self.reset()
                return
        self.positions.insert(0, (x, y))

        # print(self.positions)
        if len(self.positions) > self.length:
            self.last: tuple = self.positions.pop()

    def reset(self) -> None:
        """Reset the snake to its initial state."""
        self.length: int = 1
        self.positions: list = [self.position]
        self.direction: tuple = choice([UP, DOWN, LEFT, RIGHT])

    def draw(self) -> None:
        """Draw the snake on the screen."""
        for position in self.positions[:-1]:
            rect: tuple = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect: tuple = pygame.Rect(
            self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect: tuple = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


class Apple(GameObject):
    """Class representing the apple in the game."""

    def __init__(self) -> None:
        """Initialize an apple with a color and a random position."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self) -> None:
        """Randomize the position of the apple."""
        self.position: tuple = (
            randint(0, (GRID_WIDTH - GRID_SIZE)) * GRID_SIZE,
            randint(0, (GRID_HEIGHT - GRID_SIZE)) * GRID_SIZE
        )
        # print(self.position)

    def draw(self) -> None:
        """Draw the apple on the screen."""
        rect: tuple = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def update_direction(self) -> None:
    """Update the direction of the snake if the user changed it."""
    if self.next_direction:
        self.direction = self.next_direction
        self.next_direction = None


def handle_keys(game_object) -> None:
    """Function to handle user actions."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main() -> None:
    """Main function to initialize PyGame and start the game loop."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple: object = Apple()
    apple.draw()
    pygame.display.update()
    snake: object = Snake()
    snake.draw()
    pygame.display.update()

    # Тут опишите основную логику игры.
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
