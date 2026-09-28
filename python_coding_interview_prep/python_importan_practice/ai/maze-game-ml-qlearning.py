import numpy as np
import pygame
import sys
import time

# --- 1. SETUP THE MAZE ---
# The original string list had spaces, which makes indexing confusing.
# I've converted it to a clean 2D grid where each character is a cell.
maze_str = [
    "S...................",
    ".##.#####.#####.###.",
    ".#......#.#.....#.#.",
    ".#.####.#.#.###.#.#.",
    ".#.#..#.#...#.#.#.#.",
    ".#.#.##.###.#.#.#.#.",
    ".#.#.....#..#.#...#.",
    ".#.#####.#.##.###.#.",
    ".#.......#....#...#.",
    ".#########.##.#.#.#.",
    "..........#..#.#.#.#",
    ".########.#.##.#.#.#",
    ".#......#.#....#.#..",
    ".#.####.#.######.##.",
    "...#..#...........G."
]
MAZE = [list(row) for row in maze_str]
ROWS = len(MAZE)
COLS = len(MAZE[0])

# --- 2. Q-LEARNING SETUP ---
# Q-table: dimensions are (Rows, Cols, Actions)
# Actions: 0=Right, 1=Down, 2=Left, 3=Up
Q = np.zeros((ROWS, COLS, 4))
go = np.array([(0, 1), (1, 0), (0, -1), (-1, 0)])  # (y, x) offsets for actions

# Hyperparameters
EPISODES = 100
ALPHA = 0.1  # Learning rate
GAMMA = 0.9  # Discount factor
EPSILON = 0.2  # Exploration rate (chance to take a random action)

# --- 3. PYGAME VISUALIZER SETUP ---
pygame.init()
CELL_SIZE = 30
PADDING = 10
WIDTH = COLS * CELL_SIZE + PADDING * 2
HEIGHT = ROWS * CELL_SIZE + PADDING * 2 + 30  # Extra space for text
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Q-Learning Maze")
clock = pygame.time.Clock()

# Colors (matching the screenshot dark theme)
BG_COLOR = (18, 22, 28)
WALL_COLOR = (60, 70, 90)
PATH_COLOR = (30, 35, 45)
START_COLOR = (50, 150, 200)
GOAL_COLOR = (50, 200, 150)
AGENT_COLOR = (255, 100, 100)
TEXT_COLOR = (200, 200, 200)

font = pygame.font.SysFont("monospace", 20, bold=True)


def draw_maze(agent_pos, episode, status_text):
    screen.fill(BG_COLOR)

    # Draw Grid
    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(PADDING + c * CELL_SIZE, PADDING + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if MAZE[r][c] == '#':
                pygame.draw.rect(screen, WALL_COLOR, rect)
                pygame.draw.rect(screen, BG_COLOR, rect, 2)  # Grid lines
            else:
                pygame.draw.rect(screen, PATH_COLOR, rect)
                pygame.draw.rect(screen, BG_COLOR, rect, 2)

            if MAZE[r][c] == 'S':
                pygame.draw.rect(screen, START_COLOR, rect.inflate(-10, -10), border_radius=5)
            elif MAZE[r][c] == 'G':
                pygame.draw.rect(screen, GOAL_COLOR, rect.inflate(-10, -10), border_radius=5)

    # Draw Agent
    if agent_pos:
        ay, ax = agent_pos
        agent_rect = pygame.Rect(PADDING + ax * CELL_SIZE, PADDING + ay * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.circle(screen, AGENT_COLOR, agent_rect.center, CELL_SIZE // 3)

    # Draw Text
    ep_text = font.render(f"Episode: {episode} / {EPISODES}", True, TEXT_COLOR)
    stat_text = font.render(status_text, True, TEXT_COLOR)
    screen.blit(ep_text, (PADDING, HEIGHT - 40))
    screen.blit(stat_text, (WIDTH // 2, HEIGHT - 40))


def step_env(y, x, action):
    """Calculates the next state given current state and action."""
    dy, dx = go[action]
    ny, nx = y + dy, x + dx

    # Check boundaries
    if 0 <= ny < ROWS and 0 <= nx < COLS:
        if MAZE[ny][nx] != '#':
            return ny, nx
    return y, x  # Hit a wall or boundary, stay in place


# --- 4. MAIN GAME LOOP ---
def main():
    print("Training started. Close the Pygame window to stop.")

    for game in range(EPISODES):
        y, x = 0, 0  # Reset to Start
        steps = 0
        max_steps = 200  # Prevent infinite loops early on
        done = False

        while not done and steps < max_steps:
            # Handle Pygame events so window doesn't freeze
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # --- RL LOGIC ---
            # Epsilon-Greedy Action Selection
            if np.random.rand() < EPSILON:
                a = np.random.randint(4)  # Explore
            else:
                a = Q[y, x].argmax()  # Exploit (use learned knowledge)

            # Take action
            ny, nx = step_env(y, x, a)

            # Get Reward
            if MAZE[ny][nx] == 'G':
                reward = 100
                done = True
            elif (ny, nx) == (y, x):  # Hit a wall
                reward = -10
            else:
                reward = -1  # Small penalty for every step to encourage shortest path

            # Q-Learning Update Rule (Bellman Equation)
            # Q(s,a) = Q(s,a) + alpha * [reward + gamma * max(Q(s',a')) - Q(s,a)]
            best_next_q = Q[ny, nx].max()
            Q[y, x, a] = Q[y, x, a] + ALPHA * (reward + GAMMA * best_next_q - Q[y, x, a])

            # Move agent
            y, x = ny, nx
            steps += 1

            # --- VISUALIZATION ---
            draw_maze((y, x), game + 1, f"Steps: {steps}")
            pygame.display.flip()

            # Control simulation speed (higher = slower)
            clock.tick(60)

            # Pause briefly at the start of a new game so you can see the reset
            if steps == 1:
                time.sleep(0.2)

            # --- NEW CHECK: STOP WHEN GOAL IS REACHED ---
            if MAZE[y][x] == 'G':
                print(f"Goal reached in episode {game + 1} with {steps} steps!")
                # Optional: pause for a moment so you can see the agent on the goal
                time.sleep(5.0)
                pygame.quit()
                sys.exit()  # This exits the entire program immediately

    # Keep window open when finished
    print("Training complete!")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        draw_maze((y, x), EPISODES, "Finished!")
        pygame.display.flip()
        clock.tick(10)


if __name__ == "__main__":
    main()