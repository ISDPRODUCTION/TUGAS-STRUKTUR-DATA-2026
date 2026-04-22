import pygame
import sys
import math
import time
import random

# Standard Queue implementation
class Queue:
    def __init__(self):
        self.items = []
    def isEmpty(self):
        return self.items == []
    def enqueue(self, item):
        self.items.insert(0, item)
    def dequeue(self):
        return self.items.pop()
    def size(self):
        return len(self.items)

# Pygame Setup
pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kasus 1: Antrian Printer Bersama")
font = pygame.font.SysFont("Arial", 20)
large_font = pygame.font.SysFont("Arial", 30, bold=True)

# Colors
WHITE = (245, 245, 245)
BLUE = (52, 152, 219)
DARK_BLUE = (41, 128, 185)
GREEN = (46, 204, 113)
GRAY = (149, 165, 166)
BLACK = (44, 62, 80)

def draw_text(text, font, color, x, y, center=False):
    img = font.render(text, True, color)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(img, rect)

def main():
    printer_queue = Queue()
    docs = ["laporan.pdf", "tugas.docx", "foto.jpg"]
    for doc in docs:
        printer_queue.enqueue(doc)

    current_doc = None
    printing_progress = 0
    finished_docs = []
    
    clock = pygame.time.Clock()
    running = True
    
    # Position constants
    QUEUE_X = 100
    PRINTER_X = 600
    CENTER_Y = 200

    finished = False
    last_arrival_time = time.time()
    
    while running:
        screen.fill(WHITE)
        now = time.time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not running: break

        # Logic: Random new arrival
        if not finished and now - last_arrival_time > 3: # Check every 3 seconds
            if random.random() < 0.4 and printer_queue.size() < 5: # 40% chance
                ext = random.choice([".pdf", ".docx", ".jpg", ".png"])
                new_doc = f"Doc_{random.randint(100, 999)}{ext}"
                printer_queue.enqueue(new_doc)
                last_arrival_time = now

        # Draw Header
        draw_text("KASUS 1: ANTRIAN PRINTER (DYNAMIC)", large_font, BLACK, WIDTH//2, 40, center=True)
        
        # Draw Printer
        pygame.draw.rect(screen, GRAY, (PRINTER_X - 50, CENTER_Y - 60, 100, 120), border_radius=10)
        draw_text("PRINTER", font, WHITE, PRINTER_X, CENTER_Y, center=True)
        
        # Drawer/Finished Area
        draw_text("Selesai:", font, BLACK, 650, 300)
        for i, f_doc in enumerate(finished_docs[-3:]): 
             draw_text(f_doc, font, GREEN, 650, 330 + i*25)

        # Logic
        if not finished:
            if current_doc is None and not printer_queue.isEmpty():
                current_doc = printer_queue.dequeue()
                printing_progress = 0
                # delay between docs
            
            if current_doc:
                printing_progress += 1.5 # Slightly faster
                bar_w = 120
                pygame.draw.rect(screen, BLACK, (PRINTER_X - bar_w//2, CENTER_Y + 70, bar_w, 15), 1)
                pygame.draw.rect(screen, GREEN, (PRINTER_X - bar_w//2, CENTER_Y + 70, (min(printing_progress, 100)/100) * bar_w, 15))
                draw_text(f"Mencetak: {current_doc}", font, DARK_BLUE, PRINTER_X, CENTER_Y - 80, center=True)
                
                if printing_progress >= 100:
                    finished_docs.append(current_doc)
                    current_doc = None
            
            # Auto-finish if no docs for a while and queue empty
            if printer_queue.isEmpty() and current_doc is None and len(finished_docs) >= 5:
                finished = True
        else:
            draw_text("SEMUA DOKUMEN SELESAI DICETAK", font, GREEN, WIDTH//2, HEIGHT - 50, center=True)
            draw_text("(Tutup jendela untuk keluar)", font, GRAY, WIDTH//2, HEIGHT - 25, center=True)

        # Draw current queue items
        if not finished:
            items = printer_queue.items[::-1]
            for i, item in enumerate(items):
                box_x = QUEUE_X + i * 110
                pygame.draw.rect(screen, BLUE, (box_x, CENTER_Y - 25, 100, 50), border_radius=5)
                draw_text(item, font, WHITE, box_x + 50, CENTER_Y, center=True)
                if i == 0:
                    draw_text("Next", font, DARK_BLUE, box_x + 50, CENTER_Y - 40, center=True)

        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
