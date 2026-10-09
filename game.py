
import time
from puzzle import Puzzle


class SlidingPuzzle:
    def __init__(self):
        self.size = 4
        self.puzzle = Puzzle(self.size)
        self.moves = 0
        self.started = time.monotonic()
        self.won = False

    def display(self):
        print()
        for row in self.puzzle.board:
            print(" ".join(f"{x or ' ':>2}" for x in row))
        print(
            "Moves:", self.moves,
            " Time:", int(time.monotonic() - self.started), "s"
        )

    def run(self):
        # Prevent restarting a game that has already been won.
        if self.won:
            return

        print(
            "Sliding Puzzle — W/A/S/D moves the tile into the blank. Q quits."
        )

        # Handle a board that is already solved before the first input.
        if self.puzzle.solved():
            self.display()
            self.won = True
            print("Congratulations! You solved the puzzle!")
            return

        while True:
            self.display()
            key = input("> ").strip().lower()

            if key == "q":
                return

            if key not in "wasd":
                print("Use W/A/S/D.")
                continue

            if self.puzzle.move(key):
                self.moves += 1

                # Check immediately after every successful move.
                if self.puzzle.solved():
                    self.display()
                    self.won = True
                    print("Congratulations! You solved the puzzle!")
                    return
            else:
                print("That move is not possible.")