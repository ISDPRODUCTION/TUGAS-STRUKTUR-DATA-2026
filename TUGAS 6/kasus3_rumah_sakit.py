import pygame
import sys
import time
import random

class BPriorityQueue:
    def __init__(self, levels):
        self.levels = levels
        self.queue = [[] for _ in range(levels)]
    def isEmpty(self):
        for level in self.queue:
            if level: return False
        return True
    def enqueue(self, item, priority):
        if 0 <= priority < self.levels:
            self.queue[priority].append(item)
    def dequeue(self):
        for i in range(self.levels):
            if self.queue[i]:
                return self.queue[i].pop(0), i
        return None, None

# Pygame Setup
pygame.init()
WIDTH, HEIGHT = 900, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kasus 3: Antrian Rumah Sakit (Priority)")
font = pygame.font.SysFont("Arial", 18)
header_font = pygame.font.SysFont("Arial", 28, bold=True)

# Colors
BG_COLOR = (240, 240, 240)
BLACK = (30, 30, 30)
WHITE = (255, 255, 255)
ZONE_COLORS = [
    (231, 76, 60),  # Red: Kritis
    (241, 196, 15), # Yellow: Darurat
    (52, 152, 219), # Blue: Menengah
    (46, 204, 113)  # Green: Ringan
]
ZONE_NAMES = ["KRITIS (0)", "DARURAT (1)", "MENENGAH (2)", "RINGAN (3)"]

def main():
    pq = BPriorityQueue(4)
    patients = [
        ("Budi", 3), ("Ani", 0), ("Citra", 2), ("Dedi", 0), ("Eka", 1)
    ]
    
    patient_idx = 0
    current_patient = None
    last_action_time = time.time()
    last_arrival_time = time.time()
    state = "SERVING" # Go straight to serving since arrival is random

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BG_COLOR)
        now = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if not running: break

        # Logic: Random new arrival while NOT finished
        if state != "FINISHED" and now - last_arrival_time > 4: # every 4 seconds
            if random.random() < 0.6: # 60% chance
                new_name = random.choice(["Gani", "Hana", "Indra", "Juna", "Kira", "Lutfi"])
                new_prio = random.randint(0, 3)
                pq.enqueue(new_name, new_prio)
            last_arrival_time = now

        # Header
        title = header_font.render("KASUS 3: ANTRIAN RS (DYNAMIC)", True, BLACK)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))

        # Drawer Triage Zones
        zone_w = 180
        start_x = 50
        for i in range(4):
            x = start_x + i * (zone_w + 20)
            pygame.draw.rect(screen, ZONE_COLORS[i], (x, 100, zone_w, 350), 2, border_radius=5)
            label = font.render(ZONE_NAMES[i], True, ZONE_COLORS[i])
            screen.blit(label, (x + zone_w//2 - label.get_width()//2, 75))
            
            for j, p_name in enumerate(pq.queue[i]):
                py = 110 + j * 40
                pygame.draw.rect(screen, ZONE_COLORS[i], (x + 5, py, zone_w - 10, 35), border_radius=3)
                p_text = font.render(p_name, True, WHITE)
                screen.blit(p_text, (x + zone_w//2 - p_text.get_width()//2, py + 8))

        # Doctor Area
        pygame.draw.rect(screen, BLACK, (800, 100, 80, 350), 1)
        doc_label = font.render("DOKTER", True, BLACK)
        screen.blit(doc_label, (800 + 40 - doc_label.get_width()//2, 75))
        
        if current_patient:
            name, p_lvl = current_patient
            pygame.draw.rect(screen, ZONE_COLORS[p_lvl], (805, 200, 70, 50), border_radius=5)
            p_text = font.render(name, True, WHITE)
            screen.blit(p_text, (805 + 35 - p_text.get_width()//2, 215))

        # Logic
        if state == "SERVING":
            if now - last_action_time > 3.0:
                if not pq.isEmpty():
                    current_patient = pq.dequeue()
                    patient_idx += 1
                else:
                    current_patient = None
                    if patient_idx >= 5: # Finished after at least 5 patients
                        state = "FINISHED"
                last_action_time = now

        if state == "FINISHED":
            status_txt = "SIMULASI SELESAI"
            exit_hint = font.render("(Tutup jendela untuk keluar)", True, (100, 100, 100))
            screen.blit(exit_hint, (WIDTH//2 - exit_hint.get_width()//2, HEIGHT - 15))
        else:
            status_txt = "Rawat Inap & Pasien Baru..." 
        
        status_render = font.render(status_txt, True, BLACK)
        screen.blit(status_render, (WIDTH//2 - status_render.get_width()//2, HEIGHT - 35))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
