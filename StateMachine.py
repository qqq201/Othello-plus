from states.BaseState import *
from states.StartState import StartState
from states.PlayState import PlayState

class StateMachine:
    def __init__(self, states):
        self.states = states
        self.current = None
        self.returnButton = pygame.Rect(0, 10, 80, 30)
        self.returnText = fonts["small"].render(u"\u25c4 BACK", True, GRAY)
        self.returnTextRect = self.returnText.get_rect(center = self.returnButton.center)


    def current_state(self):
        return str(self.current)


    def change(self, state, args=None):
        self.current = self.states[state]

        if self.current_state() == "PlayState":
            self.current.enter(args)


    def update(self, mouse, click):
        screen.fill(DARK_GRAY)

        # return button
        if self.current_state() != "StartState":
            if self.returnButton.collidepoint(mouse):
                if click:
                    self.current.exit()
                    self.change("StartState")
                else:
                    pygame.draw.rect(screen, WHITE, self.returnButton, border_top_right_radius = 7, border_bottom_right_radius = 7)
                    screen.blit(self.returnText, self.returnTextRect)
            else:
                pygame.draw.rect(screen, DARK_GRAY, self.returnButton)
                screen.blit(self.returnText, self.returnTextRect)

        self.current.update(self, mouse, click)
