import pygame
import networkx as nx
import random

# Initialize Pygame
pygame.init()

# Create a Pygame window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Graph with Pygame")

# Create the graph (same as before)
G = nx.Graph()

# Number of nodes
num_nodes = random.randint(6, 7)
G.add_nodes_from(range(1, num_nodes + 1))

# Create the tree (ensure connectivity)
for i in range(1, num_nodes):
    u = random.randint(1, i)
    v = i + 1
    G.add_edge(u, v)

# Continue adding edges to avoid creating cycles
edge_seen = set((u, v) if u < v else (v, u) for u, v in G.edges())
max_edges = ((num_nodes - 1) * (num_nodes - 2)) // 2
while len(edge_seen) < max_edges:
    u = random.randint(1, num_nodes)
    v = random.randint(1, num_nodes)
    if u != v and (u, v) not in edge_seen and (v, u) not in edge_seen:
        G.add_edge(u, v)
        edge_seen.add((u, v))

# Create positions for the nodes using spring layout
pos = nx.spring_layout(G, k=0.5, seed=42)

# Convert positions to Pygame coordinates
node_positions = {node: (int(pos[node][0] * WIDTH / 2 + WIDTH / 2), int(pos[node][1] * HEIGHT / 2 + HEIGHT / 2)) for node in G.nodes()}

# Node properties
node_radius = 20
node_color = (135, 206, 235)  # Sky blue
edge_color = (169, 169, 169)  # Dark gray

# Create a list to track dragged nodes
dragged_node = None

# Function to draw the graph
def draw_graph():
    screen.fill((255, 255, 255))  # Fill the screen with white
    # Draw edges
    for u, v in G.edges():
        pygame.draw.line(screen, edge_color, node_positions[u], node_positions[v], 2)
    
    # Draw nodes
    for node in G.nodes():
        pygame.draw.circle(screen, node_color, node_positions[node], node_radius)
        font = pygame.font.SysFont(None, 20)
        label = font.render(str(node), True, (0, 0, 0))
        label_rect = label.get_rect(center=node_positions[node])
        screen.blit(label, label_rect)
    
    pygame.display.flip()

# Game loop
running = True
while running:
    draw_graph()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if any node was clicked
            mouse_pos = pygame.mouse.get_pos()
            for node, pos in node_positions.items():
                distance = ((pos[0] - mouse_pos[0]) ** 2 + (pos[1] - mouse_pos[1]) ** 2) ** 0.5
                if distance <= node_radius:
                    dragged_node = node
                    break
        
        if event.type == pygame.MOUSEBUTTONUP:
            dragged_node = None
        
        if event.type == pygame.MOUSEMOTION and dragged_node is not None:
            # Move the dragged node with the mouse
            node_positions[dragged_node] = pygame.mouse.get_pos()

    pygame.time.wait(10)

# Quit Pygame
pygame.quit()
