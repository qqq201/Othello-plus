from dependencies import *

'''
    0: empty
    1: black
    2: white
'''

class Board:
    def __init__(self):
        self.data = np.array([[0] * 8] * 8)
        self.data[int(ROWS / 2) - 1, int(COLS / 2)] = self.data[int(ROWS / 2), int(COLS / 2) - 1] = 1
        self.data[int(ROWS / 2) - 1, int(COLS / 2) - 1] = self.data[int(ROWS / 2), int(COLS / 2)] = 2
        random_numbers = np.random.choice(64, 5, replace = False)
        self.victory_cells = [(num // 8, num % 8) for num in random_numbers]
        self.turn = 1

        self.board_width = (CELL_SIZE + 5) * COLS + 16
        self.board_height = (CELL_SIZE + 5) * ROWS + 16


    def clear(self):
        self.data = np.array([[0] * 8] * 8)
        self.data[int(ROWS / 2) - 1, int(COLS / 2)] = self.data[int(ROWS / 2), int(COLS / 2) - 1] = 1
        self.data[int(ROWS / 2) - 1, int(COLS / 2) - 1] = self.data[int(ROWS / 2), int(COLS / 2)] = 2
        random_numbers = np.random.choice(64, 5, replace = False)
        self.victory_cells = [(num // 8, num % 8) for num in random_numbers]
        self.turn = 1


    def is_direction_placeable(self, position, direction, player):
        x, y = position
        dx, dy = direction

        for i in range(1, ROWS + 1):
            r = x + i * dx
            c = y + i * dy
            if r < 0 or r > 7 or c < 0 or c > 7 or self.data[r, c] == 0:
                return False

            if self.data[r, c] == player:
                return not i == 1


    def is_placeable(self, position, player):
        if self.data[position] != 0:
            return False

        return self.is_direction_placeable(position, (1, 0), player) or \
               self.is_direction_placeable(position, (1, 1), player) or \
               self.is_direction_placeable(position, (0, 1), player) or \
               self.is_direction_placeable(position, (-1, 1), player) or \
               self.is_direction_placeable(position, (-1, 0), player) or \
               self.is_direction_placeable(position, (-1, -1), player) or \
               self.is_direction_placeable(position, (0, -1), player) or \
               self.is_direction_placeable(position, (1, -1), player)


    def is_playable(self, player):
        for r in range(ROWS):
            for c in range(COLS):
                if self.is_placeable((r, c), player):
                    return True
        return False


    def available_actions(self, player):
        actions = list()

        for r in range(ROWS):
            for c in range(COLS):
                if self.is_placeable((r, c), player):
                    actions.append((r, c))
        return actions


    def stat(self):
        count = [0] * 3
        for r in range(ROWS):
            for c in range(COLS):
                count[self.data[r, c]] += 1

        return count[1], count[2]


    def flipped_discs_on_direction(self, position, direction, player):
        flip_discs = []
        x, y = position
        dx, dy = direction

        for i in range(1, 9):
            r = x + i * dx
            c = y + i * dy

            if r < 0 or r > 7 or c < 0 or c > 7 or self.data[r, c] == 0:
                return []

            if self.data[r, c] == player:
                return flip_discs
            flip_discs.append((r, c))

        return flip_discs


    def flipped_discs(self, position, player):
        x, y = position
        flip_discs = [(x, y)]
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                flip_discs = flip_discs + self.flipped_discs_on_direction(position, (dx, dy), player)

        return flip_discs


    def place(self, position, player):
        flip_discs = self.flipped_discs(position, player)
        for position in flip_discs:
            self.data[position] = player


    def get_value(self, position):
        return self.data[position]


    def get_victory_cells(self):
        return self.victory_cells


    def get_data(self):
        return self.data


    def get_turn(self):
        return self.turn


    def update(self):
        board = pygame.Rect(OFFSET - 10, OFFSET - 10, self.board_width, self.board_height)
        pygame.draw.rect(screen, GREEN, board, border_radius=7)

        for i in range(ROWS):
            for j in range(COLS):
                x, y = OFFSET + j * (CELL_SIZE + 5), OFFSET + i * (CELL_SIZE + 5)
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                if (i, j) in self.victory_cells:
                    pygame.draw.rect(screen, YELLOW, rect, border_radius=3)
                else:
                    pygame.draw.rect(screen, DARK_GREEN, rect, border_radius=3)

                if self.data[i, j] == 1:
                    pygame.draw.circle(screen, DARK_GRAY, (x + CELL_SIZE / 2 + 2, y + CELL_SIZE / 2 + 2), CELL_SIZE / 2 - 4)
                    pygame.draw.circle(screen, GRAY, (x + CELL_SIZE / 2, y + CELL_SIZE / 2), CELL_SIZE / 2 - 4)
                elif self.data[i, j] == 2:
                    pygame.draw.circle(screen, SHADOW, (x + CELL_SIZE / 2 + 2, y + CELL_SIZE / 2 + 2), CELL_SIZE / 2 - 4)
                    pygame.draw.circle(screen, WHITE, (x + CELL_SIZE / 2, y + CELL_SIZE / 2), CELL_SIZE / 2 - 4)


    def make_action(self, position):
        self.place(position, self.turn)
        self.update()

        self.turn = 1 if self.turn == 2 else 2
        return self.check_gameover()


    def check_gameover(self):
        victory_score = [0] * 3
        for cell in self.victory_cells:
            victory_score[self.data[cell]] += 1

        if victory_score[1] == 5:
            return 1

        if victory_score[2] == 5:
            return 2

        if not self.is_playable(self.turn):
            b, w = self.stat()
            if b > w:
                return 1
            elif b < w:
                return 2
            elif victory_score[1] > victory_score[2]:
                return 1
            elif victory_score[1] < victory_score[2]:
                return 2
            else:
                return 0

        return None
