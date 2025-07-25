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
from plot_tune import *

st.title("Tune GUI")

def resonance_graph_plotter_plotly(qx, qy, qx_real, qy_real, cycle_times,
                                   savename=None, xlims=(4.0, 4.5), ylims=(3.5, 4.0)):
    cycle_times = np.array(cycle_times)
    unique_times = np.unique(cycle_times)

    # Map cycle time values to colors
    color_map = px.colors.sample_colorscale("Rainbow", [i / max(1, (len(unique_times) - 1)) for i in range(len(unique_times))])
    time_to_color = {t: color_map[i] for i, t in enumerate(unique_times)}
    colors = [time_to_color[t] for t in cycle_times]

    fig = go.Figure()

    # Resonance lines
    resonances = ResonanceLinesPlotly((4., 5.), (3., 4.), (1, 2, 3, 4), 10)
    for line in resonances.get_resonance_lines():
        fig.add_trace(go.Scatter(
            x=line['x'], y=line['y'],
            mode='lines',
            line=dict(color=line['color'], dash=line['dash'], width=line['width']),
            showlegend=False
        ))

    # Main Qx/Qy (Settings)
    fig.add_trace(go.Scatter(
        x=qx, y=qy,
        mode='markers+lines',
        marker=dict(color=colors, size=8, symbol='circle'),
        line=dict(dash='dot', width=1, color='gray'),
        name='Settings'
    ))

    # Optional Machine values
    if qx_real is not None and qy_real is not None:
        real_colors = [time_to_color[t] for t in cycle_times]
        fig.add_trace(go.Scatter(
            x=qx_real, y=qy_real,
            mode='markers+lines',
            marker=dict(color=real_colors, size=10, symbol='cross'),
            line=dict(dash='dash', width=1, color='gray'),
            name='Machine'
        ))

    # Dummy scatter to generate colorbar
    fig.add_trace(go.Scatter(
        x=qx, y=qy,
        mode='markers',
        marker=dict(
            color=cycle_times,
            colorscale='Rainbow',
            size=0.1,
            colorbar=dict(
                title="Time (ms)",
                tickvals=unique_times,
                ticktext=[str(t) for t in unique_times]
            )
        ),
        showlegend=False
    ))

    # Layout
    fig.update_layout(
        title="ISIS Synchrotron Q Program",
        xaxis=dict(title='Qx', range=xlims),
        yaxis=dict(title='Qy', range=ylims),
        width=800,
        height=600,
        plot_bgcolor='white',
        legend=dict(x=0.7, y=1)
    )

    st.plotly_chart(fig)

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

#RESONANCE GRAPH
time_array = np.array([-0.1, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 7.0, 8.0, 9.0, 10.0])
output_df = getValuesRaw()
resonance_graph_plotter_plotly(output_df['Qh'], output_df['Qv'], output_df['Machine Qh'], output_df['Machine Qv'], time_array)

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
    time_point = st.slider("Enter a time point: ",
                           min_value=0.0,
                           max_value=10.0,
                           value = 1.0,
                           step=0.5)
    
    submit_button=st.form_submit_button(label="submit")
    harmonic = st.checkbox("Apply harmonic effect")

    if submit_button:
        twiss_table = get_twiss_table(time_point, harmonic)
        twiss_long = twiss_table.melt(id_vars='s', value_vars=['betx', 'bety'],
                               var_name='beta_type', value_name='beta_value')
        st.write(twiss_table.head())
        
        fig = px.line(
            twiss_long,
            x='s',
            y='beta_value',
            color='beta_type',
            title="Beta graph (betx in red, bety in blue)",
            color_discrete_map={
                'betx': 'red',
                'bety': 'blue'
            }
        )
        st.plotly_chart(fig)
