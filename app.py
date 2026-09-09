import random
import tkinter as tk

# 게임 창 및 격자 크기 설정
CELL_SIZE = 30
COLUMNS = 10
ROWS = 20

# 색상 정의
COLORS = ["cyan", "blue", "orange", "yellow", "green", "purple", "red"]

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
    def __init__(self, root):
        self.root = root
        self.root.title("파이썬 테트리스 (Tkinter)")

        self.canvas = tk.Canvas(
            root,
            width=COLUMNS * CELL_SIZE,
            height=ROWS * CELL_SIZE,
            bg="black"
        )
        self.canvas.pack()

        self.grid = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.current_piece = None
        self.game_over = False

        # 키보드 이벤트 바인딩
        self.root.bind("<Left>", lambda e: self.move(-1))
        self.root.bind("<Right>", lambda e: self.move(1))
        self.root.bind("<Up>", lambda e: self.rotate())
        self.root.bind("<Down>", lambda e: self.drop())
        self.root.bind("<space>", lambda e: self.hard_drop())

        self.spawn_piece()
        self.update_game()

    def spawn_piece(self):
        idx = random.randint(0, len(SHAPES) - 1)
        self.current_piece = {
            'shape': SHAPES[idx],
            'color': COLORS[idx],
            'x': COLUMNS // 2 - len(SHAPES[idx][0]) // 2,
            'y': 0
        }
        if self.check_collision(self.current_piece['shape'], self.current_piece['x'], self.current_piece['y']):
            self.game_over = True

    def rotate_shape(self, shape):
        return [list(row) for row in zip(*shape[::-1])]

    def check_collision(self, shape, offset_x, offset_y):
        for r, row in enumerate(shape):
            for c, val in enumerate(row):
                if val:
                    nx, ny = offset_x + c, offset_y + r
                    if nx < 0 or nx >= COLUMNS or ny >= ROWS:
                        return True
                    if ny >= 0 and self.grid[ny][nx] is not None:
                        return True
        return False

    def lock_piece(self):
        shape = self.current_piece['shape']
        color = self.current_piece['color']
        x, y = self.current_piece['x'], self.current_piece['y']

        for r, row in enumerate(shape):
            for c, val in enumerate(row):
                if val:
                    if y + r < 0:
                        self.game_over = True
                        return
                    self.grid[y + r][x + c] = color

        self.clear_lines()
        self.spawn_piece()

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell is None for cell in row)]
        lines_cleared = ROWS - len(new_grid)
        for _ in range(lines_cleared):
            new_grid.insert(0, [None for _ in range(COLUMNS)])
        self.grid = new_grid

    def move(self, dx):
        if not self.game_over:
            nx = self.current_piece['x'] + dx
            if not self.check_collision(self.current_piece['shape'], nx, self.current_piece['y']):
                self.current_piece['x'] = nx
                self.draw()

    def rotate(self):
        if not self.game_over:
            rotated = self.rotate_shape(self.current_piece['shape'])
            if not self.check_collision(rotated, self.current_piece['x'], self.current_piece['y']):
                self.current_piece['shape'] = rotated
                self.draw()

    def drop(self):
        if not self.game_over:
            ny = self.current_piece['y'] + 1
            if not self.check_collision(self.current_piece['shape'], self.current_piece['x'], ny):
                self.current_piece['y'] = ny
            else:
                self.lock_piece()
            self.draw()

    def hard_drop(self):
        """스페이스바: 바닥으로 바로 내리기"""
        if not self.game_over:
            while not self.check_collision(self.current_piece['shape'], self.current_piece['x'], self.current_piece['y'] + 1):
                self.current_piece['y'] += 1
            self.lock_piece()
            self.draw()

    def update_game(self):
        if not self.game_over:
            self.drop()
            self.root.after(500, self.update_game)  # 0.5초마다 한 칸씩 하강

    def draw(self):
        self.canvas.delete("all")

        # 격자선 그리기
        for r in range(ROWS):
            for c in range(COLUMNS):
                self.canvas.create_rectangle(
                    c * CELL_SIZE, r * CELL_SIZE,
                    (c + 1) * CELL_SIZE, (r + 1) * CELL_SIZE,
                    outline="#222222"
                )

        # 고정된 블록 그리기
        for r in range(ROWS):
            for c in range(COLUMNS):
                if self.grid[r][c]:
                    self.canvas.create_rectangle(
                        c * CELL_SIZE + 1, r * CELL_SIZE + 1,
                        (c + 1) * CELL_SIZE - 1, (r + 1) * CELL_SIZE - 1,
                        fill=self.grid[r][c], outline=""
                    )

        # 현재 떨어지는 블록 그리기
        if self.current_piece and not self.game_over:
            shape = self.current_piece['shape']
            color = self.current_piece['color']
            px, py = self.current_piece['x'], self.current_piece['y']

            for r, row in enumerate(shape):
                for c, val in enumerate(row):
                    if val:
                        x1 = (px + c) * CELL_SIZE + 1
                        y1 = (py + r) * CELL_SIZE + 1
                        x2 = (px + c + 1) * CELL_SIZE - 1
                        y2 = (py + r + 1) * CELL_SIZE - 1
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

        if self.game_over:
            self.canvas.create_text(
                COLUMNS * CELL_SIZE // 2, ROWS * CELL_SIZE // 2,
                text="GAME OVER", fill="white", font=("Arial", 20, "bold")
            )


if __name__ == "__main__":
    root = tk.Tk()
    game = Tetris(root)
    root.mainloop()
