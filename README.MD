# Streamlit bi-communication plotly map component

The goal is to be able to select elements on a map, and then access the selected elements in streamlit.
And also to update elements on a map, based on events that happened in streamlit.

For example:

1. Select points on a map, with points coloured by a category variable.
2. View the selected points as a table.
3. Change catagory value of all the selected points.
4. Update the color of the points on the map.

The closest existing component found for the above is:

1. <https://github.com/null-jones/streamlit-plotly-events>
2. <https://github.com/reyemb/streamlit-plotly-mapbox-events>

And a demo that shows plotly being used in this way:

1. <https://github.com/andfanilo/social-media-tutorials/blob/master/20220914-crossfiltering/streamlit_app.py> with a video here: <https://youtu.be/htXgwEXwmNs>

## Examples

### Basic plotly map select view returned results

Just basic illustration of interaction on the map and what is returned via the streamlit-plotly-mapbox-events component:

* `examples/plotly_mapbox_events_example.py`: original example with a bit of modication from <https://github.com/reyemb/streamlit-plotly-mapbox-events> [#4](https://github.com/WasteLabs/streamlit_bi_comms_plotly_map_component/issues/4)
* `examples/plotly_mapbox_events_carshare_example.py`: example above extended with example from <https://plotly.com/python/scattermapbox/> [#4](https://github.com/WasteLabs/streamlit_bi_comms_plotly_map_component/issues/4)

### Plotly map interaction data-frame filtering

Dataframes are filtered and displayed based on events returned from the streamlit-plotly-mapbox-events component.
It also includes filtering the data-frame based on the map viewpoint (when zooming and panning).
There is still a short-comming in that the map resets to its original viewpoint when events happen.

* `examples/plotly_mapbox_events_carshare_dataframe_filter.py`: extension of `examples/plotly_mapbox_events_carshare_example.py` [#6](https://github.com/WasteLabs/streamlit_bi_comms_plotly_map_component/issues/6)

## Note on poetry

To get it fully up and running in shell:

```
poetry shell
source $(poetry env info --path)/bin/activate
```
