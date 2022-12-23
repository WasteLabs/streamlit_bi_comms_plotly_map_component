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
