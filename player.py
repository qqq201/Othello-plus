from dependencies import *

class Player:
    def __init__(self):
        self.color = 1

    def set_player(self, color):
        self.color = color

    def clear(self):
        self.color = 1

    def play(self, board, mouse, click):
        for i in range(ROWS):
            for j in range(COLS):
                if board.is_placeable((i, j), self.color):
                    x, y = OFFSET + j * (CELL_SIZE + 5), OFFSET + i * (CELL_SIZE + 5)
                    if click:
                        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                        if rect.collidepoint(mouse) and board.get_turn() == self.color:
                            return board.make_action((i, j))
                    else:
                        pygame.draw.circle(screen, GRAY, (x + CELL_SIZE / 2, y + CELL_SIZE / 2), 5)

        pygame.display.update()
        return None
