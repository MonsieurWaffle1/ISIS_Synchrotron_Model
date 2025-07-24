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

def get_harmonic(pv_name: str, cycletime: str | float) -> float:
    """Return rows matching a specific CycleTime and PV value."""
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "..", "Collected_EPICS_data", "get_EPICS_Harmonics_full_cycle.dat")

    harmonic_data = pd.read_csv(csv_path)

    harmonic_index = harmonic_data["PV"].str.contains(f"DWTRIM::{pv_name}:AT_TIME:{cycletime}MS")
    return harmonic_data[harmonic_index]["Harmonic"].to_list()[0]

st.title("Tune GUI")


st.markdown(
    """ 
    This is the **set** tune
    """
)
#  DataFrame
df = getValues()

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

df = getValues()

# plotting set & actual tunes
fig = px.scatter(df,
    x="x", 
    y="y", 
    color="time", 
    symbol="type",
)
fig.update_layout(
    title="Set & Actual Tunes",
    xaxis_title='Qh',
    yaxis_title='Qv',
    legend=dict(x=0, y=1, traceorder='normal', orientation='h')
)

st.plotly_chart(fig)

st.title("Beta values table")

st.title("Enter time points")
with st.form(key="form"):
    time_point = st.number_input("Enter time point from -0.6 to 10 in increments of 0.5: ")
    submit_button=st.form_submit_button(label="submit")
    harmonic = st.checkbox("Apply harmonic effect")

    if submit_button:
        twiss_table = get_twiss_table(time_point, harmonic)

        fig = px.line(twiss_table, 
                     x ="s",
                     y = "betx",
                     labels={
                    "betx":"Beta X"
                     })
        st.plotly_chart(fig)
                    
 