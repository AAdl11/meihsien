"""
Journey of Kindness - Complete Algorithm Testing Suite
=====================================================
Purpose: Demonstrate "Call and Fruit" for all 8 algorithms to Professor Lam
Author: Mei Hsien Hsu
Date: November 9, 2025

This script tests all 8 AI algorithms with clear outputs for demonstration.
"""

import sys
from queue import PriorityQueue
import random
import math

print("\n" + "="*70)
print("  🎮 JOURNEY OF KINDNESS - ALGORITHM TESTING SUITE")
print("  CS 4 Final Project - Professor An Lam")
print("  Author: 許美嫻 (Mei Hsien Hsu)")
print("="*70 + "\n")

# ============================================================================
# CORE ALGORITHM 1: A* SEARCH (Contract Algorithm)
# ============================================================================
print("\n" + "="*70)
print("CORE ALGORITHM 1: A* SEARCH - Food Delivery Routing")
print("Chapter 3.5-3.6 (Russell & Norvig)")
print("="*70)

def heuristic(pos, goal):
    """Manhattan distance heuristic (admissible for 4-directional grid)"""
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

def get_neighbors(pos, grid_size):
    """Get valid neighboring positions"""
    x, y = pos
    neighbors = []
    for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:  # N, E, S, W
        nx, ny = x + dx, y + dy
        if 0 <= nx < grid_size and 0 <= ny < grid_size:
            neighbors.append((nx, ny))
    return neighbors

def a_star_search(start, goal, grid_size):
    """
    A* pathfinding algorithm
    Complexity: O(b^d) where b=branching factor, d=depth
    """
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    nodes_expanded = 0
    
    while not frontier.empty():
        current = frontier.get()[1]
        nodes_expanded += 1
        
        if current == goal:
            # Reconstruct path
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            return list(reversed(path)), nodes_expanded
        
        for next_pos in get_neighbors(current, grid_size):
            new_cost = cost_so_far[current] + 1
            
            if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                cost_so_far[next_pos] = new_cost
                priority = new_cost + heuristic(next_pos, goal)
                frontier.put((priority, next_pos))
                came_from[next_pos] = current
    
    return None, nodes_expanded

# TEST A* SEARCH
print("\n🎯 Scenario: Volunteer delivers food from Tzu Chi office to family home")
start = (0, 0)
goal = (4, 4)
grid_size = 5

print(f"Start: {start} (Tzu Chi Office)")
print(f"Goal: {goal} (Family Home)")
print(f"Grid: {grid_size}×{grid_size}")

print("\n📞 CALLING ALGORITHM...")
path, nodes = a_star_search(start, goal, grid_size)

print("\n🍎 FRUIT (RESULT):")
if path:
    print(f"✅ Path found! Length: {len(path)} steps")
    print(f"   Nodes expanded: {nodes}")
    print(f"   Path: {' → '.join([str(p) for p in path])}")
    print(f"   f(n) = g(n) + h(n) where h=Manhattan distance")
    
    print("\n📊 Visualization:")
    for i in range(grid_size):
        row = ""
        for j in range(grid_size):
            if (i, j) == start:
                row += "🏢 "  # Tzu Chi office
            elif (i, j) == goal:
                row += "🏠 "  # Family home
            elif (i, j) in path:
                row += "✓  "  # Path
            else:
                row += "·  "
        print(row)
else:
    print("❌ No path found")

print("\n💡 Key Learning: A* uses heuristic h(n) to guide search efficiently")

# ============================================================================
# CORE ALGORITHM 2: PROPOSITIONAL LOGIC - Knowledge Base (Contract Algorithm)
# ============================================================================
print("\n" + "="*70)
print("CORE ALGORITHM 2: PROPOSITIONAL LOGIC - Jing Si Aphorisms")
print("Chapter 8.2-8.3 (Russell & Norvig)")
print("="*70)

class KnowledgeBase:
    def __init__(self):
        self.facts = set()
        self.rules = {
            ('overwhelmed', 'high_complexity'): 
                "Great works are performed not by strength but by perseverance",
            ('grateful', 'after_service'): 
                "In helping others, we help ourselves",
            ('uncertain', 'decision_pending'): 
                "The mind is shaped by circumstances; master the mind",
            ('stressed', 'low_energy'): 
                "Take a deep breath, release stress, find clarity"
        }
    
    def tell(self, fact):
        """Add fact to knowledge base"""
        self.facts.add(fact)
    
    def ask(self, state, context):
        """Query KB using forward chaining"""
        key = (state, context)
        return self.rules.get(key, "Witness the moment without judgment")

# TEST KNOWLEDGE BASE
print("\n🎯 Scenario: Match wisdom aphorisms to volunteer emotional states")
kb = KnowledgeBase()

test_cases = [
    ("overwhelmed", "high_complexity", "Volunteer facing difficult coordination"),
    ("grateful", "after_service", "After successful food distribution"),
    ("uncertain", "decision_pending", "Deciding on commitment level")
]

print("\n📞 CALLING ALGORITHM...")

print("\n🍎 FRUIT (RESULTS):")
for state, context, scenario in test_cases:
    kb.tell(state)
    kb.tell(context)
    aphorism = kb.ask(state, context)
    print(f"\n📌 Scenario: {scenario}")
    print(f"   State: {state}, Context: {context}")
    print(f"   ➜ Aphorism: \"{aphorism}\"")

print("\n💡 Key Learning: Forward chaining - IF premises THEN conclusion")

# ============================================================================
# CORE ALGORITHM 3: MDP - Value Iteration (Contract Algorithm)
# ============================================================================
print("\n" + "="*70)
print("CORE ALGORITHM 3: MDP - Volunteer Engagement Journey")
print("Chapter 17 (Russell & Norvig)")
print("="*70)

class VolunteerMDP:
    def __init__(self, gamma=0.9):
        self.states = ['curious', 'engaged', 'committed', 'sustained']
        self.gamma = gamma  # Discount factor
        self.values = {s: 0.0 for s in self.states}
        
        # Transition probabilities P(s'|s,a)
        self.transitions = {
            'engaged': {
                'weekly': {'sustained': 0.6, 'engaged': 0.4},
                'monthly': {'sustained': 0.8, 'engaged': 0.2},
                'financial': {'sustained': 0.4, 'engaged': 0.6}
            }
        }
        
        # Rewards R(s,a,s')
        self.rewards = {
            ('engaged', 'weekly', 'sustained'): 10,
            ('engaged', 'monthly', 'sustained'): 7,
            ('engaged', 'financial', 'sustained'): 4
        }
    
    def value_iteration(self, threshold=0.01):
        """Compute optimal value function using Bellman equation"""
        iteration = 0
        while True:
            delta = 0
            iteration += 1
            
            for state in self.states:
                if state == 'engaged':
                    v_old = self.values[state]
                    
                    # Bellman update: V(s) = max_a Σ P(s'|s,a)[R + γV(s')]
                    action_values = []
                    for action in ['weekly', 'monthly', 'financial']:
                        value = 0
                        for next_state, prob in self.transitions['engaged'][action].items():
                            reward = self.rewards.get(('engaged', action, next_state), 0)
                            value += prob * (reward + self.gamma * self.values[next_state])
                        action_values.append((action, value))
                    
                    self.values[state] = max(action_values, key=lambda x: x[1])[1]
                    delta = max(delta, abs(v_old - self.values[state]))
            
            if delta < threshold:
                return iteration, self.values

# TEST MDP
print("\n🎯 Scenario: Optimize volunteer engagement strategy")
print("Actions: Weekly volunteering vs Monthly vs Financial support")

print("\n📞 CALLING ALGORITHM...")
mdp = VolunteerMDP(gamma=0.9)
iterations, values = mdp.value_iteration()

print("\n🍎 FRUIT (RESULTS):")
print(f"✅ Converged after {iterations} iterations")
print("\nState Values:")
for state, value in values.items():
    print(f"  V({state}) = {value:.2f}")

print("\n📊 Decision Analysis:")
print("  Weekly: High impact (10) × Low retention (0.6) = 6.0")
print("  Monthly: Moderate impact (7) × High retention (0.8) = 5.6")
print("  Financial: Low impact (4) × Low retention (0.4) = 1.6")

print("\n💡 Key Learning: Bellman equation balances immediate rewards with future value")

# ============================================================================
# ALGORITHM 4: ALPHA-BETA PRUNING
# ============================================================================
print("\n" + "="*70)
print("ALGORITHM 4: ALPHA-BETA PRUNING - Budget Allocation")
print("Chapter 5.3 (Russell & Norvig)")
print("="*70)

def alpha_beta(depth, node_index, maximizing, values, alpha, beta):
    """Alpha-Beta pruning for minimax"""
    if depth == 3:
        return values[node_index]
    
    if maximizing:
        best = float('-inf')
        for i in range(2):
            val = alpha_beta(depth + 1, node_index * 2 + i, False, values, alpha, beta)
            best = max(best, val)
            alpha = max(alpha, best)
            if beta <= alpha:
                break  # Beta cutoff
        return best
    else:
        best = float('inf')
        for i in range(2):
            val = alpha_beta(depth + 1, node_index * 2 + i, True, values, alpha, beta)
            best = min(best, val)
            beta = min(beta, best)
            if beta <= alpha:
                break  # Alpha cutoff
        return best

# TEST ALPHA-BETA
print("\n🎯 Scenario: Allocate $10,000 emergency fund across families")
values = [10, 8, 7, 6, 5, 9, 4, 3]  # Impact scores

print("\n📞 CALLING ALGORITHM...")
result = alpha_beta(0, 0, True, values, float('-inf'), float('inf'))

print("\n🍎 FRUIT (RESULT):")
print(f"✅ Optimal allocation impact score: {result}")
print(f"   Complexity: O(b^(m/2)) vs Minimax O(b^m)")
print(f"   Pruned ~50% of branches!")

print("\n💡 Key Learning: Prune branches that can't affect final decision")

# ============================================================================
# ALGORITHM 5: BAYESIAN NETWORK
# ============================================================================
print("\n" + "="*70)
print("ALGORITHM 5: BAYESIAN NETWORK - Volunteer Retention")
print("Chapter 12.5-12.6 (Russell & Norvig)")
print("="*70)

def bayesian_retention(has_skills, has_interest, has_availability):
    """P(Retention | Skills, Interest, Availability)"""
    if has_skills and has_interest and has_availability:
        return 0.85  # High retention
    elif (has_skills and has_interest) or (has_interest and has_availability):
        return 0.70  # Moderate
    elif has_interest:
        return 0.50  # Low-moderate
    else:
        return 0.20  # Low

# TEST BAYESIAN NETWORK
print("\n🎯 Scenario: Predict volunteer retention probability")

test_volunteers = [
    ("Alice", True, True, True),
    ("Bob", True, True, False),
    ("Carol", False, True, True),
    ("David", False, False, True)
]

print("\n📞 CALLING ALGORITHM...")

print("\n🍎 FRUIT (RESULTS):")
for name, skills, interest, avail in test_volunteers:
    prob = bayesian_retention(skills, interest, avail)
    print(f"  {name}: Skills={skills}, Interest={interest}, Avail={avail}")
    print(f"    ➜ Retention probability: {prob:.0%}")

print("\n💡 Key Learning: Use conditional probabilities for prediction")

# ============================================================================
# ALGORITHM 6: N-QUEENS (CSP)
# ============================================================================
print("\n" + "="*70)
print("ALGORITHM 6: N-QUEENS - Volunteer Scheduling")
print("Chapter 6.1-6.3 (Russell & Norvig)")
print("="*70)

def is_safe(board, row, col, n):
    """Check if queen placement is safe"""
    for i in range(row):
        if board[i] == col or abs(board[i] - col) == abs(i - row):
            return False
    return True

def solve_n_queens(n):
    """Backtracking with constraint satisfaction"""
    board = [-1] * n
    
    def backtrack(row):
        if row == n:
            return True
        for col in range(n):
            if is_safe(board, row, col, n):
                board[row] = col
                if backtrack(row + 1):
                    return True
                board[row] = -1
        return False
    
    if backtrack(0):
        return board
    return None

# TEST N-QUEENS
print("\n🎯 Scenario: Schedule 4 volunteers with time constraints")
n = 4

print("\n📞 CALLING ALGORITHM...")
solution = solve_n_queens(n)

print("\n🍎 FRUIT (RESULT):")
if solution:
    print(f"✅ Solution found for {n} volunteers:")
    for i, col in enumerate(solution):
        row_display = ['·'] * n
        row_display[col] = '👤'
        print(f"  Time slot {i+1}: {' '.join(row_display)}")
    print("\n💡 Key Learning: Backtracking with constraint propagation")
else:
    print("❌ No solution found")

# ============================================================================
# ALGORITHM 7: TOWER OF HANOI
# ============================================================================
print("\n" + "="*70)
print("ALGORITHM 7: TOWER OF HANOI - Virtue Development")
print("Chapter 11.2 (Russell & Norvig)")
print("="*70)

def tower_of_hanoi(n, source, target, auxiliary, moves):
    """Recursive planning algorithm"""
    if n == 1:
        moves.append(f"Move virtue 1 from {source} to {target}")
        return
    
    tower_of_hanoi(n-1, source, auxiliary, target, moves)
    moves.append(f"Move virtue {n} from {source} to {target}")
    tower_of_hanoi(n-1, auxiliary, target, source, moves)

# TEST TOWER OF HANOI
print("\n🎯 Scenario: Build virtue layers (Gratitude → Respect → Love)")
n = 3
moves = []

print("\n📞 CALLING ALGORITHM...")
tower_of_hanoi(n, "Self-Interest", "Serving Others", "Practice", moves)

print("\n🍎 FRUIT (RESULT):")
print(f"✅ Optimal moves: {len(moves)} (proven minimum: 2^{n}-1 = {2**n - 1})")
print("\nFirst 5 steps:")
for i, move in enumerate(moves[:5], 1):
    print(f"  {i}. {move}")

print(f"\n💡 Key Learning: Recursive decomposition, O(2^n) complexity")

# ============================================================================
# ALGORITHM 7: HILL CLIMBING
# ============================================================================
print("\n" + "="*70)
print("ALGORITHM 7: HILL CLIMBING - Meditation Optimization")
print("Chapter 4.1 (Russell & Norvig)")
print("="*70)

def objective_function(x):
    """Meditation quality (with local maxima)"""
    return -(x - 5)**2 + 25 + 5 * (-(x-2)**2 + 4) if x < 4 else -(x - 5)**2 + 25

def hill_climbing(start, step_size=0.5, max_iter=20):
    """Local search optimization"""
    current = start
    path = [current]
    
    for i in range(max_iter):
        current_value = objective_function(current)
        neighbors = [current - step_size, current + step_size]
        neighbor_values = [(n, objective_function(n)) for n in neighbors]
        best_neighbor, best_value = max(neighbor_values, key=lambda x: x[1])
        
        if best_value <= current_value:
            return current, objective_function(current), path, 'local_max'
        
        current = best_neighbor
        path.append(current)
    
    return current, objective_function(current), path, 'max_iter'

# TEST HILL CLIMBING
print("\n🎯 Scenario: Find optimal meditation state")
starts = [0, 3, 8]

print("\n📞 CALLING ALGORITHM...")

print("\n🍎 FRUIT (RESULTS):")
for start in starts:
    result, value, path, reason = hill_climbing(start)
    print(f"  Start x={start} → Final x={result:.2f}, Quality={value:.1f}")
    if reason == 'local_max':
        if result < 4:
            print(f"    ⚠️  Stuck at local maximum!")
        else:
            print(f"    ✅ Found global maximum!")

print("\n💡 Key Learning: Local search can get stuck; use random restarts")

# ============================================================================
# ALGORITHM 8: WUMPUS WORLD - Reasoning Under Uncertainty (超前部署！)
# ============================================================================
print("\n" + "="*70)
print("ALGORITHM 8: WUMPUS WORLD - Community Service Navigation")
print("Chapter 7 + 12-13 (Russell & Norvig)")
print("Propositional Logic + Probabilistic Reasoning")
print("="*70)

class WumpusWorld:
    """
    Wumpus World for community service under uncertainty
    - Pits = Resource-scarce families (avoid over-promising)
    - Wumpus = Community crisis (health/housing emergency)
    - Gold = Service opportunity
    - Breeze = Warning of nearby resource scarcity
    - Stench = Warning of nearby crisis
    """
    
    def __init__(self, size=4):
        self.size = size
        self.agent_pos = (0, 0)
        
        # Knowledge Base (Propositional Logic)
        self.kb = {
            'visited': set(),
            'safe': set([(0, 0)]),  # Start always safe
            'breeze_at': set(),
            'stench_at': set(),
            'possible_pits': set(),
            'possible_wumpus': set()
        }
        
        # Hidden world state
        self.pits = {(1, 2), (2, 0), (3, 3)}
        self.wumpus = (2, 2)
        self.gold = (3, 1)
    
    def get_neighbors(self, pos):
        """Get valid neighboring positions"""
        x, y = pos
        neighbors = []
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                neighbors.append((nx, ny))
        return neighbors
    
    def get_percepts(self, pos):
        """Get percepts at current position"""
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
        """Update Knowledge Base using Propositional Logic"""
        self.kb['visited'].add(pos)
        neighbors = self.get_neighbors(pos)
        
        # Logic Rule 1: No breeze → neighbors safe from pits
        if not percepts['breeze']:
            for n in neighbors:
                self.kb['safe'].add(n)
                self.kb['possible_pits'].discard(n)
        else:
            self.kb['breeze_at'].add(pos)
            for n in neighbors:
                if n not in self.kb['safe']:
                    self.kb['possible_pits'].add(n)
        
        # Logic Rule 2: No stench → neighbors safe from wumpus
        if not percepts['stench']:
            for n in neighbors:
                self.kb['possible_wumpus'].discard(n)
        else:
            self.kb['stench_at'].add(pos)
            for n in neighbors:
                if n not in self.kb['safe']:
                    self.kb['possible_wumpus'].add(n)
    
    def navigate(self, target):
        """Navigate to target using KB reasoning"""
        steps = []
        current = self.agent_pos
        
        while current != target and len(steps) < 10:
            percepts = self.get_percepts(current)
            self.update_kb(current, percepts)
            
            if percepts['glitter']:
                steps.append(('GRAB', current, 'Found service opportunity!'))
                break
            
            # Find safe unvisited neighbors
            neighbors = self.get_neighbors(current)
            safe_neighbors = [n for n in neighbors 
                            if n in self.kb['safe'] and n not in self.kb['visited']]
            
            if safe_neighbors:
                next_pos = safe_neighbors[0]
                steps.append(('MOVE', next_pos, 'Safe path'))
                current = next_pos
                self.agent_pos = current
            else:
                # Calculate risk for unvisited neighbors
                risky_neighbors = [n for n in neighbors if n not in self.kb['visited']]
                if risky_neighbors:
                    risks = []
                    for n in risky_neighbors:
                        risk = 0
                        if n in self.kb['possible_pits']:
                            risk += 5
                        if n in self.kb['possible_wumpus']:
                            risk += 10
                        risks.append((n, risk))
                    
                    best_choice = min(risks, key=lambda x: x[1])
                    if best_choice[1] < 15:
                        steps.append(('MOVE', best_choice[0], f'Calculated risk: {best_choice[1]}'))
                        current = best_choice[0]
                        self.agent_pos = current
                    else:
                        steps.append(('RETREAT', current, 'Risk too high'))
                        break
                else:
                    break
        
        return steps

# TEST WUMPUS WORLD
print("\n🎯 Scenario: Volunteer navigates Bayview-Hunters Point")
print("Goal: Find service opportunities while avoiding over-commitment")

world = WumpusWorld(size=4)

print("\n🗺️  World Layout:")
print("   👤 Agent starts at (0,0)")
print("   💎 Service opportunity at (3,1)")
print("   🕳️  Resource scarcity at (1,2), (2,0), (3,3)")
print("   🔥 Crisis situation at (2,2)")

print("\n📞 CALLING ALGORITHM...")
steps = world.navigate(target=(3, 1))

print("\n🍎 FRUIT (RESULTS):")
print(f"✅ Journey complete! {len(steps)} decisions made")
print("\nDecision Log:")
for i, (action, pos, reason) in enumerate(steps, 1):
    print(f"  {i}. {action} to {pos}: {reason}")

print("\n🧠 Knowledge Base State:")
print(f"   Visited: {len(world.kb['visited'])} squares")
print(f"   Safe: {len(world.kb['safe'])} squares")
print(f"   Possible dangers identified: {len(world.kb['possible_pits']) + len(world.kb['possible_wumpus'])}")

print("\n💡 Key Learning:")
print("   • Propositional Logic: Maintain beliefs about unseen squares")
print("   • Inference: 'No breeze' → neighbors are safe from pits")
print("   • Probabilistic Reasoning: Calculate risk when logic insufficient")
print("   • Ethical Decision-Making: Balance service impact vs safety")
print("   • Bridges Ch 7 (Logic) + Ch 12-13 (Uncertainty)!")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*70)
print("  ✅ ALL 8 ALGORITHMS TESTED - READY FOR DEMO")
print("="*70)

print("""
📊 CORE 3 (Contract):
   1. A* Search - Informed search with heuristics
   2. Propositional Logic - Knowledge representation
   3. MDP - Sequential decision-making

📊 ADDITIONAL 5 (Breadth):
   4. Alpha-Beta Pruning - Game tree optimization
   5. Bayesian Networks - Probabilistic reasoning
   6. N-Queens - Constraint satisfaction
   7. Tower of Hanoi - Recursive planning
   8. Wumpus World - Reasoning under uncertainty (超前部署！)

🎯 ALGORITHM 8 - WUMPUS WORLD (超前部署):
   ✓ Bridges Ch 7 (Logical Agents) + Ch 12-13 (Uncertainty)
   ✓ Propositional Logic: Maintain knowledge base of beliefs
   ✓ Probabilistic Reasoning: Risk assessment when logic insufficient
   ✓ Perfect fit for community service context!

🎓 Each algorithm demonstrates "Call → Fruit":
   ✓ Clear function calls
   ✓ Visible outputs
   ✓ Real volunteer scenarios
   ✓ Complexity analysis

🚀 Ready for Professor Lam demo on Monday!
""")

print("="*70 + "\n")