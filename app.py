import streamlit as st
import random
import time
from streamlit_shortcuts import add_shortcuts

st.set_page_config(page_title="2025 Snake", layout="centered")

# 1. Initialize State
if 'snake' not in st.session_state:
    st.session_state.update({
        'snake': [(5, 5), (5, 4), (5, 3)],
        'direction': 'RIGHT',
        'food': (10, 10),
        'score': 0,
        'game_over': False
    })

# 2. Movement Functions
def move(new_dir):
    # Prevent 180-degree turns into self
    opposites = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
    if new_dir != opposites.get(st.session_state.direction):
        st.session_state.direction = new_dir

# 3. Add Keyboard Shortcuts (Handles errors by wrapping in try-except)
try:
    add_shortcuts({
        'ArrowUp': lambda: move('UP'),
        'ArrowDown': lambda: move('DOWN'),
        'ArrowLeft': lambda: move('LEFT'),
        'ArrowRight': lambda: move('RIGHT'),
    })
except Exception:
    st.error("Keyboard library error. Ensure 'streamlit-shortcuts' is installed.")

# 4. Game Logic Loop
if not st.session_state.game_over:
    head_x, head_y = st.session_state.snake[0]
    
    if st.session_state.direction == 'UP': head_x -= 1
    elif st.session_state.direction == 'DOWN': head_x += 1
    elif st.session_state.direction == 'LEFT': head_y -= 1
    elif st.session_state.direction == 'RIGHT': head_y += 1

    new_head = (head_x, head_y)

    # Collision Check
    if (head_x < 0 or head_x >= 15 or head_y < 0 or head_y >= 15 or new_head in st.session_state.snake):
        st.session_state.game_over = True
    else:
        st.session_state.snake.insert(0, new_head)
        if new_head == st.session_state.food:
            st.session_state.score += 10
            st.session_state.food = (random.randint(0, 14), random.randint(0, 14))
        else:
            st.session_state.snake.pop()

# 5. Display
grid = [["⬜" for _ in range(15)] for _ in range(15)]
fx, fy = st.session_state.food
grid[fx][fy] = "🍎"
for x, y in st.session_state.snake:
    grid[x][y] = "🟩"

st.text("\n".join(["".join(row) for row in grid]))
st.write(f"Score: {st.session_state.score}")

if st.session_state.game_over:
    if st.button("Reset Game"):
        st.session_state.clear()
        st.rerun()
else:
    time.sleep(0.15)
    st.rerun()
