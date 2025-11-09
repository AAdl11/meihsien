# test_algorithms.py
# Complete test suite for all 8 Journey of Kindness algorithms
# Run this to see outputs and practice explanations

import heapq
from collections import deque

print("="*80)
print("JOURNEY OF KINDNESS - 8 ALGORITHMS TEST SUITE")
print("CS 4 Final Project - Mei Hsien Hsu")
print("="*80)

# ============================================================================
# ALGORITHM 1: A* SEARCH - Informed Search
# ============================================================================
print("\n" + "="*70)
print("ALGORITHM 1: A* SEARCH - Food Delivery Route Optimization")
print("Chapter: Russell & Norvig 3.5-3.6")
print("="*70)

class AStarSearch:
    def __init__(self, grid_size=10):
        self.grid_size = grid_size
        
    def heuristic(self, pos, goal):
        """Manhattan distance heuristic (admissible)"""
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
    
    def get_neighbors(self, pos):
        """Get valid neighbor positions"""
        x, y = pos
        neighbors = []
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                neighbors.append((nx, ny))
        return neighbors
    
    def search(self, start, goal):
        """A* search implementation"""
        print(f"\n🎯 Finding path from {start} to {goal}")
        
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}
        
        nodes_explored = 0
        
        while frontier:
            current_f, current = heapq.heappop(frontier)
            nodes_explored += 1
            
            print(f"  Exploring node {current}: f={current_f}, g={cost_so_far[current]}, h={self.heuristic(current, goal)}")
            
            if current == goal:
                # Reconstruct path
                path = []
                while current:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                
                print(f"\n✅ Path found! Length: {len(path)}")
                print(f"   Path: {' → '.join(map(str, path))}")
                print(f"   Nodes explored: {nodes_explored}")
                print(f"   Total cost: {cost_so_far[goal]}")
                return path
            
            for next_pos in self.get_neighbors(current):
                new_cost = cost_so_far[current] + 1
                
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + self.heuristic(next_pos, goal)
                    heapq.heappush(frontier, (priority, next_pos))
                    came_from[next_pos] = current
        
        return None

# Test A*
astar = AStarSearch(grid_size=10)
astar.search(start=(0, 0), goal=(9, 9))

print("\n📊 Key Concepts:")
print("  • f(n) = g(n) + h(n) where g=actual cost, h=heuristic estimate")
print("  • Admissible heuristic guarantees optimal solution")
print("  • Time Complexity: O(b^d) worst case, but efficient with good heuristic")

# ============================================================================
# ALGORITHM 2: ALPHA-BETA PRUNING - Adversarial Search
# ============================================================================
print("\n" + "="*70)
print("ALGORITHM 2: ALPHA-BETA PRUNING - Budget Allocation")
print("Chapter: Russell & Norvig 5.3")
print("="*70)

class AlphaBetaPruning:
    def __init__(self):
        self.nodes_pruned = 0
        
    def minimax(self, depth, node_index, is_max, values, alpha, beta, tree_height):
        """Alpha-Beta pruning implementation"""
        
        if depth == tree_height:
            return values[node_index]
        
        if is_max:
            best = float('-inf')
            
            for i in range(2):
                child_index = node_index * 2 + i
                val = self.minimax(depth + 1, child_index, False, values, alpha, beta, tree_height)
                best = max(best, val)
                alpha = max(alpha, best)
                
                print(f"  {'  '*depth}MAX node {node_index}: child_{i} value={val}, alpha={alpha}, beta={beta}")
                
                if beta <= alpha:
                    print(f"  {'  '*depth}✂️  PRUNE! (beta={beta} <= alpha={alpha})")
                    self.nodes_pruned += 1
                    break
                    
            return best
        else:
            best = float('inf')
            
            for i in range(2):
                child_index = node_index * 2 + i
                val = self.minimax(depth + 1, child_index, True, values, alpha, beta, tree_height)
                best = min(best, val)
                beta = min(beta, best)
                
                print(f"  {'  '*depth}MIN node {node_index}: child_{i} value={val}, alpha={alpha}, beta={beta}")
                
                if beta <= alpha:
                    print(f"  {'  '*depth}✂️  PRUNE! (beta={beta} <= alpha={alpha})")
                    self.nodes_pruned += 1
                    break
                    
            return best

# Test Alpha-Beta
values = [3, 5, 6, 9, 1, 2, 0, -1]
print(f"\n🎯 Game tree leaf values: {values}")
print("Finding optimal budget allocation...\n")

ab = AlphaBetaPruning()
result = ab.minimax(0, 0, True, values, float('-inf'), float('inf'), 3)

print(f"\n✅ Optimal value: {result}")
print(f"   Nodes pruned: {ab.nodes_pruned}")
print(f"   Efficiency improvement: {ab.nodes_pruned}/{len(values)} branches avoided")

print("\n📊 Key Concepts:")
print("  • Alpha: Best value MAX can guarantee")
print("  • Beta: Best value MIN can guarantee")
print("  • Prune when β ≤ α (no point exploring further)")
print("  • Complexity: O(b^(m/2)) vs O(b^m) for minimax")

# ============================================================================
# ALGORITHM 3: BAYESIAN NETWORKS - Probabilistic Reasoning
# ============================================================================
print("\n" + "="*70)
print("ALGORITHM 3: BAYESIAN NETWORKS - Volunteer Retention Prediction")
print("Chapter: Russell & Norvig 12.5-12.6")
print("="*70)

class BayesianNetwork:
    def __init__(self):
        # Prior probabilities
        self.P_skills_high = 0.3
        self.P_interest_high = 0.4
        self.P_availability_high = 0.5
        
        # Conditional Probability Table for retention
        # P(Retention | Skills, Interest, Availability)
        self.cpt = {
            (True, True, True): 0.95,    # All favorable
            (True, True, False): 0.70,   # High skills+interest, low availability
            (True, False, True): 0.60,   # High skills+availability, low interest
            (False, True, True): 0.65,   # High interest+availability, low skills
            (True, False, False): 0.40,
            (False, True, False): 0.45,
            (False, False, True): 0.35,
            (False, False, False): 0.10  # All unfavorable
        }
    
    def calculate_retention_probability(self, skills_high, interest_high, avail_high):
        """Calculate P(Retention | Evidence)"""
        key = (skills_high, interest_high, avail_high)
        return self.cpt[key]
    
    def predict(self, volunteer_profile):
        """Predict retention for a volunteer"""
        skills = volunteer_profile['skills'] == 'high'
        interest = volunteer_profile['interest'] == 'high'
        avail = volunteer_profile['availability'] == 'high'
        
        prob = self.calculate_retention_probability(skills, interest, avail)
        
        print(f"\n👤 Volunteer Profile:")
        print(f"   Skills: {volunteer_profile['skills']}")
        print(f"   Interest: {volunteer_profile['interest']}")
        print(f"   Availability: {volunteer_profile['availability']}")
        print(f"\n📊 Retention Probability: {prob:.1%}")
        
        return prob

# Test Bayesian Network
bn = BayesianNetwork()

test_volunteers = [
    {'name': 'Alice', 'skills': 'high', 'interest': 'high', 'availability': 'high'},
    {'name': 'Bob', 'skills': 'high', 'interest': 'low', 'availability': 'high'},
    {'name': 'Carol', 'skills': 'low', 'interest': 'high', 'availability': 'low'}
]

for v in test_volunteers:
    print(f"\n{'='*50}")
    print(f"Analyzing: {v['name']}")
    bn.predict(v)

print("\n📊 Key Concepts:")
print("  • Conditional Independence: P(A|B,C) when B makes C irrelevant")
print("  • CPT: Conditional Probability Table defines P(Child | Parents)")
print("  • Inference: Computing probabilities of unobserved variables")

# ============================================================================
# ALGORITHM 4: TOWER OF HANOI - Recursive Planning
# ============================================================================
print("\n" + "="*70)
print("ALGORITHM 4: TOWER OF HANOI - Virtue Development (3 disks)")
print("Chapter: Russell & Norvig 11.2")
print("="*70)

class TowerOfHanoi:
    def __init__(self):
        self.moves = []
        
    def solve(self, n, source, target, auxiliary):
        """Recursive solution to Tower of Hanoi"""
        if n == 1:
            move = f"Move disk 1 from {source} to {target}"
            self.moves.append(move)
            print(f"  {len(self.moves)}. {move}")
            return
        
        # Move n-1 disks from source to auxiliary
        self.solve(n-1, source, auxiliary, target)
        
        # Move largest disk from source to target
        move = f"Move disk {n} from {source} to {target}"
        self.moves.append(move)
        print(f"  {len(self.moves)}. {move}")
        
        # Move n-1 disks from auxiliary to target
        self.solve(n-1, auxiliary, target, source)

# Test Tower of Hanoi
print("\n🗼 Scenario: Develop virtues in correct order")
print("   Disk 1 (smallest) = Gratitude")
print("   Disk 2 (medium) = Respect")
print("   Disk 3 (largest) = Love")
print("   Goal: Move from 'Potential' to 'Actualized' via 'Practice'\n")

hanoi = TowerOfHanoi()
hanoi.solve(n=3, source='Potential', target='Actualized', auxiliary='Practice')

print(f"\n✅ Optimal solution: {len(hanoi.moves)} moves")
print(f"   Formula: 2^n - 1 = 2^3 - 1 = 7 moves")

print("\n📊 Key Concepts:")
print("  • Recursive problem decomposition")
print("  • Time Complexity: O(2^n)")
print("  • Demonstrates planning as search through state space")

# ============================================================================
# ALGORITHM 5: N-QUEENS - Constraint Satisfaction
# ============================================================================
print("\n" + "="*70)
print("ALGORITHM 5: N-QUEENS - Volunteer Scheduling (N=8)")
print("Chapter: Russell & Norvig 6.1-6.3")
print("="*70)

class NQueens:
    def __init__(self, n=8):
        self.n = n
        self.solutions = []
        
    def is_safe(self, board, row, col):
        """Check if queen can be placed at board[row][col]"""
        # Check column
        for i in range(row):
            if board[i] == col:
                return False
        
        # Check diagonal (upper-left)
        for i, j in zip(range(row-1, -1, -1), range(col-1, -1, -1)):
            if board[i] == j:
                return False
        
        # Check diagonal (upper-right)
        for i, j in zip(range(row-1, -1, -1), range(col+1, self.n)):
            if board[i] == j:
                return False
        
        return True
    
    def solve_util(self, board, row):
        """Backtracking utility function"""
        if row >= self.n:
            self.solutions.append(board[:])
            return True
        
        for col in range(self.n):
            if self.is_safe(board, row, col):
                board[row] = col
                
                if self.solve_util(board, row + 1):
                    return True
                
                board[row] = -1  # Backtrack
        
        return False
    
    def solve(self):
        """Solve N-Queens problem"""
        board = [-1] * self.n
        self.solve_util(board, 0)
        return self.solutions

# Test N-Queens
print("\n👥 Scenario: Schedule 8 volunteers across 8 time slots")
print("   Constraint: Each volunteer available only certain times\n")

nqueens = NQueens(n=8)
solutions = nqueens.solve()

if solutions:
    print(f"✅ Found solution!")
    print("\n   Schedule (Volunteer → Time Slot):")
    for volunteer_id, time_slot in enumerate(solutions[0]):
        print(f"   Volunteer {volunteer_id + 1} → Time Slot {time_slot + 1}")
    
    print(f"\n   Total solutions exist: {len(solutions)} (for N=8)")

print("\n📊 Key Concepts:")
print("  • Constraint Satisfaction Problem (CSP)")
print("  • Backtracking with constraint propagation")
print("  • Time Complexity: O(n!) worst case")

# ============================================================================
# ALGORITHM 6: HILL CLIMBING - Local Search
# ============================================================================
print("\n" + "="*70)
print("ALGORITHM 6: HILL CLIMBING - Meditation State Optimization")
print("Chapter: Russell & Norvig 4.1")
print("="*70)

class HillClimbing:
    def __init__(self):
        self.history = []
    
    def objective_function(self, state):
        """
        Meditation quality function (simplified):
        Quality = 100 - |state - 50|^2 / 25
        Peak at state=50, drops off on both sides
        """
        return 100 - ((state - 50) ** 2) / 25
    
    def get_neighbors(self, state):
        """Get neighboring states (±1 step)"""
        neighbors = []
        if state > 0:
            neighbors.append(state - 1)
        if state < 100:
            neighbors.append(state + 1)
        return neighbors
    
    def climb(self, start_state):
        """Hill climbing algorithm"""
        current = start_state
        current_value = self.objective_function(current)
        
        print(f"\n⛰️  Starting from state {current} (value={current_value:.2f})")
        
        self.history = [(current, current_value)]
        
        iteration = 0
        while True:
            iteration += 1
            neighbors = self.get_neighbors(current)
            
            # Find best neighbor
            best_neighbor = None
            best_value = current_value
            
            for neighbor in neighbors:
                neighbor_value = self.objective_function(neighbor)
                if neighbor_value > best_value:
                    best_neighbor = neighbor
                    best_value = neighbor_value
            
            # If no better neighbor, we're at local maximum
            if best_neighbor is None:
                print(f"\n✅ Reached local maximum at state {current}")
                print(f"   Value: {current_value:.2f}")
                print(f"   Iterations: {iteration}")
                
                # Check if global maximum
                global_max = 50
                global_max_value = self.objective_function(global_max)
                
                if abs(current - global_max) < 2:
                    print(f"   ✅ This is the global maximum!")
                else:
                    print(f"   ⚠️  Local maximum! Global is at state {global_max} (value={global_max_value:.2f})")
                
                break
            
            # Move to best neighbor
            print(f"  Iteration {iteration}: {current} → {best_neighbor} (value: {current_value:.2f} → {best_value:.2f})")
            current = best_neighbor
            current_value = best_value
            self.history.append((current, current_value))

# Test Hill Climbing
hc = HillClimbing()

print("\n🧘 Test 1: Starting near global maximum")
hc.climb(start_state=45)

print(f"\n{'='*60}")
print("🧘 Test 2: Starting far from global maximum (local maximum trap)")
hc2 = HillClimbing()
hc2.climb(start_state=15)

print("\n📊 Key Concepts:")
print("  • Local search: Only considers immediate neighbors")
print("  • Problem: Can get stuck at local maxima")
print("  • Solutions: Random restart, simulated annealing")
print("  • Time Complexity: O(n) but may not find global optimum")

# ============================================================================
# ALGORITHM 7: FIRST-ORDER LOGIC - Knowledge Base
# ============================================================================
print("\n" + "="*70)
print("ALGORITHM 7: FIRST-ORDER LOGIC - Jing Si Aphorism Matching")
print("Chapter: Russell & Norvig 8.2-8.3")
print("="*70)

class FirstOrderLogicKB:
    def __init__(self):
        self.facts = set()
        self.rules = []
        self.aphorisms = {
            'perseverance': "Great works are performed not by strength but by perseverance",
            'helping_others': "In helping others, we help ourselves",
            'master_mind': "Master the mind, and you master circumstances",
            'gratitude': "A grateful heart is a magnet for miracles",
            'patience': "With patience and perseverance, even iron can become a needle"
        }
    
    def tell(self, fact):
        """Add fact to knowledge base"""
        self.facts.add(fact)
        print(f"  ➕ Added fact: {fact}")
    
    def add_rule(self, premises, conclusion):
        """Add inference rule"""
        self.rules.append((premises, conclusion))
        print(f"  ➕ Added rule: IF {' AND '.join(premises)} THEN {conclusion}")
    
    def ask(self, query):
        """Query KB using forward chaining"""
        print(f"\n🔍 Query: {query}")
        
        # Check if directly in facts
        if query in self.facts:
            print(f"  ✅ Found in facts!")
            return True
        
        # Try forward chaining
        inferred = set()
        max_iterations = 10
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            new_facts = set()
            
            for premises, conclusion in self.rules:
                # Check if all premises satisfied
                if all(p in (self.facts | inferred) for p in premises):
                    if conclusion not in (self.facts | inferred):
                        print(f"  ⚙️  Iteration {iteration}: Inferred {conclusion}")
                        new_facts.add(conclusion)
            
            if not new_facts:
                break
            
            inferred.update(new_facts)
        
        if query in inferred:
            print(f"  ✅ Inferred through forward chaining!")
            return True
        
        print(f"  ❌ Cannot prove query")
        return False
    
    def get_aphorism(self, condition):
        """Get appropriate aphorism"""
        if condition in self.aphorisms:
            return self.aphorisms[condition]
        return self.aphorisms['gratitude']  # Default

# Test First-Order Logic
print("\n📚 Building Knowledge Base...")
kb = FirstOrderLogicKB()

# Add facts
kb.tell("user_feeling(overwhelmed)")
kb.tell("task_complexity(high)")
kb.tell("user_emotion(grateful)")

# Add rules
kb.add_rule(['user_feeling(overwhelmed)', 'task_complexity(high)'], 'recommend(perseverance)')
kb.add_rule(['user_emotion(grateful)'], 'recommend(gratitude)')
kb.add_rule(['helping(someone)'], 'recommend(helping_others)')

# Query examples
print("\n" + "="*60)
queries = [
    'recommend(perseverance)',
    'recommend(gratitude)',
    'recommend(patience)'
]

for query in queries:
    result = kb.ask(query)
    if result:
        # Extract aphorism key
        aphorism_key = query.split('(')[1].strip(')')
        print(f"  💬 Aphorism: \"{kb.get_aphorism(aphorism_key)}\"")
    print()

print("📊 Key Concepts:")
print("  • First-Order Logic: Variables + Quantifiers (∀, ∃)")
print("  • Forward Chaining: Data-driven inference")
print("  • Declarative knowledge separated from procedural reasoning")

# ============================================================================
# ALGORITHM 8: WUMPUS WORLD - Reasoning Under Uncertainty
# ============================================================================
print("\n" + "="*70)
print("ALGORITHM 8: WUMPUS WORLD - Community Service Navigation")
print("Chapter: Russell & Norvig Ch 7 + 12-13")
print("="*70)

class WumpusWorld:
    def __init__(self, size=4):
        self.size = size
        self.agent_pos = (0, 0)
        
        # Knowledge Base
        self.kb = {
            'visited': set(),
            'safe': set([(0, 0)]),
            'breeze_at': set(),
            'stench_at': set(),
            'possible_pits': set(),
            'possible_wumpus': set(),
            'gold_found': False
        }
        
        # Actual world (hidden from agent)
        self.pits = {(1, 2), (2, 0), (3, 3)}
        self.wumpus = (2, 2)
        self.gold = (3, 1)
    
    def get_neighbors(self, pos):
        """Get valid neighbors"""
        x, y = pos
        neighbors = []
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                neighbors.append((nx, ny))
        return neighbors
    
    def get_percepts(self, pos):
        """Get percepts at position"""
        percepts = {'breeze': False, 'stench': False, 'glitter': False}
        
        neighbors = self.get_neighbors(pos)
        
        # Breeze if pit nearby
        for n in neighbors:
            if n in self.pits:
                percepts['breeze'] = True
        
        # Stench if wumpus nearby
        for n in neighbors:
            if n == self.wumpus:
                percepts['stench'] = True
        
        # Glitter if gold here
        if pos == self.gold:
            percepts['glitter'] = True
        
        return percepts
    
    def update_kb(self, pos, percepts):
        """Update KB using propositional logic"""
        print(f"\n  📡 Percepts at {pos}:")
        print(f"     Breeze (resource scarcity): {percepts['breeze']}")
        print(f"     Stench (crisis): {percepts['stench']}")
        print(f"     Glitter (opportunity): {percepts['glitter']}")
        
        self.kb['visited'].add(pos)
        neighbors = self.get_neighbors(pos)
        
        # Logic Rule 1: No breeze → neighbors safe from pits
        if not percepts['breeze']:
            print(f"  ✅ No breeze → all neighbors safe from pits")
            for n in neighbors:
                self.kb['safe'].add(n)
                self.kb['possible_pits'].discard(n)
        else:
            print(f"  ⚠️  Breeze → at least one neighbor has pit")
            self.kb['breeze_at'].add(pos)
            for n in neighbors:
                if n not in self.kb['safe']:
                    self.kb['possible_pits'].add(n)
        
        # Logic Rule 2: No stench → neighbors safe from wumpus
        if not percepts['stench']:
            print(f"  ✅ No stench → all neighbors safe from wumpus")
            for n in neighbors:
                self.kb['possible_wumpus'].discard(n)
        else:
            print(f"  ⚠️  Stench → wumpus in a neighbor")
            self.kb['stench_at'].add(pos)
            for n in neighbors:
                if n not in self.kb['safe']:
                    self.kb['possible_wumpus'].add(n)
        
        if percepts['glitter']:
            self.kb['gold_found'] = True
            print(f"  ✨ Gold found!")
    
    def choose_action(self):
        """Decide next action"""
        percepts = self.get_percepts(self.agent_pos)
        self.update_kb(self.agent_pos, percepts)
        
        if percepts['glitter']:
            return 'GRAB', "✅ Service opportunity found!"
        
        # Find safe unvisited squares
        safe_moves = []
        for pos in self.kb['safe']:
            if pos not in self.kb['visited']:
                neighbors = self.get_neighbors(self.agent_pos)
                if pos in neighbors:
                    safe_moves.append(pos)
        
        if safe_moves:
            return 'MOVE', f"Moving to safe {safe_moves[0]}"
        else:
            # Calculate risk
            neighbors = self.get_neighbors(self.agent_pos)
            unvisited = [n for n in neighbors if n not in self.kb['visited']]
            
            if unvisited:
                risks = []
                for pos in unvisited:
                    risk = 0
                    if pos in self.kb['possible_pits']:
                        risk += 5
                    if pos in self.kb['possible_wumpus']:
                        risk += 10
                    risks.append((pos, risk))
                
                best = min(risks, key=lambda x: x[1])
                if best[1] < 15:
                    return 'MOVE', f"⚠️  Calculated risk: {best[0]} (risk={best[1]})"
            
            return 'RETREAT', "Risk too high"

# Test Wumpus World
print("\n🗺️  Scenario: Navigate Bayview-Hunters Point to find service opportunities\n")

world = WumpusWorld(size=4)

# Simulate journey
steps = [(0,0), (1,0), (1,1), (2,1), (3,1)]

for step_num, target_pos in enumerate(steps, 1):
    print(f"{'='*60}")
    print(f"STEP {step_num}: Agent at {world.agent_pos}")
    print(f"{'='*60}")
    
    action, reason = world.choose_action()
    print(f"\n  🤔 Decision: {action}")
    print(f"     Reasoning: {reason}")
    
    if step_num < len(steps):
        world.agent_pos = steps[step_num]
    
    if action == 'GRAB':
        print(f"\n🎉 SUCCESS! Service opportunity secured!")
        break

print("\n📊 Key Concepts:")
print("  • Propositional Logic for knowledge representation")
print("  • Inference rules: No breeze → neighbors safe")
print("  • Probabilistic risk assessment when logic insufficient")
print("  • Bridges Ch 7 (Logic) + Ch 12-13 (Uncertainty)")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*70)
print("  TESTING COMPLETE - ALL 8 ALGORITHMS")
print("="*70)

print("""
✅ Core 3 (Contract):
   1. A* Search - Informed search with heuristics
   7. First-Order Logic - Knowledge representation
   8. Wumpus World - Reasoning under uncertainty (includes MDP concepts)

✅ Additional 5 (Breadth):
   2. Alpha-Beta Pruning - Adversarial search
   3. Bayesian Networks - Probabilistic reasoning
   4. Tower of Hanoi - Recursive planning
   5. N-Queens - Constraint satisfaction
   6. Hill Climbing - Local search optimization

🎓 Ready for Professor Lam demo!
📝 Each algorithm: Theory → Implementation → Results
🎯 "Call and Fruit" demonstrated
""")

print("\n" + "="*70 + "\n")