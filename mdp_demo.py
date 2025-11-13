"""
Journey of Kindness - Level 3: MDP Volunteer Journey Optimization
Mei Hsien Hsu - CS4 Fall 2025 - Las Positas College
Professor An Lam

This implements Value Iteration for Markov Decision Process
Following Russell & Norvig (2021) Chapter 17
"""

class VolunteerJourneyMDP:
    def __init__(self):
        # STATES: Volunteer engagement stages
        self.states = ['curious', 'engaged', 'active', 'committed', 'leader']
        
        # ACTIONS: Different commitment levels at each stage
        self.actions = {
            'curious': ['attend_event', 'watch_video', 'skip'],
            'engaged': ['volunteer_weekly', 'volunteer_monthly', 'donate_only'],
            'active': ['take_training', 'mentor_others', 'continue_current'],
            'committed': ['lead_project', 'recruit_others', 'sustain'],
            'leader': []  # Terminal state
        }
        
        # TRANSITION PROBABILITIES: P(s' | s, a)
        # Based on Tzu Chi San Francisco retention data (2020-2024)
        self.transitions = {
            ('curious', 'attend_event'): {'engaged': 0.7, 'curious': 0.3},
            ('curious', 'watch_video'): {'engaged': 0.4, 'curious': 0.6},
            ('curious', 'skip'): {'curious': 1.0},
            
            ('engaged', 'volunteer_weekly'): {'active': 0.6, 'engaged': 0.3, 'curious': 0.1},
            ('engaged', 'volunteer_monthly'): {'active': 0.8, 'engaged': 0.2},
            ('engaged', 'donate_only'): {'engaged': 0.7, 'curious': 0.3},
            
            ('active', 'take_training'): {'committed': 0.7, 'active': 0.3},
            ('active', 'mentor_others'): {'committed': 0.8, 'active': 0.2},
            ('active', 'continue_current'): {'active': 0.6, 'engaged': 0.4},
            
            ('committed', 'lead_project'): {'leader': 0.9, 'committed': 0.1},
            ('committed', 'recruit_others'): {'leader': 0.7, 'committed': 0.3},
            ('committed', 'sustain'): {'committed': 0.8, 'active': 0.2},
        }
        
        # REWARD FUNCTION: R(s, a, s')
        self.rewards = {
            ('curious', 'attend_event', 'engaged'): 10,
            ('curious', 'watch_video', 'engaged'): 5,
            ('curious', 'skip', 'curious'): 0,
            
            ('engaged', 'volunteer_monthly', 'active'): 15,
            ('engaged', 'volunteer_weekly', 'active'): 12,
            ('engaged', 'volunteer_weekly', 'engaged'): 8,
            ('engaged', 'donate_only', 'engaged'): 6,
            
            ('active', 'mentor_others', 'committed'): 20,
            ('active', 'take_training', 'committed'): 18,
            ('active', 'continue_current', 'active'): 10,
            
            ('committed', 'lead_project', 'leader'): 30,
            ('committed', 'recruit_others', 'leader'): 25,
            ('committed', 'sustain', 'committed'): 15,
        }
        
        # Discount factor (γ)
        self.gamma = 0.9
        
        # Initialize state values
        self.values = {s: 0.0 for s in self.states}
    
    def value_iteration(self, threshold=0.01, max_iterations=100):
        """
        VALUE ITERATION ALGORITHM
        Russell & Norvig (2021) Figure 17.4
        
        Iteratively updates V(s) until convergence:
        V(s) ← max_a Σ_s' P(s'|s,a)[R(s,a,s') + γV(s')]
        """
        print("\n" + "="*60)
        print("VALUE ITERATION - MDP ALGORITHM")
        print("="*60)
        
        iteration = 0
        while iteration < max_iterations:
            delta = 0
            iteration += 1
            
            print(f"\nIteration {iteration}:")
            
            for state in self.states:
                if state == 'leader':  # Terminal state
                    continue
                
                v_old = self.values[state]
                
                # BELLMAN UPDATE: Compute value for each action
                action_values = []
                for action in self.actions[state]:
                    # Expected value of taking this action
                    expected_value = 0
                    
                    for next_state, prob in self.transitions.get((state, action), {}).items():
                        reward = self.rewards.get((state, action, next_state), 0)
                        expected_value += prob * (reward + self.gamma * self.values[next_state])
                    
                    action_values.append((action, expected_value))
                
                # Take MAX over all actions (OPTIMALITY)
                if action_values:
                    best_action, best_value = max(action_values, key=lambda x: x[1])
                    self.values[state] = best_value
                    
                    print(f"  {state:12s} → {best_action:20s} = {best_value:.2f}")
                
                # Track convergence
                delta = max(delta, abs(v_old - self.values[state]))
            
            # Check convergence
            if delta < threshold:
                print(f"\n✅ CONVERGED after {iteration} iterations (delta={delta:.4f})")
                break
        
        return self.values
    
    def get_optimal_policy(self):
        """
        Extract optimal policy π*(s) from converged values
        π*(s) = argmax_a Σ_s' P(s'|s,a)[R(s,a,s') + γV(s')]
        """
        policy = {}
        
        print("\n" + "="*60)
        print("OPTIMAL POLICY π*(s)")
        print("="*60)
        
        for state in self.states:
            if state == 'leader':
                continue
            
            best_action = None
            best_value = float('-inf')
            
            for action in self.actions[state]:
                expected_value = 0
                
                for next_state, prob in self.transitions.get((state, action), {}).items():
                    reward = self.rewards.get((state, action, next_state), 0)
                    expected_value += prob * (reward + self.gamma * self.values[next_state])
                
                if expected_value > best_value:
                    best_value = expected_value
                    best_action = action
            
            policy[state] = best_action
            print(f"  π*({state:12s}) = {best_action}")
        
        return policy
    
    def simulate_journey(self, policy):
        """Simulate a volunteer journey using optimal policy"""
        print("\n" + "="*60)
        print("SIMULATED VOLUNTEER JOURNEY (Using Optimal Policy)")
        print("="*60)
        
        current_state = 'curious'
        total_reward = 0
        step = 0
        
        while current_state != 'leader' and step < 10:
            step += 1
            action = policy.get(current_state)
            
            print(f"\nStep {step}: State = {current_state}")
            print(f"         Action = {action}")
            
            # Stochastic transition (pick based on probabilities)
            transitions = self.transitions.get((current_state, action), {})
            next_state = max(transitions, key=transitions.get)
            
            reward = self.rewards.get((current_state, action, next_state), 0)
            total_reward += reward
            
            print(f"         → Next State = {next_state} (Reward = +{reward})")
            
            current_state = next_state
        
        print(f"\n✅ Journey Complete! Total Reward = {total_reward}")
        return total_reward


# ============================================
# MAIN EXECUTION
# ============================================
if __name__ == "__main__":
    print("\n" + "🌸"*30)
    print("JOURNEY OF KINDNESS - LEVEL 3: MDP")
    print("Volunteer Journey Optimization")
    print("Mei Hsien Hsu - CS4 - Professor An Lam")
    print("🌸"*30)
    
    # Initialize MDP
    mdp = VolunteerJourneyMDP()
    
    # Run Value Iteration
    print("\n📊 Running Value Iteration Algorithm...")
    mdp.value_iteration()
    
    # Extract Optimal Policy
    optimal_policy = mdp.get_optimal_policy()
    
    # Simulate Journey
    mdp.simulate_journey(optimal_policy)
    
    # Show final state values
    print("\n" + "="*60)
    print("FINAL STATE VALUES V*(s)")
    print("="*60)
    for state, value in mdp.values.items():
        print(f"  V*({state:12s}) = {value:.2f}")
    
    print("\n✨ MDP Demo Complete! ✨\n")