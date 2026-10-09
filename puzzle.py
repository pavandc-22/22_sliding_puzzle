
import random


class Puzzle:
    def __init__(self, size=4):
        self.size = size
        self.board = self.make_board()

    def make_board(self):
        # Start from the solved arrangement so every generated board is solvable.
        tiles = list(range(1, self.size * self.size)) + [0]
        board = [
            tiles[r * self.size:(r + 1) * self.size]
            for r in range(self.size)
        ]

        # Scramble by making legal moves of the blank (0).
        blank_r, blank_c = self.size - 1, self.size - 1
        previous_blank = None
        scramble_moves = max(100, self.size * self.size * 20)

        for _ in range(scramble_moves):
            neighbors = []

            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = blank_r + dr, blank_c + dc

                if 0 <= nr < self.size and 0 <= nc < self.size:
                    # Avoid immediately undoing the previous move.
                    if (nr, nc) != previous_blank:
                        neighbors.append((nr, nc))

            if not neighbors and previous_blank is not None:
                neighbors = [previous_blank]

            if not neighbors:
                # A 1x1 board has no legal moves.
                break

            next_r, next_c = random.choice(neighbors)

            board[blank_r][blank_c], board[next_r][next_c] = (
                board[next_r][next_c],
                board[blank_r][blank_c],
            )

            previous_blank = (blank_r, blank_c)
            blank_r, blank_c = next_r, next_c

        return board

    def blank_pos(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    return r, c

    def move(self, direction):
        r, c = self.blank_pos()

        dr, dc = {
            "w": (-1, 0),
            "s": (1, 0),
            "a": (0, -1),
            "d": (0, 1),
        }[direction]

        nr, nc = r + dr, c + dc

        if not (0 <= nr < self.size and 0 <= nc < self.size):
            return False

        self.board[r][c], self.board[nr][nc] = (
            self.board[nr][nc],
            self.board[r][c],
        )
        return True

    def solved(self):
        return sum(self.board, []) == (
            list(range(1, self.size * self.size)) + [0]
        )