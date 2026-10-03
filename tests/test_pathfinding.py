import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from pathfinding import astar, dijkstra, make_grid


class PathfindingTest(unittest.TestCase):
    def test_open_grid_is_manhattan(self):
        grid = [[0] * 5 for _ in range(4)]
        path, _ = astar(grid, (0, 0), (3, 4))
        self.assertEqual(len(path) - 1, 7)

    def test_no_path(self):
        grid = [[0, 1, 0], [0, 1, 0], [0, 1, 0]]
        path, _ = astar(grid, (0, 0), (0, 2))
        self.assertIsNone(path)

    def test_path_is_valid(self):
        grid = make_grid(20, 30, seed=3)
        path, _ = astar(grid, (0, 0), (19, 29))
        if path:
            for (r1, c1), (r2, c2) in zip(path, path[1:]):
                self.assertEqual(abs(r1 - r2) + abs(c1 - c2), 1)
            self.assertTrue(all(grid[r][c] == 0 for r, c in path))

    def test_matches_dijkstra_and_expands_less(self):
        for seed in range(20):
            grid = make_grid(20, 30, seed=seed)
            pa, ea = astar(grid, (0, 0), (19, 29))
            pd, ed = dijkstra(grid, (0, 0), (19, 29))
            self.assertEqual(pa is None, pd is None)
            if pa:
                self.assertEqual(len(pa), len(pd))
                self.assertLessEqual(len(ea), len(ed))


if __name__ == "__main__":
    unittest.main()
