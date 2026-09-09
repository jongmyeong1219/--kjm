import random
import pygame

# 초기화
pygame.init()

# 화면 크기 설정 (10칸 x 20칸)
CELL_SIZE = 30
COLUMNS = 10
ROWS = 20
SCREEN_WIDTH = CELL_SIZE * COLUMNS
SCREEN_HEIGHT = CELL_SIZE * ROWS

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("파이썬 테트리스")

# 색상 정의
BLACK = (0, 0, 0)
GRAY = (40, 40, 40)
COLORS = [
    (0, 255, 255),  # I: 청록
    (0, 0, 255),    # J: 파랑
    (255, 165, 0),  # L: 주황
    (255, 255, 0),  # O: 노랑
    (0, 255, 0),    # S: 초록
    (128, 0, 128),  # T: 보라
    (255, 0, 0),    # Z: 빨강
]

# 테트리미노 블록 형태
SHAPES = [
    [[1, 1, 1, 1]],          # I
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
    [[1, 1], [1, 1]],        # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # Z
]


class Tetris:
    def __init__(self):
        self.grid = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.current_piece = self.new_piece()
        self.game_over = False
        self.score = 0

    def new_piece(self):
        idx = random.randint(0, len(SHAPES) - 1)
        shape = SHAPES[idx]
        color = COLORS[idx]
        x = COLUMNS // 2 - len(shape[0]) // 2
        y = 0
        return {'shape': shape, 'color': color, 'x': x, 'y': y}

    def rotate_piece(self, shape):
        return [list(row) for row in zip(*shape[::-1])]

    def check_collision(self, shape, offset_x, offset_y):
        for r, row in enumerate(shape):
            for c, val in enumerate(row):
                if val:
                    new_x = offset_x + c
                    new_y = offset_y + r
                    if new_x < 0 or new_x >= COLUMNS or new_y >= ROWS:
                        return True
                    if new_y >= 0 and self.grid[new_y][new_x]:
                        return True
        return False

    def lock_piece(self):
        shape = self.current_piece['shape']
        color = self.current_piece['color']
        x = self.current_piece['x']
        y = self.current_piece['y']

        for r, row in enumerate(shape):
            for c, val in enumerate(row):
                if val:
                    if y + r < 0:
                        self.game_over = True
                        return
                    self.grid[y + r][x + c] = color

        self.clear_lines()
        self.current_piece = self.new_piece()
        if self.check_collision(self.current_piece['shape'], self.current_piece['x'], self.current_piece['y']):
            self.game_over = True

    def clear_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.grid) if all(row)]
        for index in lines_to_clear:
            del self.grid[index]
            self.grid.insert(0, [0 for _ in range(COLUMNS)])
            self.score += 100

    def move(self, dx):
        if not self.game_over:
            new_x = self.current_piece['x'] + dx
            if not self.check_collision(self.current_piece['shape'], new_x, self.current_piece['y']):
                self.current_piece['x'] = new_x

    def drop(self):
        if not self.game_over:
            new_y = self.current_piece['y'] + 1
            if not self.check_collision(self.current_piece['shape'], self.current_piece['x'], new_y):
                self.current_piece['y'] = new_y
            else:
                self.lock_piece()

    def hard_drop(self):
        """스페이스바: 즉시 바닥으로 떨어트리기"""
        if not self.game_over:
            while not self.check_collision(self.current_piece['shape'], self.current_piece['x'], self.current_piece['y'] + 1):
                self.current_piece['y'] += 1
            self.lock_piece()

    def rotate(self):
        if not self.game_over:
            rotated = self.rotate_piece(self.current_piece['shape'])
            if not self.check_collision(rotated, self.current_piece['x'], self.current_piece['y']):
                self.current_piece['shape'] = rotated


def main():
    clock = pygame.time.Clock()
    game = Tetris()
    fall_time = 0
    fall_speed = 0.5

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        fall_time += dt

        if fall_time >= fall_speed:
            game.drop()
            fall_time = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move(-1)
                elif event.key == pygame.K_RIGHT:
                    game.move(1)
                elif event.key == pygame.K_DOWN:
                    game.drop()
                elif event.key == pygame.K_UP:
                    game.rotate()
                elif event.key == pygame.K_SPACE:
                    game.hard_drop()  # 스페이스바 조작 추가

        SCREEN.fill(BLACK)

        # 격자선 그리기
        for r in range(ROWS):
            pygame.draw.line(SCREEN, GRAY, (0, r * CELL_SIZE), (SCREEN_WIDTH, r * CELL_SIZE))
        for c in range(COLUMNS):
            pygame.draw.line(SCREEN, GRAY, (c * CELL_SIZE, 0), (c * CELL_SIZE, SCREEN_HEIGHT))

        # 고정된 블록 그리기
        for r in range(ROWS):
            for c in range(COLUMNS):
                color = game.grid[r][c]
                if color:
                    pygame.draw.rect(
                        SCREEN,
                        color,
                        (c * CELL_SIZE + 1, r * CELL_SIZE + 1, CELL_SIZE - 2, CELL_SIZE - 2)
                    )

        # 현재 떨어지는 블록 그리기
        if not game.game_over:
            piece = game.current_piece
            shape = piece['shape']
            color = piece['color']
            for r, row in enumerate(shape):
                for c, val in enumerate(row):
                    if val:
                        px = (piece['x'] + c) * CELL_SIZE + 1
                        py = (piece['y'] + r) * CELL_SIZE + 1
                        pygame.draw.rect(SCREEN, color, (px, py, CELL_SIZE - 2, CELL_SIZE - 2))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
