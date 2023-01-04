"""
Example taken from https://github.com/reyemb/streamlit-plotly-mapbox-events and updated with example from https://plotly.com/python/scattermapbox/ and https://github.com/andfanilo/social-media-tutorials/blob/master/20220914-crossfiltering/streamlit_app.py.

The orientation of the map is kept consistent (doesn't reset) and items on the map are higlighlited based on dataframe selections.

Run it via the below from the main project:

```
streamlit run examples/plotly_mapbox_events_carshare_consistent_map_dataframe_highligh.py
```

Note that this one requires aggrigrid.
"""

from typing import Dict, Set, Tuple

import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import streamlit as st
from st_aggrid import AgGrid, DataReturnMode, GridOptionsBuilder, GridUpdateMode
from streamlit_plotly_mapbox_events import plotly_mapbox_events

PLOTLY_HEIGHT = 500
LAT_COL = "centroid_lat"
LON_COL = "centroid_lon"

LAT_LON_QUERIES = [
    "lat_lon_click_query",
    "lat_lon_select_query",
    "lat_lon_hover_query",
]
LAT_LON_QUERIES_ACTIVE = {
    "lat_lon_click_query": False,
    "lat_lon_select_query": False,
    "lat_lon_hover_query": False,
}

MAP_ZOOM = 11


@st.experimental_singleton
def load_data_map() -> pd.DataFrame:
    carshare_data = px.data.carshare()
    carshare_data = carshare_data.assign(selected=False, index=carshare_data.index)
    return carshare_data[
        ["index"] + carshare_data.drop(columns=["index"]).columns.tolist()
    ]


def initialize_state():
    """Initializes all filters and counter in Streamlit Session State"""
    for query in LAT_LON_QUERIES:
        if query not in st.session_state:
            st.session_state[query] = set()

    if "map_move_query" not in st.session_state:
        st.session_state.map_move_query = set()

    if "map_layout" not in st.session_state:
        st.session_state.map_layout = {}

    if "counter" not in st.session_state:
        st.session_state.counter = 0


def reset_state_callback():
    """Resets all filters and increments counter in Streamlit Session State"""
    st.session_state.counter += 1
    for query in LAT_LON_QUERIES:
        st.session_state[query] = set()
    st.session_state.map_move_query = set()
    st.session_state.map_layout = {}


def query_data_map(
    df: pd.DataFrame, df_selected: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Apply filters in Streamlit Session State
    to filter the input DataFrame
    """
    df = df.assign(
        **{
            "lon-lat__id": lambda df: df[LON_COL].astype(str)
            + "-"
            + df[LAT_COL].astype(str)
        },
        index=df.index,
    )
    if df_selected.shape[0] > 0:
        df.loc[df["index"].isin(df_selected["index"].values), "selected"] = True
    df_selected = df[df["selected"]]
    return df, df_selected


def build_map(df: pd.DataFrame) -> go.Figure:

    if st.session_state.map_layout:
        center = st.session_state.map_layout["center"]
        zoom = st.session_state.map_layout["zoom"]
    else:
        center = {"lat": df[LAT_COL].median(), "lon": df[LON_COL].median()}
        zoom = MAP_ZOOM

    fig = px.scatter_mapbox(
        df,
        lat=LAT_COL,
        lon=LON_COL,
        color="selected",
        color_discrete_sequence=["rgba(99, 110, 250, 0.2)", "rgba(99, 110, 250, 1)"],
        category_orders={"selected": [False, True]},
        hover_name="index",
        size="car_hours",
        color_continuous_scale=px.colors.cyclical.IceFire,
        size_max=15,
        zoom=zoom,
        center=center,
    )
    fig.update_layout(
        mapbox_style="carto-positron",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=PLOTLY_HEIGHT,
    )
    return fig


def render_plotly_map_ui(transformed_df: pd.DataFrame) -> Dict:
    """Renders all Plotly figures.

    Returns a Dict of filter to set of row identifiers to keep, built from the
    click/select events from Plotly figures.

    The return will be then stored into Streamlit Session State next.
    """
    fig = build_map(transformed_df)
    map_selected = plotly_mapbox_events(
        fig,
        click_event=LAT_LON_QUERIES_ACTIVE["lat_lon_click_query"],
        select_event=LAT_LON_QUERIES_ACTIVE["lat_lon_select_query"],
        hover_event=LAT_LON_QUERIES_ACTIVE["lat_lon_hover_query"],
        relayout_event=True,
        key=f"lat_lon_query{st.session_state.counter}",
        override_height=PLOTLY_HEIGHT,
        override_width="%100",
    )

    current_query = {}
    i = 0
    for query in LAT_LON_QUERIES:
        if LAT_LON_QUERIES_ACTIVE[query] is True:
            current_query[query] = {f"{x['lon']}-{x['lat']}" for x in map_selected[i]}
            i += 1
        else:
            current_query[query] = set()

    if map_selected[-1]:
        st.session_state.map_layout["center"] = map_selected[-1]["raw"]["mapbox.center"]
        st.session_state.map_layout["zoom"] = map_selected[-1]["zoom"]
        current_query["map_move_query"] = {
            map_selected[-1]["raw"]["mapbox.center"]["lat"],
            map_selected[-1]["raw"]["mapbox.center"]["lon"],
            map_selected[-1]["zoom"],
        }
    else:
        current_query["map_move_query"] = set()
    return current_query


def update_state(current_query: Dict[str, Set]):
    """Stores input dict of filters into Streamlit Session State.

    If one of the input filters is different from previous value in Session State,
    rerun Streamlit to activate the filtering and plot updating with the new info in State.
    """
    rerun = False
    for query in LAT_LON_QUERIES:
        if current_query[query] - st.session_state[query]:
            st.session_state[query] = current_query[query]
            rerun = True
    if current_query["map_move_query"] - st.session_state["map_move_query"]:
        st.session_state["map_move_query"] = current_query["map_move_query"]
        rerun = True

    if rerun:
        st.experimental_rerun()


def selection_dataframe(df):
    data = df
    gb = GridOptionsBuilder.from_dataframe(data)
    gb.configure_pagination(
        paginationAutoPageSize=False, paginationPageSize=data.shape[0]
    )  # Add pagination
    gb.configure_column("index", headerCheckboxSelection=True)
    gb.configure_side_bar()  # Add a sidebar
    gb.configure_selection(
        "multiple",
        use_checkbox=True,
        groupSelectsChildren="Group checkbox select children",
    )  # Enable multi-row selection
    gridOptions = gb.build()

    grid_response = AgGrid(
        data,
        gridOptions=gridOptions,
        data_return_mode="AS_INPUT",
        update_on="MODEL_CHANGED",
        columns_auto_size_mode="FIT_CONTENTS",
        fit_columns_on_grid_load=False,
        theme="streamlit",  # Add theme color to the table
        enable_enterprise_modules=True,
        height=350,
        width="100%",
        reload_data=False,
    )
    data = grid_response["data"]
    selected = grid_response["selected_rows"]
    df_selected = pd.DataFrame(selected).drop(
        columns=["_selectedRowNodeInfo"], errors="ignore"
    )  # Pass the selected rows to a new dataframe df
    return df_selected


def main():
    st.title("Plotly events")
    df_map = load_data_map()
    df_selected = selection_dataframe(df_map)
    tansformed_df_map, selected_df_map = query_data_map(df_map, df_selected)
    current_query = render_plotly_map_ui(tansformed_df_map)
    update_state(current_query)
    st.write(selected_df_map)
    st.button("Reset filters", on_click=reset_state_callback)


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    initialize_state()
    main()
