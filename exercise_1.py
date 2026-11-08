## Exercises

# Exercise 1 (Easy): Basic Streamlit App

#Task: Create a simple calculator app

##Requirements**:
#1. Two number inputs
#2. Operation selector (dropdown: +, -, *, /)
#3. Calculate button
#4. Display result

#Bonus**: Add error handling for division by zero

import streamlit as st

st.title('Simple Calculator')

#create two number inputs
# we use st.number_input so that the user can only input valid numbers

num1 = st.number_input('enter first number', value=0.0)
num2 = st.number_input('enter second number', value=0.0)

#create operation selector(dropdown)
operation = st.selectbox('Select operation', ['+', '-', '*', '/'])

#add calculate button
if st.button('calculate'):

#display result (and bonus: error handling)
    if operation == '+':
            result = num1 + num2
            st.success(f'Result: {result}')

    elif operation == '-':
            result = num1 - num2
            st.success(f'Result: {result}')

    elif operation == '*':
            result = num1 * num2
            st.success(f'Result: {result}')

    elif operation == '/':
            if num2 == 0:
                st.error("Error: Cannot divide by zero!.")
            else:
                  result = num1 / num2
            st.success(f'Result: {result}')

        