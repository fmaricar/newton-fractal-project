"""Grid pathfinding: A* (and Dijkstra as the h=0 special case)."""
import heapq
import random

Cell = tuple  # (row, col)


def make_grid(rows, cols, wall_prob=0.28, seed=0):
    """Random grid; 1 = wall, 0 = open. Start (0,0) and goal (rows-1,cols-1) are kept open."""
    rng = random.Random(seed)
    grid = [[1 if rng.random() < wall_prob else 0 for _ in range(cols)] for _ in range(rows)]
    grid[0][0] = grid[rows - 1][cols - 1] = 0
    return grid


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid, start, goal, heuristic=manhattan):
    """4-connected A*. Returns (path or None, cells in the order they were expanded).

    With the Manhattan heuristic (admissible and consistent on a unit-cost
    4-connected grid) the returned path is a shortest path.
    """
    rows, cols = len(grid), len(grid[0])
    open_heap = [(heuristic(start, goal), 0, start)]
    g_cost = {start: 0}
    parent = {start: None}
    closed, expanded = set(), []

    while open_heap:
        _, g, cur = heapq.heappop(open_heap)
        if cur in closed:
            continue
        closed.add(cur)
        expanded.append(cur)
        if cur == goal:
            path = []
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            return path[::-1], expanded
        r, c = cur
        for nxt in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            nr, nc = nxt
            if not (0 <= nr < rows and 0 <= nc < cols) or grid[nr][nc] or nxt in closed:
                continue
            ng = g + 1
            if ng < g_cost.get(nxt, float("inf")):
                g_cost[nxt] = ng
                parent[nxt] = cur
                heapq.heappush(open_heap, (ng + heuristic(nxt, goal), ng, nxt))
    return None, expanded


def dijkstra(grid, start, goal):
    return astar(grid, start, goal, heuristic=lambda a, b: 0)
