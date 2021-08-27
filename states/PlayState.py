from states.BaseState import *
import asyncio
from ai import AI
from player import Player
from othello import Board

class PlayState(BaseState):
    def __init__(self):
        self.ai = AI()
        self.player = Player()
        self.board = Board()
        self.player_color = 1
        self.winner = None
        self.in_progress = False


    def enter(self, color):
        self.player.set_player(color)
        self.player_color = color
        self.ai.set_player(1 if color == 2 else 2)
        self.in_progress = False


    def exit(self):
        self.ai.clear()
        self.player.clear()
        self.board.clear()
        self.player_color = 1
        self.winner = None


    async def play(self, mouse, click):
        if not self.in_progress:
            in_turn = self.board.get_turn()

            if in_turn == self.player_color:
                self.winner = self.player.play(self.board, mouse, click)
            else:
                self.in_progress = True
                task = asyncio.create_task(self.ai.play(self.board))

                load_text = fonts["large"].render("AI's turn", True, WHITE)
                load_rect = load_text.get_rect(center=(250 + ((720 - 100) / 2), 100))
                screen.blit(load_text, load_rect)
                pygame.display.update()

                await task
                self.winner = task.result()
                self.in_progress = False


    def update(self, state_machine, mouse, click):
        self.board.update()

        if self.winner is None:
            asyncio.run(self.play(mouse, click))
        else:
            winnerText = None

            if self.winner != 0:
                winnerText = fonts["large"].render(f"Player {self.winner} won!", True, WHITE)
            else:
                winnerText = fonts["large"].render("Draw!", True, WHITE)

            winnerRect = winnerText.get_rect(center=(250 + ((720 - 100) / 2), 100))
            screen.blit(winnerText, winnerRect)
