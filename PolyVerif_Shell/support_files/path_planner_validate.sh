#!/bin/bash

echo "Start AD Path Planner Validation "

gnome-terminal --tab --title="Path Planner Validation" --command="bash -c 'cd ../PolyVerif_Shell; python3 pathPlannerCalculation/pathPlannerValidation.py; echo Report Generated > ../Poly_Suite/logfiles/logInfo.txt; $SHELL'"



