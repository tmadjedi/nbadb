#!/bin/sh
# Run the build

echo "Creating tables..."
python dbinit/create_tables.py

echo "Source to stage 1 mappings..."
python mappings/src_stg1_boxscore.py

echo "Stage 1 to stage 2 mappings..."
python mappings/stg1_stg2_game_result.py
python mappings/stg1_stg2_team_boxscore.py

echo "Stage 2 to stage 2 mappings..."
python mappings/stg2_stg2_season_result.py