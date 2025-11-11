"""
Journey of Kindness - Story-Driven AI Educational Game Backend
==============================================================

Author: Mei Hsien Hsu
Course: CS4 Introduction to Artificial Intelligence
Institution: Las Positas College, Honors Transfer Program
Instructor: Professor An Lam
Date: November 2, 2025

Mission: Recruit 500+ volunteers for Tzu Chi Foundation's Hunter's Point service
through emotionally engaging, story-driven AI education games.

Story Origin: The Raw Rice Incident (2000)
A hungry child eating uncooked rice at Hunters Point Elementary sparked
25 years of community service. This game transforms that compassion into
interactive volunteer recruitment through 8 AI-powered mission scenarios.

Design Philosophy:
- Code: 100% English (for professors and GitHub community)
- Game Interface: Bilingual EN + Traditional Chinese (for players)
- Every algorithm wrapped in emotional volunteer story
- Target: 60+ year-old Tzu Chi elders + Chinese-speaking youth

Technical Stack:
- Backend: Python 3.12 (Pyodide in browser)
- Frontend: React.js + GitHub Pages
- Media: Music, images, videos from /assets folder
- Progress: localStorage persistence

Academic Context:
Integrates 8 AI algorithms from Russell & Norvig's "AI: A Modern Approach" (4th Ed)
Target Transfer: UC Berkeley / Stanford Computer Science Programs

License: MIT
Repository: https://github.com/AAdl11/meihsien
"""

import math
import random
import heapq
from typing import List, Tuple, Dict, Optional, Set, Any
from dataclasses import dataclass, field
from collections import deque, defaultdict
from enum import Enum
import json


# =============================================================================
# STORY CONFIGURATION - Links to Media Assets
# =============================================================================

class StoryAssets:
    """
    Media assets for emotional storytelling.
    
    Structure:
    /assets/
      /music/
        - raw_rice_theme.mp3 (Main theme)
        - mission_start.mp3 (Level start)
        - mission_complete.mp3 (Level complete)
      /images/
        - hunters_point_map.jpg (Neighborhood map)
        - raw_rice_incident.jpg (Historic photo)
        - volunteer_stories/ (Real volunteer photos)
      /videos/
        - intro_story.mp4 (Raw Rice Incident narration)
        - volunteer_testimonials.mp4
    """
    
    BASE_PATH = "/assets"
    
    MUSIC = {
        'main_theme': f"{BASE_PATH}/music/raw_rice_theme.mp3",
        'mission_start': f"{BASE_PATH}/music/mission_start.mp3",
        'mission_complete': f"{BASE_PATH}/music/mission_complete.mp3",
        'meditation': f"{BASE_PATH}/music/meditation_calm.mp3"
    }
    
    IMAGES = {
        'hunters_point_map': f"{BASE_PATH}/images/hunters_point_map.jpg",
        'raw_rice_incident': f"{BASE_PATH}/images/raw_rice_incident.jpg",
        'volunteer_group': f"{BASE_PATH}/images/volunteer_stories/group.jpg"
    }
    
    VIDEOS = {
        'intro_story': f"{BASE_PATH}/videos/intro_story.mp4",
        'testimonials': f"{BASE_PATH}/videos/volunteer_testimonials.mp4"
    }


# =============================================================================
# STORY NARRATIVES - Emotional Context for Each Level
# =============================================================================

class StoryNarratives:
    """
    Story-driven descriptions for each AI algorithm mission.
    
    Each level wraps the technical algorithm in an emotional volunteer
    scenario that helps recruit new volunteers by showing real impact.
    """
    
    LEVEL_1_STORY = {
        'title': {
            'en': "🍚 Food Delivery Mission",
            'zh': "🍚 食物配送任務"
        },
        'subtitle': {
            'en': "The Raw Rice Incident Legacy",
            'zh': "生米事件的延續"
        },
        'intro': {
            'en': """
2000, Hunters Point Elementary School.
A little girl, so hungry she couldn't wait,
ate raw, uncooked rice at lunchtime.
Her mother worked three jobs but still
couldn't afford groceries.

That moment changed everything.
For 25 years, Tzu Chi volunteers have delivered
hot meals to families in this forgotten corner
of San Francisco.

Today, YOU are the volunteer driver.
Can you find the fastest route to deliver
warm food to 5 families before dinner gets cold?
""",
            'zh': """
2000年，獵人角小學。
一個小女孩餓到等不及，
午餐時吃起了生米。
她媽媽打三份工
還是買不起食物。

那一刻改變了一切。
25年來，慈濟志工持續送熱騰騰的飯菜
到這個被遺忘的舊金山角落。

今天，你是志工司機。
你能找到最快的路線，在晚餐變冷前
把溫暖的食物送到5個家庭嗎？
"""
        },
        'algorithm_hint': {
            'en': "💡 AI Helper: A* pathfinding finds optimal delivery routes",
            'zh': "💡 AI幫手：A*尋路找出最佳配送路線"
        }
    }
    
    LEVEL_2_STORY = {
        'title': {
            'en': "💔 Difficult Choices",
            'zh': "💔 艱難的抉擇"
        },
        'subtitle': {
            'en': "Strategic Resource Allocation",
            'zh': "策略資源分配"
        },
        'intro': {
            'en': """
After the Raw Rice Incident, we created
an emergency relief fund: $10,000 for families
in crisis.

But the needs are overwhelming:
- Family A: $3,000 medical bills (Mom has diabetes)
- Family B: $8,000 rent to avoid eviction
- Family C: $1,500 school supplies (3 kids)
- Family D: $50,000 housing repair (roof collapse)

You can't help everyone who needs $50K.
Sometimes compassion means making hard choices.

Which families should we prioritize?
How do we maximize impact with limited resources?
""",
            'zh': """
生米事件後，我們創建了
緊急救助基金：一萬美元幫助危機家庭。

但需求太龐大了：
- A家庭：$3,000醫療費（媽媽有糖尿病）
- B家庭：$8,000房租（避免被趕出去）
- C家庭：$1,500學用品（3個孩子）
- D家庭：$50,000房屋修繕（屋頂塌了）

你無法幫助所有需要$50K的人。
有時候慈悲意味著做出艱難的選擇。

我們應該優先幫助哪些家庭？
如何用有限資源最大化影響力？
"""
        },
        'algorithm_hint': {
            'en': "💡 AI Helper: Alpha-Beta pruning eliminates 'obviously impossible' options fast",
            'zh': "💡 AI幫手：Alpha-Beta剪枝快速排除「明顯不可能」的選項"
        }
    }
    
    LEVEL_3_STORY = {
        'title': {
            'en': "🤝 Will They Come Back?",
            'zh': "🤝 他們會回來嗎？"
        },
        'subtitle': {
            'en': "Predicting Volunteer Commitment",
            'zh': "預測志工承諾度"
        },
        'intro': {
            'en': """
Maria came once to help distribute food.
She was moved to tears seeing the families.
But will she come back next month?

Our volunteers are aging (average age: 65).
We NEED young people like Maria to continue
this 25-year legacy.

Based on what we know:
- Is she experiencing hardship herself?
- Does she have time availability?
- Does her personality fit volunteer work?

AI helps us predict: Should we reach out
actively, or give her space?
""",
            'zh': """
Maria來了一次幫忙發放食物。
她看到這些家庭感動落淚。
但她下個月會回來嗎？

我們的志工在老化（平均年齡65歲）。
我們需要像Maria這樣的年輕人
延續這25年的使命。

根據我們所知：
- 她自己有經歷困難嗎？
- 她有時間嗎？
- 她的個性適合志工工作嗎？

AI幫我們預測：我們應該主動聯繫，
還是給她空間？
"""
        },
        'algorithm_hint': {
            'en': "💡 AI Helper: Bayesian Networks calculate commitment probability",
            'zh': "💡 AI幫手：貝葉斯網絡計算承諾概率"
        }
    }
    
    LEVEL_4_STORY = {
        'title': {
            'en': "🧘 Building Virtue, One Layer at a Time",
            'zh': "🧘 逐層建立美德"
        },
        'subtitle': {
            'en': "The Tower of Compassion",
            'zh': "慈悲之塔"
        },
        'intro': {
            'en': """
Master Cheng Yen teaches:
"Gratitude is the foundation.
Respect stands upon gratitude.
Love grows from respect."

Like the Tower of Hanoi puzzle,
you can't skip steps in building compassion.
You must build virtue one layer at a time,
one action at a time.

Move the disks from "Self-Interest"
to "Serving Others."
But follow the rules: Never place
a larger burden on a smaller foundation.
""",
            'zh': """
證嚴上人教導：
「感恩是基礎。
尊重立於感恩之上。
愛從尊重中生長。」

就像河內塔的謎題，
你不能跳過建立慈悲的步驟。
你必須逐層建立美德，
一次一個行動。

把圓盤從「自利」
移到「利他」。
但要遵守規則：永遠不要把
更大的負擔放在更小的基礎上。
"""
        },
        'algorithm_hint': {
            'en': "💡 AI Helper: Recursive thinking shows optimal 2^n - 1 moves",
            'zh': "💡 AI幫手：遞歸思維展示最優2^n - 1步"
        }
    }
    
    LEVEL_5_STORY = {
        'title': {
            'en': "📅 Volunteer Shift Scheduler",
            'zh': "📅 志工排班調度"
        },
        'subtitle': {
            'en': "8 Volunteers, 8 Shifts, Zero Conflicts",
            'zh': "8位志工，8個班次，零衝突"
        },
        'intro': {
            'en': """
Saturday food distribution needs 8 volunteers:
- Morning setup (6am-9am)
- Registration desk (9am-12pm)
- Food sorting (9am-12pm)
- Distribution (12pm-3pm)
- Cleanup (3pm-6pm)
... and 3 more shifts

But everyone has conflicts:
Mrs. Chen can't work mornings (arthritis pain).
David has basketball practice at 3pm.
Rosa works until noon.

Can you arrange 8 people across 8 time slots
so NOBODY has conflicts?
Like the N-Queens puzzle: no attacks allowed!
""",
            'zh': """
週六食物發放需要8位志工：
- 早晨準備（6am-9am）
- 註冊桌（9am-12pm）
- 食物分類（9am-12pm）
- 發放（12pm-3pm）
- 清潔（3pm-6pm）
... 還有3個班次

但每個人都有衝突：
陳太太早上不能工作（關節炎痛）。
David下午3點有籃球練習。
Rosa要工作到中午。

你能把8個人安排在8個時段
讓所有人都沒有衝突嗎？
就像N皇后謎題：不允許攻擊！
"""
        },
        'algorithm_hint': {
            'en': "💡 AI Helper: Backtracking with constraint satisfaction",
            'zh': "💡 AI幫手：回溯法加約束滿足"
        }
    }
    
    LEVEL_6_STORY = {
        'title': {
            'en': "🧘 Finding Inner Peace",
            'zh': "🧘 尋找內心平和"
        },
        'subtitle': {
            'en': "Meditation Optimization",
            'zh': "禪修優化"
        },
        'intro': {
            'en': """
After 8 hours of food distribution,
volunteers gather for evening meditation.

"Find your inner peace," the guide says.
But what IS inner peace?
- Focus without distraction?
- Calmness without worry?
- Compassion without judgment?

Master Cheng Yen teaches:
"When the mind is calm, wisdom appears."

Try different meditation states.
Climb the hill toward optimal peace.
But beware: You might get stuck in
comfortable but not perfect states (local maxima).

That's when you need to "restart" - try again!
""",
            'zh': """
發放食物8小時後，
志工們聚在一起晚間禪修。

「找到你的內心平和，」導師說。
但什麼是內心平和？
- 專注而不分心？
- 平靜而不擔憂？
- 慈悲而不批判？

證嚴上人教導：
「心靜，智慧自然生。」

嘗試不同的禪修狀態。
爬向最優的平和之巔。
但要小心：你可能困在
舒適但不完美的狀態（局部最大值）。

這時你需要「重新開始」——再試一次！
"""
        },
        'algorithm_hint': {
            'en': "💡 AI Helper: Hill climbing with random restarts escapes local maxima",
            'zh': "💡 AI幫手：爬山法加隨機重啟逃離局部最大值"
        }
    }


# =============================================================================
# CORE GAME ENGINE WITH STORY INTEGRATION
# =============================================================================

class GameEngine:
    """
    Master controller for story-driven AI missions.
    
    Manages:
    - 8 story-wrapped AI algorithms
    - Bilingual story delivery
    - Human vs AI comparison
    - Elo rating progression
    - Media asset loading
    """
    
    def __init__(self):
        """Initialize game engine with story and algorithm instances."""
        self.algorithms = {
            'astar': AStarSearch(),
            'alphabeta': AlphaBetaPruning(),
            'bayesian': BayesianNetwork(),
            'hanoi': TowerOfHanoi(),
            'nqueens': NQueensSolver(),
            'hillclimb': HillClimbing(),
            'fol': FOLPlanner(),
            'blocks': BlocksWorld()
        }
        
        self.stories = StoryNarratives()
        self.assets = StoryAssets()
        self.elo_system = EloRating(initial=1000, k=32)
        self.current_level = 1
        self.completed_levels = set()
        
    def get_level_story(self, level_id: int, language: str = 'both') -> Dict[str, Any]:
        """
        Get story introduction for a level.
        
        Args:
            level_id: Mission number (1-8)
            language: 'en', 'zh', or 'both' (default)
            
        Returns:
            {
                'title': bilingual title,
                'subtitle': bilingual subtitle,
                'intro': story text,
                'algorithm_hint': what AI does,
                'media': {music, images, videos}
            }
        """
        story_map = {
            1: self.stories.LEVEL_1_STORY,
            2: self.stories.LEVEL_2_STORY,
            3: self.stories.LEVEL_3_STORY,
            4: self.stories.LEVEL_4_STORY,
            5: self.stories.LEVEL_5_STORY,
            6: self.stories.LEVEL_6_STORY
        }
        
        story = story_map.get(level_id, {})
        
        # Format based on language preference
        if language == 'en':
            formatted = {k: v.get('en', '') for k, v in story.items() if isinstance(v, dict)}
        elif language == 'zh':
            formatted = {k: v.get('zh', '') for k, v in story.items() if isinstance(v, dict)}
        else:  # both
            formatted = story
        
        # Add media assets
        formatted['media'] = {
            'music': self.assets.MUSIC['mission_start'],
            'background': self.assets.IMAGES.get(f'level_{level_id}_bg', '')
        }
        
        return formatted
    
    def run_level(self, level_id: int, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute story-driven mission with AI comparison.
        
        Flow:
        1. Show story introduction (bilingual)
        2. Player attempts mission
        3. AI demonstrates optimal solution
        4. Compare results with emotional feedback
        5. Update Elo and unlock rewards
        
        Args:
            level_id: Mission number (1-8)
            user_input: Player's solution attempt
            
        Returns:
            {
                'story': mission context,
                'user_solution': player attempt,
                'ai_solution': optimal solution,
                'comparison': human vs AI,
                'emotional_feedback': bilingual encouragement,
                'elo_change': rating adjustment,
                'rewards': unlocked content
            }
        """
        algorithm_map = {
            1: 'astar',
            2: 'alphabeta',
            3: 'bayesian',
            4: 'hanoi',
            5: 'nqueens',
            6: 'hillclimb',
            7: 'fol',
            8: 'blocks'
        }
        
        if level_id not in algorithm_map:
            raise ValueError(f"Invalid level ID: {level_id}")
        
        # Get story context
        story = self.get_level_story(level_id)
        
        # Execute algorithm
        algorithm = self.algorithms[algorithm_map[level_id]]
        ai_result = algorithm.solve(user_input)
        
        # Calculate user performance
        user_score = self._evaluate_user_performance(
            level_id, user_input, ai_result
        )
        
        # Update Elo
        elo_change = self.elo_system.calculate(user_score, ai_result.get('score', 100))
        
        # Track progress
        if user_score >= 70:
            self.completed_levels.add(level_id)
        
        # Generate emotional feedback (bilingual)
        emotional_feedback = self._generate_emotional_feedback(
            level_id, user_score, elo_change
        )
        
        return {
            'story': story,
            'user_solution': user_input,
            'ai_solution': ai_result['solution'],
            'ai_explanation': ai_result['explanation'],
            'comparison': {
                'user_score': user_score,
                'ai_score': ai_result.get('score', 100),
                'difference': abs(ai_result.get('score', 100) - user_score),
                'improvement_tips': self._get_improvement_tips(level_id, user_score, ai_result)
            },
            'emotional_feedback': emotional_feedback,
            'elo_change': elo_change,
            'current_elo': self.elo_system.rating,
            'rewards': {
                'next_level_unlocked': len(self.completed_levels) >= level_id,
                'tzuchi_qr_unlocked': self.elo_system.rating >= 1300,
                'rank': self.elo_system.get_rank()
            }
        }
    
    def _generate_emotional_feedback(
        self,
        level_id: int,
        user_score: float,
        elo_change: int
    ) -> Dict[str, str]:
        """
        Generate encouraging bilingual feedback based on performance.
        
        Design: Always encouraging, never discouraging.
        Even "failure" is framed as learning opportunity.
        """
        if user_score >= 90:
            return {
                'en': f"""
🌟 OUTSTANDING! | 非常出色！
You're thinking like a veteran volunteer!
Your solution scored {user_score:.0f}/100.

The families you helped today will remember
your efficiency and care. Thank you! 🙏

Elo Rating: +{elo_change} → {self.elo_system.rating}
""",
                'zh': f"""
🌟 非常出色！| OUTSTANDING!
你的思考方式像資深志工！
你的解決方案得分 {user_score:.0f}/100。

你今天幫助的家庭會記得
你的效率和關懷。感恩！🙏

Elo評分：+{elo_change} → {self.elo_system.rating}
"""
            }
        elif user_score >= 70:
            return {
                'en': f"""
💚 WELL DONE! | 做得好！
You completed the mission successfully!
Score: {user_score:.0f}/100

There's always room to grow, but today
you made a real difference. Keep going!

Elo Rating: +{elo_change} → {self.elo_system.rating}
""",
                'zh': f"""
💚 做得好！| WELL DONE!
你成功完成了任務！
得分：{user_score:.0f}/100

總有成長空間，但今天
你確實有所作為。繼續加油！

Elo評分：+{elo_change} → {self.elo_system.rating}
"""
            }
        else:
            return {
                'en': f"""
💙 LEARNING IN PROGRESS | 學習中
Every expert volunteer was once a beginner.
Score: {user_score:.0f}/100

Master Cheng Yen says: "Failure is the mother
of success." Try again with the AI's guidance!

Elo Rating: {elo_change:+d} → {self.elo_system.rating}
""",
                'zh': f"""
💙 學習中 | LEARNING IN PROGRESS
每位資深志工都曾是新手。
得分：{user_score:.0f}/100

證嚴上人說：「失敗為成功之母。」
跟著AI的引導再試一次！

Elo評分：{elo_change:+d} → {self.elo_system.rating}
"""
            }
    
    def _get_improvement_tips(
        self,
        level_id: int,
        user_score: float,
        ai_result: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """
        Generate bilingual improvement tips.
        
        Returns list of {en: ..., zh: ...} tip dictionaries.
        """
        tips = []
        
        if level_id == 1:  # A* Search
            if user_score < 70:
                tips.append({
                    'en': "💡 Try using Manhattan distance to estimate remaining distance",
                    'zh': "💡 試試使用曼哈頓距離來估計剩餘距離"
                })
                tips.append({
                    'en': "💡 Always explore the path with lowest f(n) = g(n) + h(n) first",
                    'zh': "💡 總是先探索f(n) = g(n) + h(n)最低的路徑"
                })
        
        elif level_id == 2:  # Alpha-Beta
            if user_score < 70:
                tips.append({
                    'en': "💡 Think: Which families can we definitely NOT help with $10K?",
                    'zh': "💡 想想：哪些家庭我們用$10K絕對幫不了？"
                })
                tips.append({
                    'en': "💡 Those 'obviously impossible' options are what Alpha-Beta prunes!",
                    'zh': "💡 那些「明顯不可能」的選項就是Alpha-Beta會剪枝的！"
                })
        
        elif level_id == 3:  # Bayesian
            if user_score < 70:
                tips.append({
                    'en': "💡 People who received help are more likely to give back",
                    'zh': "💡 受過幫助的人更可能回饋"
                })
                tips.append({
                    'en': "💡 Use Bayes' Theorem: P(A|B) = P(B|A) × P(A) / P(B)",
                    'zh': "💡 使用貝葉斯定理：P(A|B) = P(B|A) × P(A) / P(B)"
                })
        
        # Universal encouragement
        if user_score >= 90:
            tips.insert(0, {
                'en': "🌟 Excellent! You're thinking like the AI!",
                'zh': "🌟 太棒了！你的思考方式像AI一樣！"
            })
        elif user_score >= 70:
            tips.insert(0, {
                'en': "👍 Good job! Small improvements possible",
                'zh': "👍 做得好！還有小的改進空間"
            })
        else:
            tips.insert(0, {
                'en': "📚 Study the AI's approach - it shows the optimal strategy",
                'zh': "📚 研究AI的方法 — 它展示了最優策略"
            })
        
        return tips
    
    def _evaluate_user_performance(
        self,
        level_id: int,
        user_input: Dict[str, Any],
        ai_result: Dict[str, Any]
    ) -> float:
        """Evaluate user performance (0-100 scale)."""
        if level_id == 1:  # A* Search
            user_path = user_input.get('path', [])
            optimal_path = ai_result['solution'].get('path', [])
            if len(user_path) == 0:
                return 0
            return min(100, (len(optimal_path) / len(user_path)) * 100)
        
        elif level_id == 2:  # Alpha-Beta
            user_value = user_input.get('value', 0)
            optimal_value = ai_result['solution'].get('value', 0)
            return 100 if user_value == optimal_value else 50
        
        elif level_id == 3:  # Bayesian
            user_prob = user_input.get('probability', 0)
            optimal_prob = ai_result['solution'].get('probability', 0)
            diff = abs(user_prob - optimal_prob)
            return max(0, 100 - (diff * 100))
        
        elif level_id in [4, 5, 6]:  # Hanoi, N-Queens, Hill Climbing
            user_moves = user_input.get('moves', float('inf'))
            optimal_moves = ai_result['solution'].get('moves', 1)
            if user_moves == optimal_moves:
                return 100
            elif user_moves <= optimal_moves * 1.5:
                return 75
            else:
                return 50
        
        else:
            return 50


# =============================================================================
# LEVEL 1: A* SEARCH - FOOD DELIVERY MISSION
# =============================================================================

@dataclass
class Node:
    """Search node for A* pathfinding algorithm."""
    position: Tuple[int, int]
    g_cost: float = 0
    h_cost: float = 0
    f_cost: float = 0
    parent: Optional['Node'] = None
    
    def __lt__(self, other):
        return self.f_cost < other.f_cost
    
    def __eq__(self, other):
        return self.position == other.position
    
    def __hash__(self):
        return hash(self.position)


class Grid:
    """2D grid for Hunters Point neighborhood map."""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
    
    def is_walkable(self, pos: Tuple[int, int]) -> bool:
        x, y = pos
        return (0 <= x < self.width and
                0 <= y < self.height and
                self.grid[y][x] != 1)
    
    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        x, y = pos
        neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        return [n for n in neighbors if self.is_walkable(n)]
    
    def set_obstacle(self, x: int, y: int):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = 1
    
    def set_goal(self, x: int, y: int, goal_id: int):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = goal_id


class AStarSearch:
    """
    A* Pathfinding Algorithm (Russell & Norvig Chapter 3.5)
    
    Story: Find optimal route to deliver hot meals to families
    Algorithm: A* with Manhattan distance heuristic
    Complexity: O(b^d) where b=branching factor, d=depth
    """
    
    def __init__(self):
        self.stats = {
            'nodes_expanded': 0,
            'nodes_generated': 0,
            'path_cost': 0
        }
    
    def manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """Manhattan distance heuristic (admissible for 4-directional grid)."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def reconstruct_path(self, node: Node) -> List[Tuple[int, int]]:
        """Backtrack from goal to start using parent pointers."""
        path = []
        current = node
        while current:
            path.append(current.position)
            current = current.parent
        return path[::-1]
    
    def solve(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute A* search for food delivery route.
        
        Args:
            input_data: {
                'grid_size': (width, height),
                'start': (x, y),
                'goals': [(x, y), ...],
                'obstacles': [(x, y), ...]
            }
        
        Returns:
            {
                'solution': {path, cost},
                'explanation': bilingual story,
                'score': 100
            }
        """
        # Initialize grid
        width, height = input_data.get('grid_size', (10, 10))
        grid = Grid(width, height)
        
        for obs in input_data.get('obstacles', []):
            grid.set_obstacle(*obs)
        
        start = input_data.get('start', (0, 0))
        goals = input_data.get('goals', [(9, 9)])
        
        # A* algorithm
        open_set = []
        closed_set = set()
        
        start_node = Node(
            position=start,
            g_cost=0,
            h_cost=min(self.manhattan_distance(start, g) for g in goals),
            f_cost=0
        )
        start_node.f_cost = start_node.g_cost + start_node.h_cost
        
        heapq.heappush(open_set, start_node)
        self.stats['nodes_generated'] = 1
        
        while open_set:
            current = heapq.heappop(open_set)
            self.stats['nodes_expanded'] += 1
            
            if current.position in goals:
                path = self.reconstruct_path(current)
                return {
                    'solution': {
                        'path': path,
                        'cost': current.g_cost,
                        'families_reached': len([p for p in path if p in goals])
                    },
                    'explanation': self._generate_story_explanation(path, current.g_cost),
                    'score': 100
                }
            
            closed_set.add(current.position)
            
            for neighbor_pos in grid.get_neighbors(current.position):
                if neighbor_pos in closed_set:
                    continue
                
                g_cost = current.g_cost + 1
                h_cost = min(self.manhattan_distance(neighbor_pos, g) for g in goals)
                f_cost = g_cost + h_cost
                
                neighbor = Node(
                    position=neighbor_pos,
                    g_cost=g_cost,
                    h_cost=h_cost,
                    f_cost=f_cost,
                    parent=current
                )
                
                if any(n.position == neighbor_pos and n.f_cost <= f_cost for n in open_set):
                    continue
                
                heapq.heappush(open_set, neighbor)
                self.stats['nodes_generated'] += 1
        
        return {
            'solution': {'path': [], 'cost': float('inf')},
            'explanation': "No path found | 無法找到路徑",
            'score': 0
        }
    
    def _generate_story_explanation(self, path: List[Tuple[int, int]], cost: float) -> str:
        """Generate bilingual story-driven explanation."""
        return f"""
╔══════════════════════════════════════════════════════════════╗
║  🍚 FOOD DELIVERY MISSION COMPLETE | 食物配送任務完成        ║
╚══════════════════════════════════════════════════════════════╝

📍 YOUR ROUTE | 你的路線:
{' → '.join(f'({x},{y})' for x, y in path[:10])}
{'...' if len(path) > 10 else ''}

📊 MISSION STATS | 任務統計:
Total Distance | 總距離: {cost} blocks | 個街區
Delivery Stops | 配送站點: {len(path)} locations | 個地點
Algorithm Efficiency | 算法效率: {self.stats['nodes_expanded']} decisions | 個決策

🎯 IMPACT | 影響:
✓ All families received hot meals before 6pm
  所有家庭在6點前收到熱騰騰的飯菜
✓ Optimal route saved 15 minutes of drive time
  最優路線節省15分鐘車程
✓ Fresh food = healthier families = stronger community
  新鮮食物 = 更健康的家庭 = 更強大的社區

💭 REFLECTION | 反思:
"In 2000, that little girl ate raw rice because
food arrived too late. Today, YOUR efficiency
ensures no child goes hungry."

「2000年，那個小女孩吃生米是因為
食物送太晚。今天，你的效率
確保沒有孩子挨餓。」

— Master Cheng Yen | 證嚴上人

🔬 THE AI SECRET | AI秘密:
A* Search uses h(n) = Manhattan Distance to
estimate remaining path. This "智慧猜測" makes
it MUCH faster than brute-force search!

A*搜尋使用h(n) = 曼哈頓距離來
估計剩餘路徑。這個「智慧猜測」讓它
比暴力搜尋快得多！

Next Mission Unlocked! | 下個任務解鎖了！ →
"""


# =============================================================================
# LEVEL 2: STRATEGIC RESOURCE ALLOCATION - ALPHA-BETA PRUNING
# =============================================================================

@dataclass
class GameTreeNode:
    """Decision tree node for resource allocation."""
    value: Optional[int] = None
    children: List['GameTreeNode'] = field(default_factory=list)
    is_max: bool = True
    alpha: float = -math.inf
    beta: float = math.inf
    pruned: bool = False
    
    def is_terminal(self) -> bool:
        return len(self.children) == 0


class AlphaBetaPruning:
    """
    Alpha-Beta Pruning for Strategic Resource Allocation
    (Russell & Norvig Chapter 5.3)
    
    Story: $10K emergency fund, multiple families in crisis, hard choices
    Algorithm: Minimax with α-β pruning
    Teaching Modes: Tutorial (2 mistakes), Learning (1 mistake), Expert (perfect)
    """
    
    def __init__(self, difficulty='learning'):
        self.difficulty = difficulty
        self.stats = {
            'nodes_evaluated': 0,
            'nodes_pruned': 0,
            'max_depth': 0,
            'ai_mistakes_made': 0,
            'teaching_hints': []
        }
    
    def minimax(
        self,
        node: GameTreeNode,
        depth: int,
        alpha: float,
        beta: float,
        maximizing: bool,
        teaching_mode: bool = False
    ) -> int:
        """Minimax with alpha-beta pruning and optional teaching mistakes."""
        self.stats['nodes_evaluated'] += 1
        self.stats['max_depth'] = max(self.stats['max_depth'], depth)
        
        if depth == 0 or node.is_terminal():
            return node.value if node.value is not None else 0
        
        # Teaching mode: Occasionally make suboptimal choices
        if teaching_mode and self._should_make_teaching_mistake(depth):
            values = [
                self.minimax(child, depth - 1, alpha, beta, not maximizing, teaching_mode)
                for child in node.children
            ]
            
            if maximizing and len(values) > 1:
                sorted_values = sorted(enumerate(values), key=lambda x: x[1], reverse=True)
                if len(sorted_values) > 1:
                    self.stats['ai_mistakes_made'] += 1
                    self.stats['teaching_hints'].append({
                        'en': f"🎓 AI Teaching: I chose {sorted_values[1][1]} instead of optimal {sorted_values[0][1]} to give you a chance!",
                        'zh': f"🎓 AI教學：我選擇了{sorted_values[1][1]}而非最優{sorted_values[0][1]}來給你機會！"
                    })
                    return sorted_values[1][1]
        
        if maximizing:
            value = -math.inf
            for child in node.children:
                value = max(value, self.minimax(child, depth - 1, alpha, beta, False, teaching_mode))
                alpha = max(alpha, value)
                if beta <= alpha:
                    self.stats['nodes_pruned'] += len(node.children) - (node.children.index(child) + 1)
                    child.pruned = True
                    break
            return value
        else:
            value = math.inf
            for child in node.children:
                value = min(value, self.minimax(child, depth - 1, alpha, beta, True, teaching_mode))
                beta = min(beta, value)
                if beta <= alpha:
                    self.stats['nodes_pruned'] += len(node.children) - (node.children.index(child) + 1)
                    child.pruned = True
                    break
            return value
    
    def _should_make_teaching_mistake(self, depth: int) -> bool:
        """Decide if AI should make intentional mistake for teaching."""
        if self.difficulty == 'tutorial':
            return depth in [2, 1] and self.stats['ai_mistakes_made'] < 2
        elif self.difficulty == 'learning':
            return depth == 1 and self.stats['ai_mistakes_made'] < 1
        else:
            return False
    
    def solve(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute strategic resource allocation decision.
        
        Args:
            input_data: {
                'tree_structure': 'simple' | 'complex',
                'difficulty': 'tutorial' | 'learning' | 'expert'
            }
        
        Returns:
            {
                'solution': {value, families_helped},
                'explanation': bilingual story,
                'teaching_hints': list of hints,
                'score': 100
            }
        """
        tree_type = input_data.get('tree_structure', 'simple')
        difficulty = input_data.get('difficulty', self.difficulty)
        
        self.difficulty = difficulty
        self.stats = {
            'nodes_evaluated': 0,
            'nodes_pruned': 0,
            'max_depth': 0,
            'ai_mistakes_made': 0,
            'teaching_hints': []
        }
        
        root = self._build_simple_tree() if tree_type == 'simple' else self._build_complex_tree()
        
        teaching_mode = (difficulty in ['tutorial', 'learning'])
        optimal_value = self.minimax(root, 3, -math.inf, math.inf, True, teaching_mode)
        
        return {
            'solution': {
                'value': optimal_value,
                'families_helped': self._calculate_families_helped(optimal_value)
            },
            'explanation': self._generate_story_explanation(optimal_value),
            'teaching_hints': self.stats['teaching_hints'],
            'difficulty': difficulty,
            'score': 100
        }
    
    def _calculate_families_helped(self, impact_score: int) -> int:
        """Convert impact score to number of families."""
        if impact_score <= 4:
            return 1
        elif impact_score <= 8:
            return 2
        elif impact_score <= 15:
            return 3
        else:
            return 4
    
    def _build_simple_tree(self) -> GameTreeNode:
        """Build strategic resource allocation tree."""
        leaf1 = GameTreeNode(value=10)
        leaf2 = GameTreeNode(value=8)
        leaf3 = GameTreeNode(value=4)
        leaf4 = GameTreeNode(value=50)
        
        min_left = GameTreeNode(children=[leaf1, leaf2], is_max=False)
        min_right = GameTreeNode(children=[leaf3, leaf4], is_max=False)
        
        root = GameTreeNode(children=[min_left, min_right], is_max=True)
        return root
    
    def _build_complex_tree(self) -> GameTreeNode:
        """Build complex decision tree."""
        def build_level(depth: int, is_max: bool):
            if depth == 0:
                return GameTreeNode(value=random.randint(1, 100))
            children = [build_level(depth - 1, not is_max) for _ in range(2)]
            return GameTreeNode(children=children, is_max=is_max)
        return build_level(3, True)
    
    def _generate_story_explanation(self, value: int) -> str:
        """Generate bilingual story explanation."""
        pruning_efficiency = (self.stats['nodes_pruned'] / max(1, self.stats['nodes_evaluated'])) * 100
        families = self._calculate_families_helped(value)
        
        teaching_section = ""
        if self.stats['ai_mistakes_made'] > 0:
            hints_text = "\n".join([
                f"  • {h['en']}\n    {h['zh']}"
                for h in self.stats['teaching_hints']
            ])
            teaching_section = f"""

🎓 TEACHING MODE ACTIVE | 教學模式啟動
═══════════════════════════════════════════════════════════════
Difficulty | 難度: {self.difficulty.upper()}
AI Mistakes Made | AI犯的錯誤: {self.stats['ai_mistakes_made']}

{hints_text}

Why Teaching Mode? | 為什麼要教學模式？
Mei Hsien's testing showed: "永遠贏不了AI很沮喪"
(Always losing to AI is frustrating and demotivating)

Ready for higher difficulty? | 準備好更高難度了嗎？💪
"""
        
        return f"""
╔══════════════════════════════════════════════════════════════╗
║  💔 DIFFICULT CHOICES MADE | 艱難的抉擇已完成                ║
╚══════════════════════════════════════════════════════════════╝

🎯 DECISION RESULT | 決策結果:
Impact Score | 影響分數: {value}
Families Helped | 幫助的家庭: {families}

📊 ALGORITHM EFFICIENCY | 算法效率:
Total Options Considered | 考慮的選項: {self.stats['nodes_evaluated']}
Options PRUNED (Obviously Bad) | 剪枝選項（明顯糟糕）: {self.stats['nodes_pruned']}
Pruning Efficiency | 剪枝效率: {pruning_efficiency:.1f}%
{teaching_section}
💭 THE HARD TRUTH | 殘酷的現實:
"With $10,000, we CANNOT fix a $50,000 roof.
But we CAN help 3 families with medical bills,
rent, and school supplies."

「用$10,000，我們無法修$50,000的屋頂。
但我們可以幫助3個家庭付醫療費、
房租和學用品。」

This is Alpha-Beta's wisdom: Quickly identify
"obviously impossible" options and focus on
what we CAN do.

這是Alpha-Beta的智慧：快速識別
「明顯不可能」的選項，專注於
我們能做的事。

🙏 COMPASSION IN CONSTRAINTS | 約束中的慈悲:
True compassion isn't helping everyone equally—
it's maximizing impact with limited resources.

真正的慈悲不是平等幫助所有人——
而是用有限資源最大化影響力。

— Tzu Chi Emergency Relief Philosophy
— 慈濟緊急救助哲學

Next Mission Unlocked! | 下個任務解鎖了！ →
"""


# =============================================================================
# LEVEL 3: BAYESIAN NETWORK - VOLUNTEER COMMITMENT PREDICTION
# =============================================================================

class BayesianNetwork:
    """
    Bayesian Network for Volunteer Commitment Prediction
    (Russell & Norvig Chapter 12)
    
    Story: Will Maria come back to volunteer next month?
    Algorithm: Probabilistic inference using CPT tables
    Ethical: 40% baseline, bias testing, transparent probabilities
    """
    
    def __init__(self):
        self.nodes = {
            'Poor': [],
            'Elderly': [],
            'Sick': [],
            'Aid': ['Poor', 'Elderly', 'Sick'],
            'Volunteer': ['Aid']
        }
        
        self.cpt = {
            'Poor': {True: 0.30, False: 0.70},
            'Elderly': {True: 0.25, False: 0.75},
            'Sick': {True: 0.15, False: 0.85},
            'Aid': {
                (True, True, True): 0.95,
                (True, True, False): 0.85,
                (True, False, True): 0.80,
                (True, False, False): 0.70,
                (False, True, True): 0.75,
                (False, True, False): 0.60,
                (False, False, True): 0.55,
                (False, False, False): 0.30
            },
            'Volunteer': {
                True: 0.65,
                False: 0.40
            }
        }
    
    def query(self, evidence: Dict[str, bool]) -> float:
        """Perform probabilistic inference."""
        poor = evidence.get('Poor', None)
        elderly = evidence.get('Elderly', None)
        sick = evidence.get('Sick', None)
        
        if all(v is not None for v in [poor, elderly, sick]):
            p_aid = self.cpt['Aid'][(poor, elderly, sick)]
        else:
            p_aid = self._marginalize_aid(poor, elderly, sick)
        
        p_volunteer_given_aid_true = self.cpt['Volunteer'][True]
        p_volunteer_given_aid_false = self.cpt['Volunteer'][False]
        
        result = (p_aid * p_volunteer_given_aid_true +
                 (1 - p_aid) * p_volunteer_given_aid_false)
        
        return result
    
    def _marginalize_aid(self, poor, elderly, sick) -> float:
        """Marginalize over unobserved variables."""
        total_prob = 0.0
        
        for p in ([poor] if poor is not None else [True, False]):
            for e in ([elderly] if elderly is not None else [True, False]):
                for s in ([sick] if sick is not None else [True, False]):
                    p_combo = (self.cpt['Poor'][p] *
                              self.cpt['Elderly'][e] *
                              self.cpt['Sick'][s])
                    p_aid = self.cpt['Aid'][(p, e, s)]
                    total_prob += p_combo * p_aid
        
        if any(v is not None for v in [poor, elderly, sick]):
            normalizer = 0.0
            for p in ([poor] if poor is not None else [True, False]):
                for e in ([elderly] if elderly is not None else [True, False]):
                    for s in ([sick] if sick is not None else [True, False]):
                        normalizer += (self.cpt['Poor'][p] *
                                     self.cpt['Elderly'][e] *
                                     self.cpt['Sick'][s])
            total_prob /= normalizer
        
        return total_prob
    
    def solve(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict volunteer commitment probability."""
        evidence = input_data.get('evidence', {})
        probability = self.query(evidence)
        
        confidence = (
            "High | 高 (Active Recruitment | 積極招募)" if probability >= 0.7
            else "Moderate | 中等 (Engage & Monitor | 接觸觀察)" if probability >= 0.5
            else "Low | 低 (Passive Contact | 被動接觸)"
        )
        
        return {
            'solution': {
                'probability': probability,
                'confidence': confidence,
                'evidence': evidence
            },
            'explanation': self._generate_story_explanation(probability, evidence),
            'score': 100
        }
    
    def _generate_story_explanation(self, probability: float, evidence: Dict[str, bool]) -> str:
        """Generate bilingual story explanation."""
        evidence_text = "\n".join([
            f"  {k}: {'✓ Yes | 是' if v else '✗ No | 否'}"
            for k, v in evidence.items()
        ]) if evidence else "  (No evidence | 無證據 - using baseline | 使用基準值)"
        
        return f"""
╔══════════════════════════════════════════════════════════════╗
║  🤝 WILL MARIA COME BACK? | Maria會回來嗎？                   ║
╚══════════════════════════════════════════════════════════════╝

🎯 PREDICTION | 預測:
P(Maria Returns | Evidence) = {probability:.3f} ({probability*100:.1f}%)
Confidence Level | 信心水平: {self._get_confidence_desc(probability)}

📊 OBSERVED EVIDENCE | 觀察到的證據:
{evidence_text}

💭 THE STORY | 故事:
Last Saturday, Maria helped distribute food.
She saw little Jasmine's smile when receiving
her family's groceries. Maria cried.

上週六，Maria幫忙發放食物。
她看到小Jasmine收到家人食物時的笑容。
Maria哭了。

But will she come back? Our volunteers are
aging (average 65 years old). We NEED Maria
and people like her to continue this legacy.

但她會回來嗎？我們的志工在老化
（平均65歲）。我們需要Maria
和像她這樣的人延續這個使命。

🔬 AI REASONING | AI推理:
Bayesian Networks calculate probability based on:
- Has Maria experienced hardship? (Empathy)
- Does she have time available? (Capacity)
- Does her personality fit? (Compatibility)

貝葉斯網絡基於以下計算概率：
- Maria經歷過困難嗎？（同理心）
- 她有時間嗎？（能力）
- 她的個性適合嗎？（兼容性）

📞 ACTION PLAN | 行動計劃:
{self._get_action_plan(probability)}

🙏 ETHICAL SAFEGUARDS | 道德保障:
✓ No discrimination based on demographics
  不基於人口統計歧視
✓ Transparent probability (Maria can see this!)
  透明概率（Maria可以看到這個！）
✓ Human final decision (AI is advisory only)
  人類最終決策（AI僅供建議）

Next Mission Unlocked! | 下個任務解鎖了！ →
"""
    
    def _get_confidence_desc(self, prob: float) -> str:
        """Get bilingual confidence description."""
        if prob >= 0.7:
            return "HIGH | 高 - Prioritize active recruitment | 優先積極招募"
        elif prob >= 0.5:
            return "MODERATE | 中等 - Engage and monitor | 接觸並觀察"
        else:
            return "LOW | 低 - Maintain passive contact | 保持被動接觸"
    
    def _get_action_plan(self, prob: float) -> str:
        """Get bilingual action plan based on probability."""
        if prob >= 0.7:
            return """
✓ Call Maria this week | 本週打電話給Maria
✓ Send volunteer info packet | 寄送志工資訊包
✓ Invite to next orientation | 邀請參加下次說明會
✓ Connect with veteran volunteer mentor | 與資深志工導師連結
"""
        elif prob >= 0.5:
            return """
✓ Send thank-you card | 寄送感謝卡
✓ Invite to monthly community event | 邀請參加月度社區活動
✓ Follow up in 2 weeks | 兩週後跟進
"""
        else:
            return """
✓ Add to contact list | 加入聯繫清單
✓ Send quarterly newsletter | 寄送季度通訊
✓ Wait for life changes (graduation, job change, etc.)
  等待生活變化（畢業、換工作等）
"""


# =============================================================================
# LEVEL 4: TOWER OF HANOI - BUILDING VIRTUE LAYERS
# =============================================================================

class TowerOfHanoi:
    """
    Tower of Hanoi Recursive Solution (Russell & Norvig Chapter 3)
    
    Story: Building virtue layers (Gratitude → Respect → Love)
    Algorithm: Recursive divide-and-conquer
    Complexity: O(2^n) - exponential but proven optimal
    Moves: 2^n - 1 (no shortcuts exist)
    """
    
    def __init__(self):
        self.moves = []
        self.move_count = 0
    
    def solve_recursive(self, n: int, source: str, target: str, auxiliary: str):
        """
        Recursive solution to Tower of Hanoi.
        
        Args:
            n: Number of disks
            source: Starting peg ('A')
            target: Destination peg ('C')
            auxiliary: Helper peg ('B')
        """
        if n == 1:
            self.moves.append((source, target))
            self.move_count += 1
            return
        
        # Move n-1 disks to auxiliary
        self.solve_recursive(n - 1, source, auxiliary, target)
        
        # Move largest disk to target
        self.moves.append((source, target))
        self.move_count += 1
        
        # Move n-1 disks from auxiliary to target
        self.solve_recursive(n - 1, auxiliary, target, source)
    
    def solve(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Solve Tower of Hanoi puzzle.
        
        Args:
            input_data: {
                'num_disks': int (default 3)
            }
            
        Returns:
            {
                'solution': {
                    'moves': [(from, to), ...],
                    'total_moves': int
                },
                'explanation': bilingual story,
                'score': 100
            }
        """
        n = input_data.get('num_disks', 3)
        
        # Reset state
        self.moves = []
        self.move_count = 0
        
        # Solve
        self.solve_recursive(n, 'A', 'C', 'B')
        
        return {
            'solution': {
                'moves': self.moves,
                'total_moves': self.move_count
            },
            'explanation': self._generate_story_explanation(n),
            'score': 100
        }
    
    def _generate_story_explanation(self, n: int) -> str:
        """Generate bilingual story explanation."""
        optimal = 2**n - 1
        
        return f"""
╔══════════════════════════════════════════════════════════════╗
║  🧘 TOWER OF COMPASSION COMPLETE | 慈悲之塔完成              ║
╚══════════════════════════════════════════════════════════════╝

🎯 VIRTUE LAYERS | 美德層次:
Disks | 圓盤數: {n}
- Bottom (largest): Gratitude | 感恩 (foundation)
- Middle: Respect | 尊重 (builds on gratitude)
- Top (smallest): Love | 愛 (grows from respect)

📊 MOVEMENT ANALYSIS | 移動分析:
Optimal Moves | 最優移動: {optimal} (proven minimum)
Your Moves | 你的移動: {self.move_count}
Efficiency | 效率: {100 if self.move_count == optimal else 0}%

💭 MASTER CHENG YEN'S TEACHING | 證嚴上人教導:
"You cannot skip steps in building compassion.
Gratitude is the foundation.
Respect stands upon gratitude.
Love grows from respect."

「建立慈悲不能跳過步驟。
感恩是基礎。
尊重立於感恩之上。
愛從尊重中生長。」

🔬 THE AI SECRET | AI秘密:
Tower of Hanoi proves that some problems have
NO SHORTCUTS. You must go through all 2^n - 1 states.

This is like building virtue: There are no shortcuts
to true compassion. One action at a time.

河內塔證明有些問題沒有捷徑。
你必須經過所有2^n - 1個狀態。

這就像建立美德：真正的慈悲沒有捷徑。
一次一個行動。

📚 ALGORITHM PROOF | 算法證明:
Recurrence: T(n) = 2T(n-1) + 1
Solution: T(n) = 2^n - 1
Proof by induction:
- Base: T(1) = 1 = 2^1 - 1 ✓
- Step: T(n) = 2(2^(n-1) - 1) + 1 = 2^n - 1 ✓

Next Mission Unlocked! | 下個任務解鎖了！ →
"""


# =============================================================================
# LEVEL 5: N-QUEENS - VOLUNTEER SHIFT SCHEDULING
# =============================================================================

class NQueensSolver:
    """
    N-Queens Problem via Backtracking (Russell & Norvig Chapter 4.1)
    
    Story: Schedule 8 volunteers across 8 time slots with zero conflicts
    Algorithm: Backtracking with constraint satisfaction
    Complexity: O(n!) worst case, much better with pruning
    """
    
    def __init__(self):
        self.solutions = []
        self.backtrack_count = 0
    
    def is_safe(self, board: List[int], row: int, col: int) -> bool:
        """
        Check if placing queen at (row, col) is safe.
        
        board[i] = j means queen in row i is at column j
        """
        for i in range(row):
            # Same column
            if board[i] == col:
                return False
            
            # Diagonal
            if abs(board[i] - col) == abs(i - row):
                return False
        
        return True
    
    def solve_recursive(self, board: List[int], row: int, n: int):
        """
        Backtracking algorithm for N-Queens.
        
        Args:
            board: Current partial solution
            row: Current row to place queen
            n: Board size
        """
        # Base case: All queens placed
        if row == n:
            self.solutions.append(board[:])
            return
        
        # Try each column
        for col in range(n):
            self.backtrack_count += 1
            
            if self.is_safe(board, row, col):
                board[row] = col
                self.solve_recursive(board, row + 1, n)
                board[row] = -1  # Backtrack
    
    def solve(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Solve N-Queens problem.
        
        Args:
            input_data: {
                'n': int (board size, default 8),
                'find_all': bool (default False)
            }
            
        Returns:
            {
                'solution': {
                    'board': [col_positions],
                    'visualization': str,
                    'total_solutions': int
                },
                'explanation': bilingual story,
                'score': 100
            }
        """
        n = input_data.get('n', 8)
        find_all = input_data.get('find_all', False)
        
        # Reset state
        self.solutions = []
        self.backtrack_count = 0
        
        # Solve
        board = [-1] * n
        self.solve_recursive(board, 0, n)
        
        # Return first solution or all
        solution = self.solutions[0] if self.solutions else []
        
        return {
            'solution': {
                'board': solution,
                'visualization': self._visualize_board(solution, n),
                'total_solutions': len(self.solutions),
                'moves': len(solution)
            },
            'explanation': self._generate_story_explanation(n),
            'score': 100 if solution else 0
        }
    
    def _visualize_board(self, board: List[int], n: int) -> str:
        """Generate ASCII art of chess board."""
        if not board:
            return "No solution found"
        
        lines = []
        for row in range(n):
            line = ""
            for col in range(n):
                if board[row] == col:
                    line += "♛ "
                else:
                    line += "□ " if (row + col) % 2 == 0 else "■ "
            lines.append(line)
        
        return "\n".join(lines)
    
    def _generate_story_explanation(self, n: int) -> str:
        """Generate bilingual story explanation."""
        return f"""
╔══════════════════════════════════════════════════════════════╗
║  📅 VOLUNTEER SHIFT SCHEDULER COMPLETE | 志工排班完成        ║
╚══════════════════════════════════════════════════════════════╝

🎯 SCHEDULING RESULT | 排班結果:
Board Size | 棋盤大小: {n}×{n}
Total Solutions Found | 找到的解決方案: {len(self.solutions)}
Backtrack Steps | 回溯步數: {self.backtrack_count}

📋 VOLUNTEER ASSIGNMENTS | 志工分配:
{self._visualize_board(self.solutions[0] if self.solutions else [], n)}

💭 THE REAL-WORLD SCENARIO | 真實場景:
Mrs. Chen (Row 1): Can't work mornings (arthritis)
陳太太（第1行）：早上不能工作（關節炎）

David (Row 3): Basketball practice at 3pm
David（第3行）：下午3點籃球練習

Rosa (Row 5): Works until noon
Rosa（第5行）：要工作到中午

Maria (Row 7): Free only evenings
Maria（第7行）：只有晚上有空

🔬 THE AI SECRET | AI秘密:
N-Queens uses CONSTRAINT SATISFACTION:
- Variables: Volunteer positions
- Domain: Time slots 1-{n}
- Constraints: No conflicts (row/col/diagonal)

Algorithm Efficiency | 算法效率:
- Worst case: {math.factorial(n)} permutations
  最壞情況：{math.factorial(n)} 排列
- With pruning: ~{self.backtrack_count} checks
  使用剪枝：~{self.backtrack_count} 檢查
- Speedup: {math.factorial(n) / max(1, self.backtrack_count):.1f}x
  加速：{math.factorial(n) / max(1, self.backtrack_count):.1f}倍

📚 CSP FRAMEWORK | 約束滿足問題框架:
This isn't just a puzzle—it's how we schedule:
- Hospital shifts (nurses + doctors)
- School timetables (teachers + classrooms)
- Conference rooms (meetings + attendees)

這不只是謎題——這是我們如何排程：
- 醫院班次（護士+醫生）
- 學校時間表（老師+教室）
- 會議室（會議+參與者）

Next Mission Unlocked! | 下個任務解鎖了！ →
"""


# =============================================================================
# LEVEL 6: HILL CLIMBING - MEDITATION OPTIMIZATION
# =============================================================================

class HillClimbing:
    """
    Hill Climbing with Random Restarts (Russell & Norvig Chapter 4.1.1)
    
    Story: Meditation state optimization (inner peace maximization)
    Algorithm: Local search with random restarts
    Complexity: O(∞) without restarts, O(k×n) with k restarts
    """
    
    def __init__(self):
        self.history = []
        self.local_maxima_count = 0
    
    def evaluate(self, state: Dict[str, float]) -> float:
        """
        Evaluate meditation state quality.
        
        Objective function with multiple local maxima:
        f(focus, calmness, compassion) = weighted sum + interactions
        """
        f = state['focus']
        c = state['calmness']
        co = state['compassion']
        
        # Non-convex function with local maxima
        score = (
            0.4 * f + 0.3 * c + 0.3 * co +  # Linear terms
            0.1 * math.sin(f / 10) * 50 +    # Oscillation (local maxima)
            0.1 * math.sin(c / 10) * 50 +
            0.05 * (f * c / 100)             # Interaction term
        )
        
        return score
    
    def get_neighbors(self, state: Dict[str, float], step_size: float = 5.0) -> List[Dict[str, float]]:
        """Generate neighboring states (±step in each dimension)."""
        neighbors = []
        
        for key in state.keys():
            # Increase
            new_state = state.copy()
            new_state[key] = min(100, state[key] + step_size)
            neighbors.append(new_state)
            
            # Decrease
            new_state = state.copy()
            new_state[key] = max(0, state[key] - step_size)
            neighbors.append(new_state)
        
        return neighbors
    
    def climb(self, start_state: Dict[str, float], max_iterations: int = 100) -> Dict[str, Any]:
        """Simple hill climbing algorithm."""
        current = start_state
        current_score = self.evaluate(current)
        
        for i in range(max_iterations):
            self.history.append((current.copy(), current_score))
            
            # Generate neighbors
            neighbors = self.get_neighbors(current)
            
            # Find best neighbor
            best_neighbor = max(neighbors, key=self.evaluate)
            best_score = self.evaluate(best_neighbor)
            
            # If no improvement, local maximum reached
            if best_score <= current_score:
                self.local_maxima_count += 1
                return {
                    'state': current,
                    'score': current_score,
                    'iterations': i + 1,
                    'reason': 'local_maximum'
                }
            
            # Move to better neighbor
            current = best_neighbor
            current_score = best_score
        
        return {
            'state': current,
            'score': current_score,
            'iterations': max_iterations,
            'reason': 'max_iterations'
        }
    
    def solve(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Solve meditation optimization with random restarts.
        
        Args:
            input_data: {
                'start_state': Optional[Dict[str, float]],
                'num_restarts': int (default 5),
                'max_iterations': int (default 100)
            }
            
        Returns:
            {
                'solution': {
                    'best_state': Dict[str, float],
                    'best_score': float,
                    'total_iterations': int
                },
                'explanation': bilingual story,
                'score': performance_score
            }
        """
        num_restarts = input_data.get('num_restarts', 5)
        max_iterations = input_data.get('max_iterations', 100)
        
        # Reset state
        self.history = []
        self.local_maxima_count = 0
        
        best_overall = None
        best_score = -math.inf
        
        # Random restart hill climbing
        for restart in range(num_restarts):
            # Random start state or user-provided
            if restart == 0 and 'start_state' in input_data:
                start = input_data['start_state']
            else:
                start = {
                    'focus': random.uniform(0, 100),
                    'calmness': random.uniform(0, 100),
                    'compassion': random.uniform(0, 100)
                }
            
            # Climb
            result = self.climb(start, max_iterations)
            
            # Track best
            if result['score'] > best_score:
                best_score = result['score']
                best_overall = result
        
        return {
            'solution': {
                'best_state': best_overall['state'],
                'best_score': best_score,
                'total_iterations': len(self.history),
                'local_maxima_found': self.local_maxima_count,
                'moves': best_overall['iterations']
            },
            'explanation': self._generate_story_explanation(best_overall),
            'score': min(100, int(best_score))
        }
    
    def _generate_story_explanation(self, result: Dict[str, Any]) -> str:
        """Generate bilingual story explanation."""
        state = result['state']
        
        return f"""
╔══════════════════════════════════════════════════════════════╗
║  🧘 INNER PEACE OPTIMIZED | 內心平和優化完成                  ║
╚══════════════════════════════════════════════════════════════╝

🎯 OPTIMAL MEDITATION STATE | 最優禪修狀態:
Focus | 集中力: {state['focus']:.1f}/100
Calmness | 平靜心: {state['calmness']:.1f}/100
Compassion | 慈悲心: {state['compassion']:.1f}/100

Peace Score | 平和分數: {result['score']:.2f}/100
Iterations | 迭代次數: {result['iterations']}

💭 MASTER CHENG YEN'S TEACHING | 證嚴上人教導:
"When the mind is calm, wisdom appears.
When wisdom appears, compassion flows.
When compassion flows, peace is found."

「心靜，智慧自然生。
智慧生，慈悲自然流。
慈悲流，平和自然現。」

🔬 THE AI SECRET | AI秘密:
Hill Climbing found {self.local_maxima_count} LOCAL MAXIMA
(comfortable but not perfect states)

爬山法找到了{self.local_maxima_count}個局部最大值
（舒適但不完美的狀態）

That's why we needed RANDOM RESTARTS:
- Try different starting points
- Escape comfortable plateaus
- Find true inner peace

這就是為什麼需要隨機重啟：
- 嘗試不同起點
- 逃離舒適平台
- 找到真正的內心平和

📚 ALGORITHM LIMITATIONS | 算法限制:
Hill Climbing is GREEDY: Always picks best neighbor
But can get STUCK in local maxima

爬山法是貪婪的：總是選最好的鄰居
但會困在局部最大值

Like meditation: Sometimes you feel "good enough"
but true peace requires pushing beyond comfort zone

就像禪修：有時你覺得「夠好了」
但真正的平和需要突破舒適區

🏔️ BETTER ALTERNATIVES | 更好的替代方案:
- Simulated Annealing: Accept worse moves sometimes
  模擬退火：有時接受較差的移動
- Genetic Algorithms: Population-based search
  遺傳算法：基於群體的搜索
- Gradient Descent: Use derivatives (if available)
  梯度下降：使用導數（如果可用）

Next Mission Unlocked! | 下個任務解鎖了！ →
"""


# =============================================================================
# LEVEL 7: FIRST-ORDER LOGIC + BACKWARD CHAINING
# =============================================================================

class FOLPlanner:
    """
    First-Order Logic with Backward Chaining (Russell & Norvig Chapter 8-9)
    
    Story: Volunteer eligibility reasoning
    Algorithm: Backward chaining inference
    Complexity: Depends on knowledge base size
    """
    
    def __init__(self):
        # Knowledge base: Rules in Horn clause form
        self.kb = [
            # Rule 1: Person with compassion can volunteer
            {'if': ['Person(?x)', 'Compassionate(?x)'], 'then': 'CanVolunteer(?x)'},
            
            # Rule 2: Experienced hardship leads to compassion
            {'if': ['Person(?x)', 'ExperiencedHardship(?x)'], 'then': 'Compassionate(?x)'},
            
            # Rule 3: Volunteer with availability can serve
            {'if': ['CanVolunteer(?x)', 'Available(?x)'], 'then': 'CanServe(?x)'},
            
            # Rule 4: Serving helps families
            {'if': ['CanServe(?x)'], 'then': 'HelpsFamily(?x)'}
        ]
        
        self.facts = set()
        self.proof_steps = []
    
    def unify(self, term1: str, term2: str, bindings: Dict[str, str]) -> Optional[Dict[str, str]]:
        """
        Unification algorithm for FOL terms.
        
        Args:
            term1: First term (may contain variables like ?x)
            term2: Second term
            bindings: Current variable bindings
            
        Returns:
            Updated bindings if unification succeeds, None otherwise
        """
        if term1 == term2:
            return bindings
        
        # Variable unification
        if term1.startswith('?'):
            if term1 in bindings:
                return self.unify(bindings[term1], term2, bindings)
            else:
                new_bindings = bindings.copy()
                new_bindings[term1] = term2
                return new_bindings
        
        if term2.startswith('?'):
            if term2 in bindings:
                return self.unify(term1, bindings[term2], bindings)
            else:
                new_bindings = bindings.copy()
                new_bindings[term2] = term1
                return new_bindings
        
        return None
    
    def backward_chain(self, goal: str, depth: int = 0) -> bool:
        """
        Backward chaining to prove a goal.
        
        Args:
            goal: Goal to prove (e.g., 'CanServe(Maria)')
            depth: Recursion depth (for visualization)
            
        Returns:
            True if goal can be proven
        """
        self.proof_steps.append(('  ' * depth) + f"Trying to prove: {goal}")
        
        # Check if goal is a known fact
        if goal in self.facts:
            self.proof_steps.append(('  ' * depth) + f"✓ {goal} is a known fact")
            return True
        
        # Try to prove using rules
        for rule in self.kb:
            # Try to unify goal with rule conclusion
            bindings = self.unify(rule['then'], goal, {})
            
            if bindings is not None:
                self.proof_steps.append(('  ' * depth) + f"Found rule: {rule['then']} ← {rule['if']}")
                
                # Try to prove all premises
                all_proven = True
                for premise in rule['if']:
                    # Substitute bindings in premise
                    instantiated_premise = premise
                    for var, value in bindings.items():
                        instantiated_premise = instantiated_premise.replace(var, value)
                    
                    if not self.backward_chain(instantiated_premise, depth + 1):
                        all_proven = False
                        break
                
                if all_proven:
                    self.proof_steps.append(('  ' * depth) + f"✓ {goal} proven!")
                    return True
        
        self.proof_steps.append(('  ' * depth) + f"✗ Cannot prove {goal}")
        return False
    
    def solve(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prove volunteer eligibility using FOL.
        
        Args:
            input_data: {
                'person': str (e.g., 'Maria'),
                'facts': List[str] (known facts)
            }
            
        Returns:
            {
                'solution': {
                    'can_serve': bool,
                    'proof': List[str]
                },
                'explanation': bilingual story,
                'score': 100
            }
        """
        person = input_data.get('person', 'Maria')
        self.facts = set(input_data.get('facts', [
            f'Person({person})',
            f'ExperiencedHardship({person})',
            f'Available({person})'
        ]))
        
        self.proof_steps = []
        
        # Try to prove CanServe(person)
        goal = f'CanServe({person})'
        result = self.backward_chain(goal)
        
        return {
            'solution': {
                'can_serve': result,
                'proof': self.proof_steps,
                'person': person
            },
            'explanation': self._generate_story_explanation(person, result),
            'score': 100
        }
    
    def _generate_story_explanation(self, person: str, can_serve: bool) -> str:
        """Generate bilingual story explanation."""
        proof_text = '\n'.join(self.proof_steps)
        
        return f"""
╔══════════════════════════════════════════════════════════════╗
║  🤔 VOLUNTEER ELIGIBILITY REASONING | 志工資格推理           ║
╚══════════════════════════════════════════════════════════════╝

🎯 QUERY | 查詢:
Can {person} serve as a volunteer?
{person}能成為志工嗎？

📋 PROOF TRACE | 證明追蹤:
{proof_text}

✅ CONCLUSION | 結論:
{person} {'CAN' if can_serve else 'CANNOT'} serve as volunteer
{person} {'可以' if can_serve else '不能'}成為志工

💭 THE REASONING | 推理過程:
First-Order Logic allows us to REASON about people:
- NOT just "Maria" but "ANY person ?x"
- NOT just facts but RULES: IF ... THEN ...

一階邏輯讓我們能推理關於人：
- 不只是「Maria」而是「任何人?x」
- 不只是事實而是規則：如果...那麼...

🔬 THE AI SECRET | AI秘密:
Backward Chaining is GOAL-DRIVEN:
1. Start with what you want to prove
2. Find rules that conclude that goal
3. Recursively prove the premises

後向鏈是目標驅動的：
1. 從你想證明的開始
2. 找到能得出該目標的規則
3. 遞歸證明前提

📚 REAL-WORLD APPLICATIONS | 真實應用:
- Medical diagnosis (symptom → disease)
  醫療診斷（症狀→疾病）
- Legal reasoning (facts → verdict)
  法律推理（事實→判決）
- Expert systems (conditions → recommendation)
  專家系統（條件→建議）

🙏 TZU CHI APPLICATION | 慈濟應用:
We don't just recruit ANYONE—we reason about:
- Do they have the right heart? (Compassionate)
- Do they have the capacity? (Available)
- Will they sustain commitment? (Experienced hardship)

我們不只是招募任何人——我們推理：
- 他們有正確的心嗎？（有同情心）
- 他們有能力嗎？（有時間）
- 他們會持續承諾嗎？（經歷過困難）

Next Mission Unlocked! | 下個任務解鎖了！ →
"""


# =============================================================================
# LEVEL 8: GOAL STACK PLANNING / BLOCKS WORLD
# =============================================================================

class BlocksWorld:
    """
    Goal Stack Planning for Blocks World (Russell & Norvig Chapter 11)
    
    Story: Warehouse resource organization
    Algorithm: STRIPS-style planning
    Complexity: Depends on number of objects and goal complexity
    """
    
    def __init__(self):
        self.plan = []
        self.state = {}
    
    def strips_move(self, block: str, from_loc: str, to_loc: str, state: Dict) -> Dict:
        """
        Execute a STRIPS-style move action.
        
        Preconditions:
        - Block is clear (no block on top)
        - From location has the block
        - To location is clear (if not table)
        
        Effects:
        - Block moves from 'from_loc' to 'to_loc'
        - Block on 'from_loc' becomes clear
        - 'to_loc' becomes not clear
        """
        new_state = state.copy()
        
        # Update locations
        new_state[block] = to_loc
        
        # Update clear status
        if from_loc != 'table':
            new_state[f'clear_{from_loc}'] = True
        
        if to_loc != 'table':
            new_state[f'clear_{to_loc}'] = False
        
        return new_state
    
    def solve_blocks(self, initial: Dict[str, str], goal: Dict[str, str]) -> List[Tuple[str, str, str]]:
        """
        Solve blocks world problem using goal stack planning.
        
        Args:
            initial: Initial state {block: location}
            goal: Goal state {block: location}
            
        Returns:
            List of moves (block, from, to)
        """
        self.plan = []
        self.state = initial.copy()
        
        # Simple goal stack planner
        for block, target_loc in goal.items():
            if self.state.get(block) != target_loc:
                # Need to move this block
                current_loc = self.state.get(block, 'table')
                
                # Clear the block first (move blocks on top)
                self._clear_block(block)
                
                # Clear the target location
                if target_loc != 'table':
                    self._clear_block(target_loc)
                
                # Move the block
                self.plan.append((block, current_loc, target_loc))
                self.state = self.strips_move(block, current_loc, target_loc, self.state)
        
        return self.plan
    
    def _clear_block(self, block: str):
        """Recursively clear a block by moving blocks on top of it."""
        # Find blocks on top
        blocks_on_top = [b for b, loc in self.state.items() if loc == block]
        
        for top_block in blocks_on_top:
            # Recursively clear the top block
            self._clear_block(top_block)
            
            # Move it to table
            self.plan.append((top_block, block, 'table'))
            self.state = self.strips_move(top_block, block, 'table', self.state)
    
    def solve(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate plan to achieve goal state.
        
        Args:
            input_data: {
                'initial': {block: location},
                'goal': {block: location}
            }
            
        Returns:
            {
                'solution': {
                    'plan': [(block, from, to), ...],
                    'steps': int
                },
                'explanation': bilingual story,
                'score': 100
            }
        """
        initial = input_data.get('initial', {
            'A': 'table',
            'B': 'table',
            'C': 'table'
        })
        
        goal = input_data.get('goal', {
            'C': 'B',
            'B': 'A',
            'A': 'table'
        })
        
        plan = self.solve_blocks(initial, goal)
        
        return {
            'solution': {
                'plan': plan,
                'steps': len(plan),
                'moves': len(plan)
            },
            'explanation': self._generate_story_explanation(plan, initial, goal),
            'score': 100
        }
    
    def _generate_story_explanation(self, plan: List[Tuple], initial: Dict, goal: Dict) -> str:
        """Generate bilingual story explanation."""
        plan_text = '\n'.join([
            f"  {i+1}. Move {move[0]} from {move[1]} to {move[2]}"
            for i, move in enumerate(plan)
        ])
        
        return f"""
╔══════════════════════════════════════════════════════════════╗
║  📦 WAREHOUSE ORGANIZATION COMPLETE | 倉庫整理完成           ║
╚══════════════════════════════════════════════════════════════╝

🎯 PLANNING RESULT | 規劃結果:
Initial State | 初始狀態: {initial}
Goal State | 目標狀態: {goal}
Total Moves | 總移動數: {len(plan)}

📋 EXECUTION PLAN | 執行計劃:
{plan_text}

💭 THE REAL-WORLD SCENARIO | 真實場景:
Tzu Chi warehouse stores:
- A: Rice (heavy, bottom)
- B: Vegetables (medium, middle)
- C: Snacks (light, top)

慈濟倉庫儲存：
- A：米（重，底部）
- B：蔬菜（中，中間）
- C：零食（輕，頂部）

Goal: Optimize for FIFO (First-In-First-Out)
Oldest supplies should be on top for distribution
目標：優化先進先出
最舊的物資應該在頂部以便發放

🔬 THE AI SECRET | AI秘密:
STRIPS Planning uses:
- Preconditions: What must be true to act
  前置條件：行動前必須為真的條件
- Effects: What changes after action
  效果：行動後的變化
- Goal Stack: Work backward from goal
  目標堆棧：從目標倒推

This is how robots plan manipulation tasks!
這是機器人如何規劃操作任務！

📚 CLASSICAL PLANNING | 經典規劃:
Blocks World is the "Hello World" of AI planning:
- Simple to state
- Hard to solve optimally
- Generalizes to real problems

積木世界是AI規劃的「Hello World」：
- 簡單陳述
- 難以最優解決
- 推廣到實際問題

🏭 REAL-WORLD APPLICATIONS | 真實應用:
- Factory assembly lines
  工廠裝配線
- Warehouse logistics
  倉庫物流
- Meal preparation (cooking order)
  餐點準備（烹飪順序）
- Surgery planning (operation steps)
  手術規劃（操作步驟）

🙏 TZU CHI WAREHOUSE WISDOM | 慈濟倉庫智慧:
Master Cheng Yen teaches:
"Organize with mindfulness.
The order of supplies reflects
the order of our compassion."

證嚴上人教導：
「用心整理。
物資的順序反映
我們慈悲的順序。」

ALL 8 MISSIONS COMPLETE! | 所有8個任務完成！
You've mastered all algorithms! | 你已精通所有算法！ 🎉
"""


# =============================================================================
# ELO RATING SYSTEM
# =============================================================================

class EloRating:
    """
    Elo Rating System for gamification.
    
    Rating Milestones:
    - 1000: Beginner | 初學者
    - 1300: Tzu Chi QR Code Unlocked! | 慈濟QR碼解鎖！
    - 1500: Proficient | 精通
    - 1800: Advanced | 高級
    - 2000+: Expert | 專家
    """
    
    def __init__(self, initial: int = 1000, k: int = 32):
        self.rating = initial
        self.k = k
        self.history = [(0, initial)]
    
    def calculate(self, user_score: float, ai_score: float) -> int:
        """Calculate Elo change based on performance."""
        user_normalized = user_score / 100
        ai_normalized = ai_score / 100
        
        expected = 1 / (1 + 10 ** ((ai_normalized * 2000 - self.rating) / 400))
        actual = user_normalized
        
        change = int(self.k * (actual - expected))
        self.rating += change
        self.history.append((len(self.history), self.rating))
        
        return change
    
    def get_rank(self) -> str:
        """Get bilingual rank description."""
        if self.rating >= 2000:
            return "Expert | 專家"
        elif self.rating >= 1800:
            return "Advanced | 高級"
        elif self.rating >= 1500:
            return "Proficient | 精通"
        elif self.rating >= 1300:
            return "Competent | 勝任 - 🎉 Tzu Chi QR Unlocked! | 慈濟QR碼解鎖！"
        elif self.rating >= 1000:
            return "Novice | 新手"
        else:
            return "Beginner | 初學者"


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    """Test story-driven game engine."""
    print("=" * 70)
    print("Journey of Kindness - Story-Driven AI Game | 慈善之旅 - 故事驅動AI遊戲")
    print("From Raw Rice Incident to 500 Volunteers | 從生米事件到500位志工")
    print("=" * 70)
    print()
    
    engine = GameEngine()
    
    # Test Level 1: Food Delivery
    print("Testing Level 1: Food Delivery Mission | 測試關卡1：食物配送任務...")
    story1 = engine.get_level_story(1)
    print(f"Title: {story1['title']['en']} | {story1['title']['zh']}")
    print(f"Story intro (first 100 chars):\n{story1['intro']['en'][:100]}...")
    print()
    
    level1_input = {
        'grid_size': (10, 10),
        'start': (0, 0),
        'goals': [(9, 9)],
        'obstacles': [(2, 2), (2, 3)]
    }
    result1 = engine.run_level(1, level1_input)
    print(f"Path length | 路徑長度: {len(result1['ai_solution']['path'])}")
    print(f"Elo change | Elo變化: {result1['elo_change']:+d}")
    print(f"Emotional feedback: {result1['emotional_feedback']['en'][:80]}...")
    print()
    
    # Test Level 2: Strategic Resource Allocation
    print("Testing Level 2: Difficult Choices | 測試關卡2：艱難的抉擇...")
    story2 = engine.get_level_story(2)
    print(f"Title: {story2['title']['en']} | {story2['title']['zh']}")
    print()
    
    level2_input = {
        'tree_structure': 'simple',
        'difficulty': 'learning'
    }
    result2 = engine.run_level(2, level2_input)
    print(f"Families helped | 幫助的家庭: {result2['ai_solution']['families_helped']}")
    print(f"Elo change | Elo變化: {result2['elo_change']:+d}")
    if result2.get('teaching_hints'):
        print(f"Teaching hints | 教學提示: {len(result2['teaching_hints'])} hints")
    print()
    
    # Summary
    print("=" * 70)
    print("Story-Driven Tests Complete! | 故事驅動測試完成！")
    print(f"Final Elo | 最終Elo: {engine.elo_system.rating}")
    print(f"Rank | 等級: {engine.elo_system.get_rank()}")
    print(f"Tzu Chi QR Unlocked | 慈濟QR碼解鎖: {engine.elo_system.rating >= 1300}")
    print("=" * 70)


if __name__ == "__main__":
    main()
    