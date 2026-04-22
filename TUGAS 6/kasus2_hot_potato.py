import pygame
import sys
import math
import time
import random

class Queue:
    def __init__(self):
        self.items = []
    def isEmpty(self):
        return self.items == []
    def enqueue(self, item):
        self.items.insert(0, item)
    def dequeue(self):
        if not self.isEmpty():
            return self.items.pop()
    def size(self):
        return len(self.items)

# Pygame Setup
pygame.init()
WIDTH, HEIGHT = 700, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kasus 2: Permainan Hot Potato")
font = pygame.font.SysFont("Arial", 24)
title_font = pygame.font.SysFont("Arial", 32, bold=True)

# Colors
BG_COLOR = (30, 30, 30)
WHITE = (255, 255, 255)
PLAYER_COLOR = (100, 149, 237)
POTATO_COLOR = (255, 69, 0)
ELIMINATED_COLOR = (80, 80, 80)
WINNER_COLOR = (50, 205, 50)

def main():
    names = ["Budi", "Ani", "Citra", "Dedi", "Eka"]
    q = Queue()
    all_players = names[:]
    for name in names:
        q.enqueue(name)

    num_passes = random.randint(2, 6)
    current_pass = 0
    potato_holder = names[0]
    eliminated_name = None
    winner = None

    clock = pygame.time.Clock()
    running = True
    
    # Circle layout
    center_x, center_y = WIDTH//2, HEIGHT//2
    radius = 200

    last_step_time = time.time()
    step_delay = 1.0 # seconds

    while running:
        screen.fill(BG_COLOR)
        now = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if not running: break

        # Title
        title_text = title_font.render("KASUS 2: PERMAINAN HOT POTATO", True, WHITE)
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 40))

        # Logic
        if winner is None and now - last_step_time > step_delay:
            if current_pass < num_passes:
                potato_holder = q.dequeue()
                q.enqueue(potato_holder)
                current_pass += 1
                eliminated_name = None
            else:
                eliminated_name = q.dequeue()
                current_pass = 0
                if q.size() == 1:
                    winner = q.dequeue()
                    potato_holder = None # potato vanishes at end
                last_step_time += 1.0 
            last_step_time = now

        # Draw players
        for i, name in enumerate(all_players):
            angle = (i / len(all_players)) * 2 * math.pi - math.pi/2
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            state_color = PLAYER_COLOR
            current_q_items = q.items + ([winner] if winner else [])
            if name not in current_q_items and name != potato_holder:
                state_color = ELIMINATED_COLOR
            
            if name == winner:
                state_color = WINNER_COLOR
                pygame.draw.circle(screen, state_color, (int(x), int(y)), 40)
                label = font.render("PEMENANG!", True, WINNER_COLOR)
                screen.blit(label, (int(x) - label.get_width()//2, int(y) - 65))
            else:
                pygame.draw.circle(screen, state_color, (int(x), int(y)), 35)

            if name == potato_holder and winner is None:
                pygame.draw.circle(screen, POTATO_COLOR, (int(x), int(y)), 35, 5)
                label = font.render("🔥 POTATO", True, POTATO_COLOR)
                screen.blit(label, (int(x) - label.get_width()//2, int(y) - 60))

            name_text = font.render(name, True, WHITE)
            screen.blit(name_text, (int(x) - name_text.get_width()//2, int(y) + 40))

        # Status text
        if eliminated_name:
            status = font.render(f"!!! {eliminated_name} Tersingkir !!!", True, POTATO_COLOR)
        elif winner:
            status = font.render(f"HASIL AKHIR: {winner} Menang!", True, WINNER_COLOR)
            exit_hint = font.render("(Tutup jendela untuk keluar)", True, (150, 150, 150))
            screen.blit(exit_hint, (WIDTH//2 - exit_hint.get_width()//2, HEIGHT - 40))
        else:
            status = font.render(f"Operasi: {current_pass}/{num_passes}", True, WHITE)
        
        screen.blit(status, (WIDTH//2 - status.get_width()//2, HEIGHT - 80))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
