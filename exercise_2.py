# Exercise 2 (Easy): Session State Practice
# Task**: Build a todo list app

# Requirements:
# 1. Text input for new todo
# 2. Add button
# 3. Display all todos
# 4. Clear all button
# 5. Use session state to persist todos

import streamlit as st

st.title('📝 Todo List')

# 1. Initialize session state (The Memory)
if 'todos' not in st.session_state:
    st.session_state.todos = []

# 2. Text input for new todo
new_todo = st.text_input("Enter a new task:")

# 3. Add button
if st.button("Add Task"):
    if new_todo.strip() != "": # Make sure it's not empty
        st.session_state.todos.append(new_todo)
    else:
        st.warning("Please type a task before adding.")

st.divider() # Just a visual line

# 4. Display all todos
st.subheader("Your Tasks:")
if not st.session_state.todos:
    st.write("No tasks yet. Add one above!")
else:
    for i, task in enumerate(st.session_state.todos):
        st.write(f"{i + 1}. {task}")

# 5. Clear all button
if st.button("Clear All Tasks"):
    st.session_state.todos = [] # Empty the list
    st.rerun() # Force the screen to refresh immediately