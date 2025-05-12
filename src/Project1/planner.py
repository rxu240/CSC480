import sys
import heapq

class Planner:
    def __init__(self, world):
        self.cols, self.rows, self.start, self.grid, initial_dirty = self.load_world(world)
        self.initial_dirty = frozenset(initial_dirty)

    def load_world(self,world):
        with open(world, 'r') as w:
            cols = int(w.readline())
            rows = int(w.readline())
            start = None
            grid = []
            dirty = set()

            for r, line in enumerate(w):
                clean = list(line.rstrip('\n'))
                for c, ch in enumerate(clean):
                    if (ch=='@'):
                        start = (r,c)
                    elif (ch=='*'):
                        dirty.add((r,c))
                grid.append(clean)

        return cols, rows, start, grid, dirty
    
    # Goal hit when no '*' remains in state.
    def is_goal(self, state):
        _, remaining = state
        return len(remaining) == 0

    # Valid when in bounds and not blocked
    def is_valid(self,row, col):
        return (0 <= row < self.rows
                and 0 <= col < self.cols
                and self.grid[row][col] != '#')

    # implement motion, bounds-checks, walls, and vacuum
    def successors(self, state):
        (r, c), dirty = state

        # Move 
        for rowchange, colchange, direction in [
            (-1,0,'N'), 
            (1,0,'S'), 
            (0,-1,'W'), 
            (0,1,'E')]:

            newrow, newcol = r+rowchange, c+colchange
            if self.is_valid(newrow, newcol):
                yield direction, 1, ((newrow, newcol), dirty)

        # Vacuum
        if (r, c) in dirty:
            new_dirty = dirty - {(r, c)}
            yield 'V', 1, ((r, c), frozenset(new_dirty))

    def dfs(self):
        initial = (self.start, self.initial_dirty)
        stack = [(initial, [])]   
        stack_set = {initial}     
        explored = set()

        nodes_generated = 1
        nodes_expanded  = 0

        while stack:
            state, path = stack.pop()
            stack_set.remove(state)

            if self.is_goal(state):
                return path, nodes_generated, nodes_expanded

            explored.add(state)
            nodes_expanded += 1

            for direction, _, next in self.successors(state):
                if next in explored or next in stack_set:
                    continue
                stack.append((next, path + [direction]))
                stack_set.add(next)
                nodes_generated += 1

        return [], nodes_generated, nodes_expanded

    def ufs(self):
        initial = (self.start, self.initial_dirty)
        # priority queue of cumulative_cost, state, path
        queue = [(0, initial, [])]
        queue_cost = {initial: 0}
        explored = set()

        nodes_generated = 1
        nodes_expanded  = 0

        while queue:
            cost, state, path = heapq.heappop(queue)

            if state in explored or cost > queue_cost.get(state, float('inf')):
                continue

            if self.is_goal(state):
                return path, nodes_generated, nodes_expanded

            explored.add(state)
            nodes_expanded += 1

            for direction, step_cost, next in self.successors(state):
                new_cost = cost + step_cost
                if next in explored:
                    continue

                old_cost = queue_cost.get(next)
                if old_cost is None or new_cost < old_cost:
                    queue_cost[next] = new_cost
                    heapq.heappush(queue, (new_cost, next, path + [direction]))
                    nodes_generated += 1

        return [], nodes_generated, nodes_expanded
    
def main():
    if len(sys.argv) != 3:
        print("Usage: py planner.py [uniform-cost|depth-first] world-file.txt")
        sys.exit(1)

    algo = sys.argv[1]
    world_file = sys.argv[2]
    planner = Planner(world_file)

    if algo == 'uniform-cost':
        nodes, generated, expanded = planner.ufs()
    if algo == 'depth-first':
        nodes, generated, expanded = planner.dfs()

    for node in nodes:
        print(node)
    print(f"{generated} nodes generated")
    print(f"{expanded} nodes expanded")

if __name__ == "__main__":
    main()