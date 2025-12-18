import streamlit as st
import random
import time
from streamlit_shortcuts import add_shortcuts

# --- INITIAL SETUP ---
st.set_page_config(page_title="Keyboard Snake", layout="centered")
st.title("🐍 Keyboard-Controlled Snake")

# Game constants
GRID_SIZE = 15
DELAY = 0.15  # Slightly faster for better keyboard response

# Initialize Session State
if 'snake' not in st.session_state:
    st.session_state.snake = [(5, 5), (5, 4), (5, 3)]
    st.session_state.direction = 'RIGHT'
    st.session_state.food = (10, 10)
    st.session_state.score = 0
    st.session_state.game_over = False

# Define movement functions for shortcuts
def set_up(): st.session_state.direction = 'UP'
def set_down(): st.session_state.direction = 'DOWN'
def set_left(): st.session_state.direction = 'LEFT'
def set_right(): st.session_state.direction = 'RIGHT'

# --- KEYBOARD SHORTCUT BINDING ---
# These bind physical keys to the functions defined above
add_shortcuts({
    'ArrowUp': set_up,
    'ArrowDown': set_down,
    'ArrowLeft': set_left,
    'ArrowRight': set_right,
    'r': lambda: st.session_state.clear() # Shortcut to restart
})

# --- GAME LOGIC ---
if not st.session_state.game_over:
    head_x, head_y = st.session_state.snake[0]
    
    if st.session_state.direction == 'UP': head_x -= 1
    elif st.session_state.direction == 'DOWN': head_x += 1
    elif st.session_state.direction == 'LEFT': head_y -= 1
    elif st.session_state.direction == 'RIGHT': head_y += 1

    new_head = (head_x, head_y)

    # Collision Check
    if (head_x < 0 or head_x >= GRID_SIZE or 
        head_y < 0 or head_y >= GRID_SIZE or 
        new_head in st.session_state.snake):
        st.session_state.game_over = True
    else:
        st.session_state.snake.insert(0, new_head)
        if new_head == st.session_state.food:
            st.session_state.score += 10
            st.session_state.food = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
        else:
            st.session_state.snake.pop()

# --- RENDERING ---
grid = [["⬜" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
fx, fy = st.session_state.food
grid[fx][fy] = "🍎"
for x, y in st.session_state.snake:
    grid[x][y] = "🟩"

game_display = "\n".join(["".join(row) for row in grid])
st.text(game_display)
st.write(f"### Score: {st.session_state.score}")
st.caption("Use Arrow Keys to move • Press 'R' to restart")

if st.session_state.game_over:
    st.error("GAME OVER!")
    if st.button("Restart"):
        st.session_state.clear()
        st.rerun()
else:
    time.sleep(DELAY)
    st.rerun()
