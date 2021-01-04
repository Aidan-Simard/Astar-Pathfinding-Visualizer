import pygame
import math
import random

pygame.init()

width = 1002
height = 1002

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (150, 150, 150)
LIGHT_GREY = (220, 220, 220)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)

screen = pygame.display.set_mode((width, height))

class Node():
    def __init__(self, x, y, color=GREY, wall=False, seen=False):
        self.x = x
        self.y = y
        self.color = color
        self.wall = wall
        self.seen = seen
        self.neighbours = []
    
    def update_node_color(self, color):
        # Updates the color of a node. Black nodes are walls and blue nodes have been seen.
        self.color = color
        if self.color == BLACK:
            self.wall = True
        if self.color == BLUE:
            self.seen = True

    def update_node_neighbours(self):
        # Updates valid neighbours of a node in 8 directions.

        self.neighbours = []

        if self.y > 0 and graph.graph[self.y-1][self.x].wall == False:
            self.neighbours.append(graph.graph[self.y-1][self.x])
        
        if self.x < 49 and graph.graph[self.y][self.x+1].wall == False:
            self.neighbours.append(graph.graph[self.y][self.x+1])

        if self.y < 49 and graph.graph[self.y+1][self.x].wall == False:
            self.neighbours.append(graph.graph[self.y+1][self.x])

        if self.x > 0 and graph.graph[self.y][self.x-1].wall == False:
            self.neighbours.append(graph.graph[self.y][self.x-1])

        if self.x > 0 and self.y > 0 and graph.graph[self.y-1][self.x-1].wall == False:
            if graph.graph[self.y-1][self.x].wall == False and graph.graph[self.y][self.x-1].wall == False:
                self.neighbours.append(graph.graph[self.y-1][self.x-1])

        if self.x < 49 and self.y < 49 and graph.graph[self.y+1][self.x+1].wall == False:
            if graph.graph[self.y][self.x+1].wall == False and graph.graph[self.y+1][self.x].wall == False:
                self.neighbours.append(graph.graph[self.y+1][self.x+1])

        if self.x > 0 and self.y < 49 and graph.graph[self.y+1][self.x-1].wall == False:
            if graph.graph[self.y][self.x-1].wall == False and graph.graph[self.y+1][self.x].wall == False:
                self.neighbours.append(graph.graph[self.y+1][self.x-1])
        
        if self.x < 49 and self.y > 0 and graph.graph[self.y-1][self.x+1].wall == False:
            if graph.graph[self.y][self.x+1].wall == False and graph.graph[self.y-1][self.x].wall == False:
                self.neighbours.append(graph.graph[self.y-1][self.x+1])

class Graph():
    def __init__(self):
        self.graph = []
        self.start = None
        self.end = None
        self.seen_nodes = []
        self.wall_nodes = []
        self.found = False
        self.path = []

    def create_graph(self):
        # Creates a 2D list of nodes
        for y in range(0, 50):
            row = []
            for x in range(0, 50):
                row.append(Node(x, y))
            self.graph.append(row)

    def fill_node(self, node, color=GREY):
        # Fills a node in the graph with some color
        node.update_node_color(color)
        pygame.draw.rect(screen, node.color, (node.x*20+2, node.y*20+2, 18, 18))

    def fill_seen_nodes(self):
        # Fills all nodes that have been seen by the pathfinding algorithm
        for node in self.seen_nodes:
            self.fill_node(node, BLUE)

    def fill_start_node(self):
        # Fills the start node with green
        self.fill_node(self.start, GREEN)

    def fill_end_node(self):
        # Fills the end node with red
        self.fill_node(self.end, RED)
    
    def fill_wall_nodes(self):
        # Fills all wall nodes in the graph
        for node in self.wall_nodes:
            self.fill_node(node, BLACK)

    def fill_path_nodes(self):
        # Fills all nodes in the path from the start to end node
        for node in self.path:
            self.fill_node(node, PURPLE)
    
    def update_all_node_neighbours(self):
        # Updates the neighbours of each node in the graph
        for row in range(len(self.graph)):
            for col in range(len(self.graph)):
                self.graph[row][col].update_node_neighbours()

    def astar(self):
        # Open set is used to determine if there are more nodes that can be explored
        opn = set()
        # Closed set is all nodes that no longer have to be explored
        closed = set()
        # Dictionary with the path of each node
        cameFrom = {}
        # Distance from the start node to every other node
        g = {node: math.inf for row in self.graph for node in row}
        g[self.start] = 0
        # Sum of the "g" value and the heuristic (heuristic is the distance from some node to the end node)
        f = {node: math.inf for row in self.graph for node in row}
        f[self.start] = heuristic(self.start, self.end)

        opn.add(self.start)

        while len(opn) != 0:
            # Allows user to exit the window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            pygame.time.wait(10)

            # Gets the node with the smallest "f" value. 
            # Can be optimized with priority queue
            current = get_min_open(closed, opn, f)

            if current is self.end:
                # End node is found -> Create the path from the start to the end node
                self.found = True
                self.construct_path(current, cameFrom)
                return
            
            opn.remove(current)
            closed.add(current)

            # Update the window with seen nodes 
            graph.fill_seen_nodes()
            pygame.display.update()

            for neighbour in current.neighbours:
                # Skip each neighbour that has already been explored
                if neighbour in closed:
                    continue
                
                # Distance from neighbour to the start node
                tmp = g[current] + 1

                if tmp < g[neighbour]:
                    cameFrom[neighbour] = current
                    g[neighbour] = tmp
                    f[neighbour] = g[neighbour] + heuristic(neighbour, self.end)

                    if neighbour not in opn:
                        opn.add(neighbour)

                        # Only add nodes that are not the start and end nodes to the seen nodes
                        if (neighbour.x, neighbour.y) != (self.start.x, self.start.y) and (neighbour.x, neighbour.y) != (self.end.x, self.end.y):
                            self.seen_nodes.append(neighbour)

        # Path was not found - Setting found to True so that the main does not try to find the path again
        self.found = True
        return
    
    def construct_path(self, node, cameFrom):
        # Finds the path from the start to the end nodes
        node = cameFrom[node]
        while node != self.start:
            self.path.append(node)
            node = cameFrom[node]
    
def get_min_open(closed, opn, f):
    # Finds the node with the smallest "f" value in dictionary f
    m = list(opn)[0]
    for node in f:
        if node in opn and node not in closed:
            if f[node] < f[m]:
                m = node 
    return m

def heuristic(start, end):
    # Distance from some node to another node
    d_max = max(abs(start.x-end.x), abs(start.y-end.y))
    d_min = min(abs(start.x-end.x), abs(start.y-end.y))
    return 14*d_min+10*(d_max-d_min)

def draw_grid():
    # Draws a grid
    for var in range(0, 1020, 20):
        pygame.draw.line(screen, GREY, (var, 0), (var, 1000), 2)
        pygame.draw.line(screen, GREY, (0, var), (1000, var), 2)
    
def find_coords(y, x):
    # Find the graph coordinates given coordinates from the screen
    return (x//20, y//20)

graph = Graph()
graph.create_graph()
graph.update_all_node_neighbours()

# MAIN
#
# Note that diagonal distances are not considered to be more expensive than "inline" distances
#
# 1. First click sets the start node
# 2. Second click sets the end node
# 3. Hold down mouse and draw walls
# 4. Pressing space begins the search 

def main():
    running = True
    space = False
    FPS = 120
    clock = pygame.time.Clock()

    while running:
        clock.tick(FPS)        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(LIGHT_GREY)
        draw_grid()

        while graph.start is None:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    pos = find_coords(pos[1], pos[0])
                    graph.start = graph.graph[pos[1]][pos[0]]
                if event.type == pygame.QUIT:
                    pygame.quit()
            pygame.display.update()

        graph.fill_start_node()

        while graph.end is None:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    pos = find_coords(pos[1], pos[0])
                    graph.end = graph.graph[pos[1]][pos[0]]
                if event.type == pygame.QUIT:
                    pygame.quit()                    
            pygame.display.update()

        graph.fill_end_node()

        while space == False:
            for event in pygame.event.get():
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    pos = find_coords(pos[0], pos[1])
                    if 0 <= pos[0] <= 49 and 0 <= pos[1] <= 49 and graph.graph[pos[0]][pos[1]] != graph.start and graph.graph[pos[0]][pos[1]] != graph.end:
                        graph.graph[pos[0]][pos[1]].wall = True
                        graph.wall_nodes.append(graph.graph[pos[0]][pos[1]])

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        space = True
                
                if event.type == pygame.QUIT:
                    pygame.quit()
        
            graph.fill_wall_nodes()
            pygame.display.update()

        if space == True and graph.found == False:
            graph.update_all_node_neighbours()
            graph.astar()

        graph.fill_wall_nodes()
        graph.fill_seen_nodes()
        graph.fill_path_nodes()
        pygame.display.update()

main()