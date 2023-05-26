#!/bin/bash

python main.py &
rasa run actions &
rasa run --enable-api --cors "*" &
wait