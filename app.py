import streamlit as st
import random
import time

# --- INITIAL SETUP ---
st.set_page_config(page_title="Streamlit Snake", layout="centered")
st.title("🐍 Streamlit Snake Game")

# Game constants
GRID_SIZE = 15
DELAY = 0.2  # Speed of the game in seconds

# Initialize Session State
if 'snake' not in st.session_state:
    st.session_state.snake = [(5, 5), (5, 4), (5, 3)]
    st.session_state.direction = 'RIGHT'
    st.session_state.food = (10, 10)
    st.session_state.score = 0
    st.session_state.game_over = False

def reset_game():
    st.session_state.snake = [(5, 5), (5, 4), (5, 3)]
    st.session_state.direction = 'RIGHT'
    st.session_state.score = 0
    st.session_state.game_over = False

# --- INPUT HANDLING ---
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("⬆️"): st.session_state.direction = 'UP'
with col1:
    if st.button("⬅️"): st.session_state.direction = 'LEFT'
with col3:
    if st.button("➡️"): st.session_state.direction = 'RIGHT'
with col2:
    if st.button("⬇️"): st.session_state.direction = 'DOWN'

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
        # Food Check
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

# Visual output
game_display = "\n".join(["".join(row) for row in grid])
st.text(game_display)
st.write(f"### Score: {st.session_state.score}")

if st.session_state.game_over:
    st.error("GAME OVER!")
    if st.button("Restart"):
        reset_game()
        st.rerun()
else:
    # Auto-refresh mechanism
    time.sleep(DELAY)
    st.rerun()
