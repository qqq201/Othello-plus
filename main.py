from StateMachine import *

if __name__ == "__main__":
    state_machine = StateMachine({
        "StartState": StartState(),
        "PlayState": PlayState()
    })

    state_machine.change("StartState")

    run = True

    while run:
        click = False

        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONUP:
                click = True

        state_machine.update(mouse, click)
        pygame.display.flip()

    pygame.quit()
