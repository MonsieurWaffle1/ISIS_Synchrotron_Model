#### UI imports
import streamlit as st
import plotly.graph_objs as go
import plotly.express as px

#### Dataset and data manipulation imports
import pandas as pd
import seaborn as sns
import numpy as np

#### Importing data
from get_tune_values import *
from plot_tune_notebook import *

st.title("Tune GUI")


st.markdown(
    """ 
    This is the **set** tune
    """
)
#  DataFrame
df = getValues()

print(df)

set_df = df[df['type'] == 'set']

edited_df = st.data_editor(
    set_df,
    key="1",
    column_config={
    "type": None
    },
    use_container_width=True,
    num_rows="dynamic"
)

st.markdown(
    """ 
    Once we process the set tune, this is the **actual** tune
    """
)

actual_df = df[df['type'] == 'actual']

edited_df = st.data_editor(
    actual_df,
    key="2",
    column_config={
    "type": None
    },
    use_container_width=True,
    num_rows="dynamic"
)

################################### REPLACE CODE UNDER WITH TABLE
fig = px.scatter(df, 
                    x="x", 
                    y="y",
                    color="type",
                    labels={
                    "x":"Qx", 
                    "y":"Qy",
                    "type":"Type of tune", 
                    })
st.plotly_chart(fig)

###################################### beta table
st.title("Beta values table")

twiss_table = get_twiss_table()

fig = px.line(twiss_table, 
            x="s", 
            y="betx",
            labels={
            "betx":"Beta X"
            }
            )
st.plotly_chart(fig)