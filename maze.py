import random
import pygame
import timeit

N, S, E, W = 0, 1, 2, 3
directions = {N: (0, -1), S: (0, 1), E: (-1, 0), W: (1, 0)}
opposite = {N: S, S: N, E: W, W: E}

def next_coord(x, y, adj):
    return x + directions[adj][0], y + directions[adj][1]

class Cell:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.visited = False
        #N, S, E, W
        self.walls = [True, True, True, True]
        self.color = (240, 210, 190)
    
    def visit(self):
        self.visited = True
    
    def draw(self, screen):
        draw_x = self.x*self.size
        draw_y = self.y*self.size

        if self.walls[N]:
            pygame.draw.line(screen, self.color, (draw_x, draw_y), (draw_x+self.size, draw_y))
        if self.walls[W]:
            pygame.draw.line(screen, self.color, (draw_x+self.size, draw_y), (draw_x+self.size, draw_y+self.size))
        if self.walls[S]:
            pygame.draw.line(screen, self.color, (draw_x, draw_y+self.size), (draw_x+self.size, draw_y+self.size))
        if self.walls[E]:
            pygame.draw.line(screen, self.color, (draw_x, draw_y), (draw_x, draw_y+self.size))

def interative_maze(cx, cy, grid):
    path = {(cx, cy): 0}

    while len(path) != 0:
            adjacent = [N, S, E, W]
            random.shuffle(adjacent)

            for adj in adjacent:
                nx, ny = next_coord(cx, cy, adj)

                if 0 <= ny < len(grid) and 0 <= nx < len(grid[ny]) and not grid[ny][nx].visited:
                    # num_of_walls = 0
                    # for wall in grid[ny][nx].walls:
                    #     if wall:
                    #         num_of_walls += 1
                    # if num_of_walls > 3:
                    if grid[ny][nx].walls.count(True) > 3:
                        grid[cy][cx].visit()
                        grid[cy][cx].walls[adj] = False
                        grid[ny][nx].walls[opposite[adj]] = False
                        path[(cx, cy)] = (nx, ny)
                        cx, cy = nx, ny
                        break
            else:
                cx, cy = list(path.values())[-1]
                path.popitem()

def recursive_maze(cx, cy, grid):
    adjacent = [N, S, E, W]
    random.shuffle(adjacent)

    for adj in adjacent:
        nx, ny = next_coord(cx, cy, adj)

        if 0 <= ny < len(grid) and 0 <= nx < len(grid[ny]) and not grid[ny][nx].visited:
            # num_of_walls = 0
            # for wall in grid[ny][nx].walls:
            #     if wall:
            #         num_of_walls += 1
            # if num_of_walls > 3:
            if grid[ny][nx].walls.count(True) > 3:
                grid[cy][cx].visit()
                grid[cy][cx].walls[adj] = False
                grid[ny][nx].walls[opposite[adj]] = False
                recursive_maze(nx, ny, grid)

def generate_maze(width, height, size, method=None, seed=0):
    if seed != 0:
        random.seed(seed)

    grid = [[Cell(x, y, size) for x in range(width)] for y in range(height)]

    if method != None:
        method(0, 0, grid)

    return grid

def draw_maze(screen, grid):
    for row in grid:
        for cell in row:
            cell.draw(screen)

def time_maze(width, height, size, method, repeat=3, number=1):
    t = timeit.Timer(lambda: generate_maze(width, height, size, method))

    results = t.repeat(repeat, number)
    print(method.__name__, " Average Time:", sum(results)/len(results))

if __name__ == "__main__":
    time_maze(10, 10, 10, interative_maze, 5)
    time_maze(10, 10, 10, recursive_maze, 5)

    width = 600
    height = 600
    size = 20
    
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("RayCasting")

    clock = pygame.time.Clock()

    maze = generate_maze(width//size, height//size, size)

    cx, cy = 0, 0
    path = {(cx, cy): 0}

    running = True
    while running:
        clock.tick(60)

        if len(path) != 0:
            adjacent = [N, S, E, W]
            random.shuffle(adjacent)

            for adj in adjacent:
                nx, ny = next_coord(cx, cy, adj)

                if 0 <= ny < len(maze) and 0 <= nx < len(maze[ny]) and not maze[ny][nx].visited:
                    num_of_walls = 0
                    for wall in maze[ny][nx].walls:
                        if wall:
                            num_of_walls += 1
                    if num_of_walls > 3:
                        maze[cy][cx].visit()
                        maze[cy][cx].walls[adj] = False
                        maze[ny][nx].walls[opposite[adj]] = False
                        path[(cx, cy)] = (nx, ny)
                        cx, cy = nx, ny
                        break
            else:
                cx, cy = list(path.values())[-1]
                path.popitem()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.KMOD_LCTRL:
                    running = False

                if event.key == pygame.K_SPACE:
                    maze = generate_maze(width//size, height//size, size)
                    cx, cy = 0, 0
                    path = {(cx, cy): 0}

        screen.fill((0, 0, 0))
        draw_maze(screen, maze)
        pygame.draw.rect(screen, (0, 0, 255), (cx*size, cy*size, size, size))

        pygame.display.update()
pygame.quit()