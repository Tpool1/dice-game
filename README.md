# Dice Escalation Challenge

A fun dice rolling game built with Pygame where you progress through increasingly difficult levels by rolling sixes!

## Game Rules

1. You start with one die and need to roll a six to advance to the next level.
2. Once you roll a six, you move to level 2 where you need to roll two sixes simultaneously (on two dice).
3. At level 3, you need to roll three sixes simultaneously.
4. The pattern continues as you progress through the levels.

## Installation

1. Make sure you have Python 3.x installed on your system.
2. Install Pygame:
   ```
   pip install pygame
   ```

## Running the Game

1. Open a terminal or command prompt.
2. Navigate to the game directory.
3. Run the game:
   ```
   python main.py
   ```

## Controls

- **Left Mouse Button**: 
  - Click "Roll Dice" to roll the dice
  - Click "Restart" to start a new game

## Game Strategy

- The game is entirely based on chance, but it becomes exponentially harder as you progress through the levels.
- At level 1, the probability of rolling a six is 1/6 (about 16.7%).
- At level 2, the probability of rolling two sixes simultaneously is (1/6)² = 1/36 (about 2.8%).
- At level 3, the probability drops to (1/6)³ = 1/216 (about 0.46%).
- At level 4, it's (1/6)⁴ = 1/1296 (about 0.077%).

## Customization

You can modify several aspects of the game by editing the constants at the top of `main.py`:
- `SCREEN_WIDTH` and `SCREEN_HEIGHT`: Change the window size
- `DICE_SIZE`: Change the size of the dice
- `ANIMATION_SPEED`: Adjust the speed of the dice rolling animation
- Color constants: Modify the game's appearance

## Requirements

- Python 3.x
- Pygame 2.x

## License

This game is provided as open source software. Feel free to modify and distribute it according to your needs.
