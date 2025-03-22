import pygame
import sys
import random
import time
import os
from pygame import mixer

# Initialize pygame
pygame.init()
mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 128)
FONT_SIZE = 32
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
DICE_SIZE = 100
DICE_MARGIN = 20
ANIMATION_SPEED = 10
FPS = 60

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Dice Game")
clock = pygame.time.Clock()

# Load fonts
font = pygame.font.SysFont('Arial', FONT_SIZE)
small_font = pygame.font.SysFont('Arial', 24)
title_font = pygame.font.SysFont('Arial', 48)

# Create assets folder if it doesn't exist
if not os.path.exists('assets'):
    os.makedirs('assets')

# Dice images
dice_images = []

def load_or_create_dice_images():
    """Load dice images or create them if they don't exist"""
    global dice_images
    dice_images = []
    
    for i in range(1, 7):
        # Check if image exists
        path = f'assets/dice{i}.png'
        if os.path.exists(path):
            img = pygame.image.load(path)
            img = pygame.transform.scale(img, (DICE_SIZE, DICE_SIZE))
            dice_images.append(img)
        else:
            # Create the dice image
            surface = pygame.Surface((DICE_SIZE, DICE_SIZE), pygame.SRCALPHA)
            surface.fill((255, 255, 255, 0))
            pygame.draw.rect(surface, WHITE, (0, 0, DICE_SIZE, DICE_SIZE), border_radius=10)
            pygame.draw.rect(surface, BLACK, (0, 0, DICE_SIZE, DICE_SIZE), 2, border_radius=10)
            
            # Draw dots based on dice value
            dot_radius = DICE_SIZE // 10
            if i == 1:
                # Center dot
                pygame.draw.circle(surface, BLACK, (DICE_SIZE // 2, DICE_SIZE // 2), dot_radius)
            elif i == 2:
                # Top-left and bottom-right dots
                pygame.draw.circle(surface, BLACK, (DICE_SIZE // 4, DICE_SIZE // 4), dot_radius)
                pygame.draw.circle(surface, BLACK, (3 * DICE_SIZE // 4, 3 * DICE_SIZE // 4), dot_radius)
            elif i == 3:
                # Top-left, center, and bottom-right dots
                pygame.draw.circle(surface, BLACK, (DICE_SIZE // 4, DICE_SIZE // 4), dot_radius)
                pygame.draw.circle(surface, BLACK, (DICE_SIZE // 2, DICE_SIZE // 2), dot_radius)
                pygame.draw.circle(surface, BLACK, (3 * DICE_SIZE // 4, 3 * DICE_SIZE // 4), dot_radius)
            elif i == 4:
                # Four corner dots
                pygame.draw.circle(surface, BLACK, (DICE_SIZE // 4, DICE_SIZE // 4), dot_radius)
                pygame.draw.circle(surface, BLACK, (3 * DICE_SIZE // 4, DICE_SIZE // 4), dot_radius)
                pygame.draw.circle(surface, BLACK, (DICE_SIZE // 4, 3 * DICE_SIZE // 4), dot_radius)
                pygame.draw.circle(surface, BLACK, (3 * DICE_SIZE // 4, 3 * DICE_SIZE // 4), dot_radius)
            elif i == 5:
                # Four corner dots + center dot
                pygame.draw.circle(surface, BLACK, (DICE_SIZE // 4, DICE_SIZE // 4), dot_radius)
                pygame.draw.circle(surface, BLACK, (3 * DICE_SIZE // 4, DICE_SIZE // 4), dot_radius)
                pygame.draw.circle(surface, BLACK, (DICE_SIZE // 2, DICE_SIZE // 2), dot_radius)
                pygame.draw.circle(surface, BLACK, (DICE_SIZE // 4, 3 * DICE_SIZE // 4), dot_radius)
                pygame.draw.circle(surface, BLACK, (3 * DICE_SIZE // 4, 3 * DICE_SIZE // 4), dot_radius)
            elif i == 6:
                # Six dots (2 rows of 3)
                pygame.draw.circle(surface, BLACK, (DICE_SIZE // 4, DICE_SIZE // 4), dot_radius)
                pygame.draw.circle(surface, BLACK, (DICE_SIZE // 4, DICE_SIZE // 2), dot_radius)
                pygame.draw.circle(surface, BLACK, (DICE_SIZE // 4, 3 * DICE_SIZE // 4), dot_radius)
                pygame.draw.circle(surface, BLACK, (3 * DICE_SIZE // 4, DICE_SIZE // 4), dot_radius)
                pygame.draw.circle(surface, BLACK, (3 * DICE_SIZE // 4, DICE_SIZE // 2), dot_radius)
                pygame.draw.circle(surface, BLACK, (3 * DICE_SIZE // 4, 3 * DICE_SIZE // 4), dot_radius)
            
            # Save the image
            pygame.image.save(surface, path)
            dice_images.append(surface)

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
        
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        
    def is_clicked(self, pos, click):
        return self.rect.collidepoint(pos) and click

class Dice:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.value = 1
        self.target_value = 1
        self.animation_frames = 0
        self.is_rolling = False
        self.roll_speed = random.randint(5, 15)
        
    def roll(self):
        self.target_value = random.randint(1, 6)
        self.is_rolling = True
        self.animation_frames = self.roll_speed
        
    def update(self):
        if self.is_rolling:
            if self.animation_frames > 0:
                self.animation_frames -= 1
                # Show random values during animation
                self.value = random.randint(1, 6)
            else:
                self.value = self.target_value
                self.is_rolling = False
                
    def draw(self, surface):
        if 0 <= self.value - 1 < len(dice_images):
            surface.blit(dice_images[self.value - 1], (self.x, self.y))

class Game:
    def __init__(self):
        self.dice_count = 1
        self.dice = []
        self.is_rolling = False
        self.roll_count = 0
        self.total_rolls = 0
        self.start_time = time.time()
        self.game_time = 0
        self.best_time = float('inf')
        self.best_rolls = float('inf')
        self.load_best_scores()
        self.reset_dice()
        
        # Buttons
        button_y = SCREEN_HEIGHT - BUTTON_HEIGHT - 20
        self.roll_button = Button(
            SCREEN_WIDTH // 2 - BUTTON_WIDTH - 10, 
            button_y, 
            BUTTON_WIDTH, 
            BUTTON_HEIGHT, 
            "Roll Dice", 
            GREEN, 
            (150, 255, 150)
        )
        
        self.restart_button = Button(
            SCREEN_WIDTH // 2 + 10, 
            button_y, 
            BUTTON_WIDTH, 
            BUTTON_HEIGHT, 
            "Restart", 
            BLUE, 
            (150, 150, 255)
        )
        
    def load_best_scores(self):
        """Load best scores from a file"""
        if os.path.exists('best_scores.txt'):
            try:
                with open('best_scores.txt', 'r') as f:
                    lines = f.readlines()
                    if len(lines) >= 2:
                        self.best_time = float(lines[0].strip())
                        self.best_rolls = int(lines[1].strip())
            except Exception as e:
                print(f"Error loading best scores: {e}")
                
    def save_best_scores(self):
        """Save best scores to a file"""
        try:
            with open('best_scores.txt', 'w') as f:
                f.write(f"{self.best_time}\n")
                f.write(f"{self.best_rolls}\n")
        except Exception as e:
            print(f"Error saving best scores: {e}")
        
    def reset_dice(self):
        """Reset the dice arrangement"""
        self.dice = []
        
        if self.dice_count <= 5:
            # Arrange dice in a single row
            total_width = self.dice_count * DICE_SIZE + (self.dice_count - 1) * DICE_MARGIN
            start_x = (SCREEN_WIDTH - total_width) // 2
            
            for i in range(self.dice_count):
                x = start_x + i * (DICE_SIZE + DICE_MARGIN)
                y = SCREEN_HEIGHT // 2 - DICE_SIZE // 2 - 50
                self.dice.append(Dice(x, y))
        else:
            # Arrange dice in multiple rows
            dice_per_row = 5
            rows = (self.dice_count + dice_per_row - 1) // dice_per_row
            
            for row in range(rows):
                dice_in_this_row = min(dice_per_row, self.dice_count - row * dice_per_row)
                total_width = dice_in_this_row * DICE_SIZE + (dice_in_this_row - 1) * DICE_MARGIN
                start_x = (SCREEN_WIDTH - total_width) // 2
                
                for i in range(dice_in_this_row):
                    x = start_x + i * (DICE_SIZE + DICE_MARGIN)
                    y = SCREEN_HEIGHT // 2 - DICE_SIZE // 2 - 50 * rows + row * (DICE_SIZE + DICE_MARGIN)
                    self.dice.append(Dice(x, y))
    
    def roll_dice(self):
        """Roll all dice"""
        if not self.is_rolling:
            self.is_rolling = True
            self.roll_count += 1
            self.total_rolls += 1
            
            for die in self.dice:
                die.roll()
    
    def update(self):
        """Update game state"""
        # Update dice
        self.is_rolling = False
        for die in self.dice:
            die.update()
            if die.is_rolling:
                self.is_rolling = True
                
        # Check if all dice show 6
        if not self.is_rolling:
            all_sixes = all(die.value == 6 for die in self.dice)
            if all_sixes:
                # Level up!
                self.dice_count += 1
                self.reset_dice()
                self.roll_count = 0
            
        # Update game time
        self.game_time = time.time() - self.start_time
        
    def draw(self, surface):
        """Draw the game"""
        # Draw background
        surface.fill(GRAY)
        
        # Draw title
        title_text = title_font.render("The Dice Game", True, DARK_BLUE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 40))
        surface.blit(title_text, title_rect)
        
        # Draw dice
        for die in self.dice:
            die.draw(surface)
            
        # Draw buttons
        self.roll_button.draw(surface)
        self.restart_button.draw(surface)
        
        # Draw stats
        stats_y = 100
        level_text = small_font.render(f"Level: {self.dice_count}", True, BLACK)
        surface.blit(level_text, (20, stats_y))
        
        rolls_text = small_font.render(f"Rolls this level: {self.roll_count}", True, BLACK)
        surface.blit(rolls_text, (20, stats_y + 30))
        
        total_rolls_text = small_font.render(f"Total rolls: {self.total_rolls}", True, BLACK)
        surface.blit(total_rolls_text, (20, stats_y + 60))
        
        time_text = small_font.render(f"Time: {self.game_time:.1f}s", True, BLACK)
        surface.blit(time_text, (20, stats_y + 90))
        
        # Draw best scores
        if self.best_time < float('inf'):
            best_time_text = small_font.render(f"Best time: {self.best_time:.1f}s", True, BLACK)
            surface.blit(best_time_text, (SCREEN_WIDTH - 200, stats_y))
            
        if self.best_rolls < float('inf'):
            best_rolls_text = small_font.render(f"Best rolls: {self.best_rolls}", True, BLACK)
            surface.blit(best_rolls_text, (SCREEN_WIDTH - 200, stats_y + 30))
            
        # Draw instructions
        instruction_y = SCREEN_HEIGHT - 120
        current_goal = small_font.render(f"Current goal: Get {self.dice_count} sixes", True, BLACK)
        surface.blit(current_goal, (SCREEN_WIDTH // 2 - current_goal.get_width() // 2, instruction_y))
        
    def restart(self):
        """Restart the game"""
        # Check if this run beat any records
        if self.dice_count > 1 and self.game_time < self.best_time:
            self.best_time = self.game_time
            
        if self.dice_count > 1 and self.total_rolls < self.best_rolls:
            self.best_rolls = self.total_rolls
            
        # Save best scores
        self.save_best_scores()
        
        # Reset game state
        self.dice_count = 1
        self.roll_count = 0
        self.total_rolls = 0
        self.start_time = time.time()
        self.reset_dice()
        
    def handle_event(self, event):
        """Handle a pygame event"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check button clicks
            mouse_pos = pygame.mouse.get_pos()
            
            if self.roll_button.is_clicked(mouse_pos, True):
                self.roll_dice()
                
            if self.restart_button.is_clicked(mouse_pos, True):
                self.restart()
                
        elif event.type == pygame.MOUSEMOTION:
            # Check button hover
            mouse_pos = pygame.mouse.get_pos()
            self.roll_button.check_hover(mouse_pos)
            self.restart_button.check_hover(mouse_pos)

def main():
    """Main game function"""
    # Load assets
    load_or_create_dice_images()
    
    # Create game instance
    game = Game()
    
    # Main game loop
    running = True
    while running:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)
                
        # Update game state
        game.update()
        
        # Draw everything
        game.draw(screen)
        
        # Update the display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(FPS)
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
    