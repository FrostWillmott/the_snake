from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()

# Starting position for GameObjects
STARTING_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)


# Тут опишите все классы игры.
class GameObject:
    """Base class for game objects."""

    def __init__(self, body_color=None, border_color=None):
        """Initialize a game object with a color and a position."""
        self.body_color: tuple = body_color
        self.position: tuple = STARTING_POSITION
        self.border_color: tuple = border_color

    def draw(self):
        """
        Method to draw the game object.
        To be implemented in subclasses.
        """
        raise NotImplementedError(
            f'draw() to be implemented in subclass {self.__class__.__name__}')


class Snake(GameObject):
    """Class representing the snake in the game."""

    def __init__(
            self, body_color=SNAKE_COLOR, border_color=BORDER_COLOR
    ) -> None:
        """
        Initialize a snake
        with a color, length, positions, direction, and next direction.
        """
        super().__init__(body_color, border_color)
        self.length: int = 1
        self.positions: list = [self.position]
        self.last: None = None
        self.direction: tuple = RIGHT
        self.next_direction: None = None

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

        self.positions.insert(
            0, (x, y)
        )

        self.last: tuple = (
            self.positions.pop()
            if len(self.positions) > self.length
            else None)

    def reset(self) -> None:
        """Reset the snake to its initial state."""
        self.length: int = 1
        self.positions: list = [self.position]
        self.direction: tuple = choice([UP, DOWN, LEFT, RIGHT])

    def draw(self) -> None:
        """Draw the snake on the screen."""
        for position in self.positions[:-1]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, self.body_color, rect, 1)

        # Отрисовка головы змейки
        head_rect = pg.Rect(
            self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, self.body_color, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


class Apple(GameObject):
    """Class representing the apple in the game."""

    def __init__(
            self, body_color=APPLE_COLOR,
            border_color=BORDER_COLOR) -> None:
        """Initialize an apple with a color and a random position."""
        super().__init__(body_color, border_color)
        self.randomize_position()

    def randomize_position(self, occupied_positions=[STARTING_POSITION]) -> None:
        """Randomize the position of the apple."""
        while self.position in occupied_positions:
            self.position = (
                randint(0, GRID_WIDTH - GRID_SIZE) * GRID_SIZE,
                randint(0, GRID_HEIGHT - GRID_SIZE) * GRID_SIZE
            )

    def draw(self) -> None:
        """Draw the apple on the screen."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, self.border_color, rect, 1)


def update_direction(self) -> None:
    """Update the direction of the snake if the user changed it."""
    if self.next_direction:
        self.direction = self.next_direction
        self.next_direction = None


def handle_keys(game_object) -> None:
    """Function to handle user actions."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit


def main() -> None:
    """Main function to initialize PyGame and start the game loop."""
    # Инициализация PyGame:
    pg.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    # Тут опишите основную логику игры.
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() in snake.positions[2:]:
            snake.reset()
            apple.randomize_position()
            screen.fill(BOARD_BACKGROUND_COLOR)
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
