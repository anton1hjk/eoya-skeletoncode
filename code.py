import random

EMPTY_STRING = ""
SPACE = ' '
GRID_SIZE = 9 

class Cell:
    def __init__(self):
        self.value = SPACE

    def update(self, value):
        self.value = value

    def reset(self):
        self.value = SPACE

    def get_value(self):
        return self.value

class Puzzle:
    def __init__(self):
        self.reset()

    def reset(self):
        self.grid = [[Cell() for _ in range(GRID_SIZE + 1)] for _ in range(GRID_SIZE + 1)]
        self.puzzle = [EMPTY_STRING for _ in range(GRID_SIZE * GRID_SIZE)]
        self.solution = [EMPTY_STRING for _ in range(GRID_SIZE + 1)]
        self.answer = [EMPTY_STRING for _ in range(2 * GRID_SIZE * GRID_SIZE)]
        self.name = ""

    def load_puzzle_file(self):
        try:
            with open(f"{self.name}.txt", "r") as f:
                line_num = 0
                for line in f:
                    line = line.strip()
                    self.puzzle[line_num] = line
                    line_num += 1

            if line_num == 0:
                print("Puzzle file empty")
                return False

            return True
        except:
            print("Puzzle file does not exist")
            return False

    def load_solution(self):
        try:
            with open(f"{self.name}S.txt", "r") as f:
                for i in range(1, GRID_SIZE + 1):
                    self.solution[i] = SPACE + f.readline().strip()

                    if len(self.solution[i]) != GRID_SIZE + 1:
                        print("File data error")
                        return False
            return True
        except:
            print("Solution file does not exist")
            return False

    def transfer_puzzle_into_grid(self):
        try:
            i = 0
            while self.puzzle[i] != EMPTY_STRING:
                cell = self.puzzle[i]
                row = int(cell[0])
                column = int(cell[1])
                digit = cell[2]
                self.grid[row][column].update(digit)
                i += 1

            self.grid[0][0].update('X')
            self.reset_answer()
            return True

        except:
            print("Error in puzzle file")
            return False

    def load(self):
        self.reset()
        self.name = input("Enter puzzle name to load: ")

        if not self.load_puzzle_file():
            return False

        if not self.load_solution():
            return False

        if not self.transfer_puzzle_into_grid():
            return False

        return True

    def reset_answer(self):
        self.answer[0] = self.name
        self.answer[1] = "0"
        self.answer[2] = "0"
        for i in range(3, len(self.answer)):
            self.answer[i] = EMPTY_STRING

    def transfer_answer_into_grid(self):
        for i in range(3, int(self.answer[2]) + 3):
            cell = self.answer[i]
            row = int(cell[0])
            column = int(cell[1])
            digit = cell[2]
            self.grid[row][column].update(digit)

    def load_partial(self):
        if not self.load():
            return

        try:
            with open(f"{self.name}P.txt", "r") as f:
                first_line = f.readline().strip()

                if first_line != self.name:
                    print("Partial solution file is corrupt")
                    return

                i = 0
                self.answer[i] = first_line

                for line in f:
                    i += 1
                    self.answer[i] = line.strip()

            self.transfer_answer_into_grid()

        except:
            print("Partial solution file does not exist")

    def save_partial(self):
        if self.grid[0][0].get_value() != 'X':
            print("No puzzle loaded")
            return

        if int(self.answer[2]) == 0:
            print("No answers to keep")
            return

        with open(f"{self.name}P.txt", "w") as f:
            for i in range(int(self.answer[2]) + 3):
                f.write(self.answer[i] + "\n")

    def display(self):
        print()
        print("   1   2   3   4   5   6   7   8   9")
        print(" |===.===.===|===.===.===|===.===.===|")

        for r in range(1, GRID_SIZE + 1):
            print(f"{r}|", end='')

            for c in range(1, GRID_SIZE + 1):
                if c % 3 == 0:
                    print(f"{SPACE}{self.grid[r][c].get_value()}{SPACE}|", end='')
                else:
                    print(f"{SPACE}{self.grid[r][c].get_value()}{SPACE}.", end='')

            print()

            if r % 3 == 0:
                print(" |===.===.===|===.===.===|===.===.===|")
            else:
                print(" |...........|...........|...........|")

        print()

    def solve(self):
        self.display()

        if self.grid[0][0].get_value() != 'X':
            print("No puzzle loaded")
            return

        print("Enter row column digit:")
        print("(Press Enter to stop)")

        move = input()

        while move != EMPTY_STRING:
            if len(move) != 3:
                print("Invalid input")
            else:
                try:
                    row = int(move[0])
                    column = int(move[1])
                    digit = move[2]

                    if digit < '1' or digit > '9':
                        print("Invalid input")
                    else:
                        self.grid[row][column].update(digit)
                        self.answer[2] = str(int(self.answer[2]) + 1)
                        self.answer[int(self.answer[2]) + 2] = move

                        self.display()

                except:
                    print("Invalid input")

            print("Enter row column digit:")
            print("(Press Enter to stop)")
            move = input()

    def check_solution(self):
        errors = 0
        incomplete = False
        solved = False

        for row in range(1, GRID_SIZE + 1):
            for column in range(1, GRID_SIZE + 1):
                entry = self.grid[row][column].get_value()

                if entry == SPACE:
                    incomplete = True

                if not (entry == self.solution[row][column] or entry == SPACE):
                    print(f"Error in row {row} column {column}")
                    errors += 1

        if errors > 0:
            print(f"You have made {errors} error(s)")
        elif incomplete:
            print("So far so good, carry on")
        else:
            solved = True

        return errors, solved

    def calculate_score(self, errors):
        self.answer[1] = str(int(self.answer[1]) - errors)

    def display_results(self):
        if int(self.answer[2]) > 0:
            print(f"Your score is {self.answer[1]}")
            print(f"Your solution for {self.name} was:")

            for i in range(3, int(self.answer[2]) + 3):
                print(self.answer[i])
        else:
            print("You didn't make a start")

class Game:
    def __init__(self):
        self.puzzle = Puzzle()
        self.finished = False

    def menu(self):
        print("\nMain Menu")
        print("=========")
        print("L - Load new puzzle")
        print("P - Load partially solved puzzle")
        print("S - Solve puzzle")
        print("C - Check solution")
        print("K - Keep partially solved puzzle")
        print("X - Exit\n")

    def get_choice(self):
        choice = ""
        while len(choice) != 1:
            choice = input("Enter your choice: ")
        return choice.upper()

    def run(self):
        while not self.finished:
            self.menu()
            choice = self.get_choice()

            if choice == 'L':
                self.puzzle.load()

            elif choice == 'P':
                self.puzzle.load_partial()

            elif choice == 'S':
                self.puzzle.solve()

            elif choice == 'C':
                if self.puzzle.grid[0][0].get_value() != 'X':
                    print("No puzzle loaded")
                elif int(self.puzzle.answer[2]) > 0:
                    errors, solved = self.puzzle.check_solution()
                    self.puzzle.calculate_score(errors)

                    if solved:
                        print("You have successfully solved the puzzle")
                        self.finished = True
                    else:
                        print(f"Your score so far is {self.puzzle.answer[1]}")
                else:
                    print("No answers to check")

            elif choice == 'K':
                self.puzzle.save_partial()

            elif choice == 'X':
                self.finished = True

            else:
                print(random.choice([
                    "Invalid menu option. Try again",
                    "You did not choose a valid menu option. Try again",
                    "Your menu option is not valid. Try again",
                    "Only L, P, S, C, K or X are valid menu options. Try again",
                    "Try one of L, P, S, C, K or X"
                ]))

        if self.puzzle.answer[2] != EMPTY_STRING:
            self.puzzle.display_results()


if __name__ == "__main__":
    new_game = Game()
    new_game.run()