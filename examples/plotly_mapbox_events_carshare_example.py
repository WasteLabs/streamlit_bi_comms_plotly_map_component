"""
Example taken from https://github.com/reyemb/streamlit-plotly-mapbox-events and updated with example from https://plotly.com/python/scattermapbox/

Run it via the below from the main project:

```
streamlit run examples/plotly_mapbox_events_carshare_example.py
```

Exposes all the main plotly mapbox elements needed.
"""

import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_plotly_mapbox_events import plotly_mapbox_events

st.set_page_config(layout="wide")

df = px.data.carshare()
mapbox = px.scatter_mapbox(
    df,
    lat="centroid_lat",
    lon="centroid_lon",
    color="peak_hour",
    size="car_hours",
    color_continuous_scale=px.colors.cyclical.IceFire,
    size_max=15,
    zoom=10,
    height=700,
)
mapbox.update_layout(
    mapbox_style="carto-positron", margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=700
)

mapbox_events = plotly_mapbox_events(
    mapbox,
    click_event=True,
    select_event=True,
    hover_event=True,
    relayout_event=True,
    override_height=700,
    override_width="100%",
)

plot_name_holder_clicked = st.empty()
plot_name_holder_selected = st.empty()
plot_name_holder_hovered = st.empty()
plot_name_holder_relayout = st.empty()

plot_name_holder_clicked.write(f"Clicked Point: {mapbox_events[0]}")
plot_name_holder_selected.write(f"Selected Point: {mapbox_events[1]}")
plot_name_holder_hovered.write(f"Hovered Point: {mapbox_events[2]}")
plot_name_holder_relayout.write(f"Relayout: {mapbox_events[3]}")
