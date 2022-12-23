"""
Example taken from https://github.com/reyemb/streamlit-plotly-mapbox-events and updated with example from https://plotly.com/python/scattermapbox/ and https://github.com/andfanilo/social-media-tutorials/blob/master/20220914-crossfiltering/streamlit_app.py.

For this one, the original data-frame is filtered based on the plotly events and the orientation of the map is kept consistent (doesn't reset).

Run it via the below from the main project:

```
streamlit run examples/plotly_mapbox_events_carshare_consistent_map_layout.py
```

Exposes all the main plotly mapbox elements needed.
"""

from typing import Dict, Set

import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import streamlit as st
from streamlit_plotly_events import plotly_events


@st.experimental_singleton
def load_data() -> pd.DataFrame:
    return px.data.tips()


def initialize_state():
    """Initializes all filters and counter in Streamlit Session State"""
    if "bill_to_tip_query" not in st.session_state:
        st.session_state["bill_to_tip_query"] = set()

    if "counter" not in st.session_state:
        st.session_state.counter = 0


def reset_state_callback():
    """Resets all filters and increments counter in Streamlit Session State"""
    st.session_state.counter = 1 + st.session_state.counter
    st.session_state["bill_to_tip_query"] = set()


def query_data(df: pd.DataFrame) -> pd.DataFrame:
    """Apply filters in Streamlit Session State
    to filter the input DataFrame
    """
    df["bill_to_tip"] = (
        (100 * df["total_bill"]).astype(int).astype(str)
        + "-"
        + (100 * df["tip"]).astype(int).astype(str)
    )
    df["size_to_time"] = df["size"].astype(str) + "-" + df["time"].astype(str)
    df["selected"] = True

    if st.session_state["bill_to_tip_query"]:
        df.loc[
            ~df["bill_to_tip"].isin(st.session_state["bill_to_tip_query"]), "selected"
        ] = False

    return df


def build_bill_to_tip_figure(df: pd.DataFrame) -> go.Figure:
    fig = px.scatter(
        df,
        "total_bill",
        "tip",
        color="selected",
        color_discrete_sequence=["rgba(99, 110, 250, 0.2)", "rgba(99, 110, 250, 1)"],
        category_orders={"selected": [False, True]},
        hover_data=[
            "total_bill",
            "tip",
            "day",
        ],
        height=800,
    )
    fig.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF")
    fig.update_xaxes(gridwidth=0.1, gridcolor="#EDEDED")
    fig.update_yaxes(gridwidth=0.1, gridcolor="#EDEDED")
    return fig


def render_plotly_ui(transformed_df: pd.DataFrame) -> Dict:
    """Renders all Plotly figures.

    Returns a Dict of filter to set of row identifiers to keep, built from the
    click/select events from Plotly figures.

    The return will be then stored into Streamlit Session State next.
    """
    bill_to_tip_figure = build_bill_to_tip_figure(transformed_df)
    bill_to_tip_selected = plotly_events(
        bill_to_tip_figure,
        select_event=True,
        key=f"bill_to_tip_{st.session_state.counter}",
    )

    current_query = {}
    current_query["bill_to_tip_query"] = {
        f"{int(100*el['x'])}-{int(100*el['y'])}" for el in bill_to_tip_selected
    }

    return current_query


def update_state(current_query: Dict[str, Set]):
    """Stores input dict of filters into Streamlit Session State.

    If one of the input filters is different from previous value in Session State,
    rerun Streamlit to activate the filtering and plot updating with the new info in State.
    """
    rerun = False
    if current_query["bill_to_tip_query"] - st.session_state["bill_to_tip_query"]:
        st.session_state["bill_to_tip_query"] = current_query["bill_to_tip_query"]
        rerun = True

    if rerun:
        st.experimental_rerun()


def main():
    df = load_data()
    transformed_df = query_data(df)

    st.title("Plotly events")

    current_query = render_plotly_ui(transformed_df)

    update_state(current_query)

    st.button("Reset filters", on_click=reset_state_callback)


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    initialize_state()
    main()
