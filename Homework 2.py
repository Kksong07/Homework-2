import time


# Definition of VacuumWorld and Cost of available action 

class VacuumWorld:
    ROWS = 4  
    COLUMNS = 5  
    ACTION_COSTS = {
        'Left': 1.0,
        'Right': 0.9,
        'Up': 0.8,
        'Down': 0.7,
        'Suck': 0.6
    }
    ACTIONS = ['Left', 'Right', 'Up', 'Down', 'Suck'] 

    def __init__(self, initial_position, dirty_squares):
        self.grid = [[' ' for _ in range(self.COLUMNS)] for _ in range(self.ROWS)]
        self.agent_position = initial_position
        self.dirty_squares = set(dirty_squares)
        self.total_cost = 0.0
        self.place_agent(initial_position)
        self.place_dirt()
        self.expanded_nodes = []  # To store first 5 expanded nodes
        self.nodes_expanded_count = 0  # Count total number of nodes expanded
        self.nodes_generated_count = 0  # Count total number of nodes generated
        self.execution_time = 0.0  # To store CPU execution time

    def place_agent(self, position):
        row, col = position
        self.grid[row-1][col-1] = 'A'  # Place the agent in the grid
    
    def place_dirt(self):
        for row, col in self.dirty_squares:
            self.grid[row-1][col-1] = 'D'  # Mark the grid as dirty (D)

    def move_agent(self, direction, agent_position, dirty_squares):
        row, col = agent_position

        # Suck' action with action cost 
        if direction == 'Suck':
            if (row, col) in dirty_squares:
                dirty_squares.remove((row, col)) 
            return (row, col), dirty_squares, self.ACTION_COSTS[direction]

        # Movement with action cost
        if direction == 'Left' and col > 1:
            col -= 1
        elif direction == 'Right' and col < self.COLUMNS:
            col += 1
        elif direction == 'Up' and row > 1:
            row -= 1
        elif direction == 'Down' and row < self.ROWS:
            row += 1

        # Return new agent position, dirty squares, and the cost of the action
        return (row, col), dirty_squares, self.ACTION_COSTS[direction]

    def is_goal(self, dirty_squares):
        return len(dirty_squares) == 0

    
    
    
# Iterative deepning search Algorithm 

    def iterative_deepening_search(self, max_depth):
        for depth in range(max_depth + 1):
            result = self.depth_limited_search(self.agent_position, self.dirty_squares, depth)   # For each depth execute detph_search 
            if result is not None:
                return result                # IF solution found at detph return soltuion if not return None 
        return None 

    def depth_limited_search(self, agent_position, dirty_squares, limit):
        return self.recursive_dls(agent_position, dirty_squares, [], 0, limit)

    # Checking for all possible actions in depth 
    def recursive_dls(self, agent_position, dirty_squares, path, current_depth, limit):
        # Tracking expanded node
        self.track_expanded_node(agent_position, path)

        # Check current state acheives goal state (cleaning all dirt)
        if self.is_goal(dirty_squares):
            return path 
        
        # If reached depth limit, stop searching
        if current_depth >= limit:
            return None

        # Explore all possible actions from the current state (if it can take right, left or others)
        for action in self.ACTIONS:
            self.nodes_generated_count += 1 # checking how many nodes have been generated 
            
            new_position, new_dirty_squares, cost = self.move_agent(action, agent_position, dirty_squares.copy())
            new_path = path + [(action, new_position, cost)]

            # Recursively search with the updated state
            result = self.recursive_dls(new_position, new_dirty_squares, new_path, current_depth + 1, limit)
            if result is not None:
                return result  # Solution found along this path
        
        return None  # X solution found at depth

    def track_expanded_node(self, agent_position, path):
        # Increment the counter for each node expanded
        self.nodes_expanded_count += 1

        # Store the first 5 unique expanded nodes (without dirty squares)
        state = agent_position
        if len(self.expanded_nodes) < 5 and state not in [node[0] for node in self.expanded_nodes]:
            self.expanded_nodes.append((agent_position, path))

            
            
            
# For Output 
# 1) First 5 search nodes 
    def print_summary(self, solution):
        print("First 5 expanded search nodes:")
        for idx, (position, path) in enumerate(self.expanded_nodes):
            print(f"Node {idx + 1}:")
            print(f"  Agent Position: {position}")
            print(f"  Path: {path}")
            print()

# 2) total node expanded 
        print(f"Total number of nodes expanded: {self.nodes_expanded_count}")
    
# 3) total node generated 
        print(f"Total number of nodes generated: {self.nodes_generated_count}")
    
# 4) execution time 
        print(f"CPU execution time: {self.execution_time:.6f} seconds")

# 5) Solution Output 
        if solution:
    # Calculate total cost
            total_cost = sum(cost for _, _, cost in solution)

    # Print the sequence of moves
            moves = [action for action, _, _ in solution]
            print("Sequence of moves:", " -> ".join(moves))
            print(f"Total number of moves: {len(moves)}")
            print(f"Total cost of solution: {total_cost:.2f}")  
            
            

# Function to run seperate Instances 

def run_vacuum_world(initial_position, dirty_squares, max_depth):
    
    # Initialize the vacuum world
    vacuum_world = VacuumWorld(initial_position, dirty_squares)

    # Measure the CPU execution time
    start_time = time.time()

    # Perform iterative deepening search
    solution = vacuum_world.iterative_deepening_search(max_depth)

    # Record the end time and calculate the CPU execution time
    end_time = time.time()
    vacuum_world.execution_time = end_time - start_time

    # Print the summary for the instance
    vacuum_world.print_summary(solution)
            
 
            


# In[14]:


# Instance #1 
initial_position_1 = (2, 2)
dirty_squares_1 = [(1, 2), (2, 4), (3, 5)]

# Found solution in 9 depth 
run_vacuum_world(initial_position_1, dirty_squares_1, max_depth=10)


# In[15]:


# Instance #2
initial_position_2 = (3, 2)
dirty_squares_2 = [(1, 2), (2, 1), (2, 4), (3, 3)]

# Found solution in 12 depth 
run_vacuum_world(initial_position_2, dirty_squares_2, max_depth=13)


# In[ ]:




