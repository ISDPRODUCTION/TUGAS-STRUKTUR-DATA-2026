import pygame
import sys
import random
import time

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

class Agent:
    def __init__(self, id):
        self.id = id
        self.current_task_start = 0
        self.service_duration = 0
        self.busy = False
    
    def start_service(self, duration, current_time):
        self.busy = True
        self.current_task_start = current_time
        self.service_duration = duration
    
    def update(self, current_time):
        if self.busy:
            if current_time - self.current_task_start >= self.service_duration:
                self.busy = False
                return True # Finished service
        return False

# Pygame Setup
pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kasus 5: Simulasi Loket Bandara")
font = pygame.font.SysFont("Arial", 20)
stat_font = pygame.font.SysFont("Arial", 24, bold=True)

# Colors
BG_COLOR = (45, 52, 54)
COUNTER_COLOR = (99, 110, 114)
BUSY_COLOR = (231, 76, 60)
FREE_COLOR = (46, 204, 113)
PASSENGER_COLOR = (255, 255, 255)
WHITE = (255, 255, 255)
UI_PANEL = (30, 30, 30)

def main():
    # Simulation Params
    num_agents = 3 # You can change this to 2 to see the wait time increase
    arrival_rate = 15 # 1 passenger every ~15 frames (~0.25s)
    service_range = (60, 180) # 1-3 seconds in frames
    
    passenger_queue = Queue()
    agents = [Agent(i) for i in range(num_agents)]
    
    total_served = 0
    total_wait_time = 0
    frame_count = 0
    
    clock = pygame.time.Clock()
    running = True

    max_frames = 60 * 30 # 30 seconds of simulation
    sim_finished = False

    while running:
        screen.fill(BG_COLOR)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if not running: break

        if not sim_finished:
            frame_count += 1
            if frame_count >= max_frames:
                sim_finished = True

            # Logic: Random Arrival
            if random.randrange(1, arrival_rate + 1) == arrival_rate:
                passenger_queue.enqueue(frame_count)

            # Logic: Update Agents and Serve
            for agent in agents:
                if agent.update(frame_count):
                    total_served += 1
                
                if not agent.busy and not passenger_queue.isEmpty():
                    arrival_time = passenger_queue.dequeue()
                    wait = frame_count - arrival_time
                    total_wait_time += wait
                    agent.start_service(random.randint(*service_range), frame_count)

        # Draw UI Panel
        pygame.draw.rect(screen, UI_PANEL, (0, 0, WIDTH, 100))
        title_txt = f"SIMULASI LOKET BANDARA {'(SELESAI)' if sim_finished else ''}"
        title = stat_font.render(title_txt, True, WHITE)
        screen.blit(title, (20, 35))
        
        avg_wait = (total_wait_time / total_served / 60) if total_served > 0 else 0
        stats = [
            f"Waktu Simulasi: {frame_count // 60}s",
            f"Total Terlayani: {total_served}",
            f"Antrian Saat Ini: {passenger_queue.size()}",
            f"Rata-rata Tunggu: {avg_wait:.2f} unit"
        ]
        
        for i, text in enumerate(stats):
            render = font.render(text, True, WHITE)
            screen.blit(render, (400 + (i//2)*250, 20 + (i%2)*40))

        if sim_finished:
            hint = font.render("SIMULASI SELESAI - Tutup jendela untuk keluar", True, (150, 150, 150))
            screen.blit(hint, (20, 75))

        # Draw Counters/Agents
        start_x = WIDTH // 2 - (num_agents * 120) // 2
        for i, agent in enumerate(agents):
            x = start_x + i * 150
            y = 200
            color = BUSY_COLOR if agent.busy else FREE_COLOR
            pygame.draw.rect(screen, COUNTER_COLOR, (x, y, 100, 100), border_radius=10)
            pygame.draw.circle(screen, color, (x + 50, y + 50), 30)
            label = font.render(f"Loket {i+1}", True, WHITE)
            screen.blit(label, (x + 50 - label.get_width()//2, y + 110))
            if agent.busy:
                rem = (agent.service_duration - (frame_count - agent.current_task_start)) // 6
                rem_text = font.render(f"{rem}", True, WHITE)
                screen.blit(rem_text, (x + 50 - rem_text.get_width()//2, y + 40))

        # Draw Queue
        for i in range(min(passenger_queue.size(), 100)):
            row = i // 15
            col = i % 15
            px = 100 + col * 40
            py = 400 + row * 40
            pygame.draw.circle(screen, PASSENGER_COLOR, (px, py), 12)
            if i == 0:
                pygame.draw.circle(screen, (241, 196, 15), (px, py), 14, 2)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
