from states.BaseState import *

class StartState(BaseState):
    def __init__(self):
        button_width = 170
        button_height = 40
        offset = 100
        self.player1_button = pygame.Rect(WIDTH / 2 - button_width / 2, offset, button_width, button_height)
        self.player1_text = fonts["small"].render("Player 1", True, BLACK)
        self.player1_text_rect = self.player1_text.get_rect(center = self.player1_button.center)

        self.player2_button = pygame.Rect(WIDTH / 2 - button_width / 2, offset + button_height + 20, button_width, button_height)
        self.player2_text = fonts["small"].render("Player 2", True, BLACK)
        self.player2_text_rect = self.player2_text.get_rect(center = self.player2_button.center)


    def update(self, state_machine, mouse, click):
        pygame.draw.rect(screen, WHITE, self.player1_button, border_radius = 7)
        screen.blit(self.player1_text, self.player1_text_rect)

        pygame.draw.rect(screen, WHITE, self.player2_button, border_radius = 7)
        screen.blit(self.player2_text, self.player2_text_rect)

        if click and self.player1_button.collidepoint(mouse):
            state_machine.change("PlayState", 1)
        elif click and self.player2_button.collidepoint(mouse):
            state_machine.change("PlayState", 2)
