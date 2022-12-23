"""
Example taken from https://github.com/reyemb/streamlit-plotly-mapbox-events and updated with example from https://plotly.com/python/scattermapbox/ and https://github.com/andfanilo/social-media-tutorials/blob/master/20220914-crossfiltering/streamlit_app.py.

For this one, the original data-frame is filtered based on the plotly events and the orientation of the map is kept consistent (doesn't reset).

Run it via the below from the main project:

```
streamlit run examples/plotly_mapbox_events_carshare_consistent_map_layout.py
```

Exposes all the main plotly mapbox elements needed.
"""

import plotly.express as px
import streamlit as st
from streamlit_plotly_mapbox_events import plotly_mapbox_events

st.set_page_config(layout="wide")

df = px.data.carshare()
df = df.assign(
    **{
        "id_lon-lat": lambda df: df["centroid_lon"].astype(str)
        + "-"
        + df["centroid_lat"].astype(str)
    },
    index=df.index,
)

mapbox = px.scatter_mapbox(
    df,
    lat="centroid_lat",
    lon="centroid_lon",
    color="peak_hour",
    hover_name="index",
    size="car_hours",
    color_continuous_scale=px.colors.cyclical.IceFire,
    size_max=15,
    zoom=11,
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

if mapbox_events[0]:
    st.write("POINT CLICKED")
    lat_lon_id = [f"{x['lon']}-{x['lat']}" for x in mapbox_events[0]]
    df_select = df.loc[df["id_lon-lat"].isin(lat_lon_id)]
    st.write(df_select)
else:
    st.empty()

if mapbox_events[1]:
    st.write("POINT SELECTED")
    lat_lon_id = [f"{x['lon']}-{x['lat']}" for x in mapbox_events[1]]
    df_select = df.loc[df["id_lon-lat"].isin(lat_lon_id)]
    st.write(df_select)
else:
    st.empty()

if mapbox_events[2]:
    st.write("POINT HOVERED")
    lat_lon_id = [f"{x['lon']}-{x['lat']}" for x in mapbox_events[2]]
    df_select = df.loc[df["id_lon-lat"].isin(lat_lon_id)]
    st.write(df_select)
else:
    st.empty()

if mapbox_events[3]:
    st.write("LAYOUT CHANGED")
    min_max_lat_lon = mapbox_events[3]["raw"]["mapbox._derived"]["coordinates"]
    min_lon = min_max_lat_lon[0][0]
    max_lon = min_max_lat_lon[1][0]
    min_lat = min_max_lat_lon[2][1]
    max_lat = min_max_lat_lon[0][1]
    assert min_lon <= max_lon
    assert min_lat <= max_lat
    selection_flag = (
        (df["centroid_lon"] >= min_lon)
        & (df["centroid_lon"] <= max_lon)
        & (df["centroid_lat"] >= min_lat)
        & (df["centroid_lat"] <= max_lat)
    )
    center = mapbox_events[3]["raw"]["mapbox.center"]
    zoom = mapbox_events[3]["raw"]["mapbox.zoom"]
    df_select = df.loc[selection_flag]
    st.write(df_select)


plot_name_holder_clicked = st.empty()
plot_name_holder_selected = st.empty()
plot_name_holder_hovered = st.empty()
plot_name_holder_relayout = st.empty()

plot_name_holder_clicked.write(f"Clicked Point: {mapbox_events[0]}")
plot_name_holder_selected.write(f"Selected Point: {mapbox_events[1]}")
plot_name_holder_hovered.write(f"Hovered Point: {mapbox_events[2]}")
plot_name_holder_relayout.write(f"Relayout: {mapbox_events[3]}")
