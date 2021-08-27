# Othello plus
## Gameplay rules
Regular [Othello](https://www.ultraboardgames.com/othello/game-rules.php)'rules with some variations:
- The game is over when one of the two players is not able to make a move (instead of both likes the original)
- Added 5 special cells called victory cells. The game would end immediately if one player occupied all victory cells.
- In the end game if both players have the same number of discs on the board, the player containing the more victory cells will win. Otherwise, it'll be a draw.

<image src="https://user-images.githubusercontent.com/61228506/131079051-cbeb5822-52cc-4584-ba19-cd97cdae4063.png" alt="preview" width="500"/>

Note: this program was built to serve for AI testing purpose only. Thus, some errors may occur.

## AI
The AI was implemented based on Adversarial search with additional algorithms that helps enhance the performance.

### Applied techniques
1. Negamax
2. Transposition table
3. Move ordering
4. Negascout (Principle variation search)
5. Quiescence search
6. Iterative deepening

### Evaluation Strategy
- Evaluate base on:
  - The score of each position reflects how valuable it is.
  - The number of occupied victory cells
  - Consider special situation happends with the next-to-corner cells

- Maintaining the mobility

- Evaporation Strategy (according to http://www.samsoft.org.uk/reversi/strategy.htm)

### Performance

Depth ply: 5 - 8 in the beginning, 10 in the end game

Response time: ~5s / turn
