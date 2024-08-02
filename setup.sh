#!/bin/sh

# Create the .streamlit directory if it doesn't exist
mkdir -p /app/.streamlit

# Create the config.toml file
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > /app/.streamlit/config.toml
