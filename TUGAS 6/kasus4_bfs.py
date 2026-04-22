import pygame
import sys
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

# Pygame Setup
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kasus 4: Visual BFS (Breadth-First Search)")
font = pygame.font.SysFont("Arial", 22)
title_font = pygame.font.SysFont("Arial", 28, bold=True)

# Colors
BG_COLOR = (20, 26, 35)
NODE_COLOR = (70, 70, 70)
VISITED_COLOR = (46, 204, 113)
CURRENT_COLOR = (52, 152, 219)
QUEUE_COLOR = (241, 196, 15)
WHITE = (255, 255, 255)
EDGE_COLOR = (100, 100, 100)

def main():
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }
    
    # Static positions for nodes
    node_pos = {
        'A': (WIDTH//2, 100),
        'B': (WIDTH//2 - 150, 250),
        'C': (WIDTH//2 + 150, 250),
        'D': (WIDTH//2 - 250, 400),
        'E': (WIDTH//2 - 50, 400),
        'F': (WIDTH//2 + 150, 400)
    }

    visited = set()
    queue = Queue()
    
    # State control
    queue.enqueue('A')
    visited.add('A')
    current_node = None
    
    step_time = time.time()
    step_delay = 2.0
    
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BG_COLOR)
        now = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if not running: break

        # Title
        title = title_font.render("KASUS 4: BFS (LEVEL-BY-LEVEL)", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 25))

        # Drawer edges
        for node, neighbors in graph.items():
            for neighbor in neighbors:
                pygame.draw.line(screen, EDGE_COLOR, node_pos[node], node_pos[neighbor], 2)

        # Draw nodes
        for node, pos in node_pos.items():
            color = NODE_COLOR
            if node == current_node:
                color = CURRENT_COLOR
            elif node in visited:
                color = VISITED_COLOR
            
            if node in queue.items:
                pygame.draw.circle(screen, QUEUE_COLOR, pos, 35, 5) 
            
            pygame.draw.circle(screen, color, pos, 30)
            text = font.render(node, True, WHITE)
            screen.blit(text, (pos[0] - text.get_width()//2, pos[1] - text.get_height()//2))

        # Status
        status_y = HEIGHT - 80
        pygame.draw.rect(screen, (40, 40, 40), (50, status_y, WIDTH - 100, 50), border_radius=10)
        
        if queue.isEmpty() and current_node is None:
            q_text = font.render("TRAVERSAL SELESAI!", True, VISITED_COLOR)
            hint = font.render("(Tutup jendela untuk keluar)", True, (100, 100, 100))
            screen.blit(hint, (WIDTH - 100 - hint.get_width(), status_y + 15))
        else:
            q_text = font.render(f"Queue Status: {queue.items[::-1]}", True, QUEUE_COLOR)
        
        screen.blit(q_text, (70, status_y + 15))

        # BFS Logic step
        if now - step_time > step_delay:
            if not queue.isEmpty():
                current_node = queue.dequeue()
                for neighbor in graph[current_node]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.enqueue(neighbor)
                step_time = now
            else:
                current_node = None

        legend_y = 100
        pygame.draw.circle(screen, CURRENT_COLOR, (700, legend_y), 10)
        screen.blit(font.render("Processing", True, WHITE), (720, legend_y - 12))
        pygame.draw.circle(screen, VISITED_COLOR, (700, legend_y + 30), 10)
        screen.blit(font.render("Visited", True, WHITE), (720, legend_y + 18))
        pygame.draw.circle(screen, QUEUE_COLOR, (700, legend_y + 60), 10, 3)
        screen.blit(font.render("In Queue", True, WHITE), (720, legend_y + 48))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
