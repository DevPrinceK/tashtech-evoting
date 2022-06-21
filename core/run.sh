#!/bin/bash

# Starts both the Python and Webpack servers in the background.
# Both servers automatically shut down when there's an error.
python ./manage.py runserver & npm start