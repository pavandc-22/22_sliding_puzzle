
import time
from puzzle import Puzzle


class SlidingPuzzle:
    def __init__(self, size=4):
        if size not in (3, 4, 5):
            raise ValueError("Puzzle size must be 3, 4, or 5.")

        self.size = size
        self.puzzle = Puzzle(self.size)
        self.moves = 0
        self.started = time.monotonic()
        self.won = False
        self.finished_at = None

    def elapsed_time(self):
        """Return elapsed seconds, frozen when the game is won."""
        end_time = (
            self.finished_at
            if self.finished_at is not None
            else time.monotonic()
        )
        return int(end_time - self.started)

    def display(self):
        print()
        for row in self.puzzle.board:
            print(" ".join(f"{x or ' ':>2}" for x in row))
        print("Moves:", self.moves, " Time:", self.elapsed_time(), "s")

    def _finish(self):
        # Make victory feedback idempotent: announce it only once.
        if not self.won:
            self.won = True
            self.finished_at = time.monotonic()
            self.display()
            print("Congratulations! You solved the puzzle!")

    def run(self):
        # A completed game cannot be resumed or announce victory again.
        if self.won:
            return

        print(
            f"Sliding Puzzle ({self.size}x{self.size}) — "
            "W/A/S/D moves the tile into the blank. Q quits."
        )

        # Preserve Task 2 behavior for a board already solved before input.
        if self.puzzle.solved():
            self._finish()
            return

        while not self.won:
            self.display()
            key = input("> ").strip().lower()

            if key == "q":
                return
            if key not in {"w", "a", "s", "d"}:
                print("Use W/A/S/D.")
                continue

            # A move is successful only when the board actually changes.
            moved = self.puzzle.move(key)

            if not moved:
                print("That move is not possible.")
                continue

            # Only successful moves reach this point.
            self.moves += 1

            # Check for victory only after a successful movement.
            if self.puzzle.solved():
                self._finish()
                return