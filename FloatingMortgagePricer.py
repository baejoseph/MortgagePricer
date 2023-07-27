import numpy as np
import numpy_financial as npf

import streamlit as st

from InterestRates import InterestRates

def add_vertical_space(num_lines: int = 1):
    """Add vertical space to your Streamlit app."""
    for _ in range(num_lines):
        st.write("")


