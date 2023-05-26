#!/bin/bash

python main.py &
rasa run actions &
rasa run --cors "*" --enable-api &
wait