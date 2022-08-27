import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
from plotly import graph_objs as go
#from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(
    page_title="Mo Suraksha",
    page_icon="👋",
)

st.title("MO SURAKSHA")

if "my_input" not in st.session_state:
    st.session_state["my_input"] = ""

my_input = st.text_input("Input a text here", st.session_state["my_input"])
submit = st.button("Submit")
if submit:
    st.write(f"Hello {my_input}, how are you doing today?")
st.image("health.jpg", width=200)
st.write("!!! Welcome to MO SURAKSHA !!!")

col1, col2, col3 = st.beta_columns([1,6,1])

# with col1:
# st.write("")

# with col2:
# st.image("")

# with col3:
# st.write("health.jpg",width =200)

