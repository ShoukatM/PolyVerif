#!/bin/bash

echo "Start AD Localization Validation "

#gnome-terminal --tab --title="Control Validation" --command="bash -c 'cd ../Poly_Suite; python3 localizationCalculation/LocalizationValidation.py; echo Report Generated > ../Poly_Suite/logfiles/logInfo.txt; exit; $SHELL'"


gnome-terminal --tab --title="Localization Result" --command="bash -c 'python3 localizationCalculation/LocalizationValidation.py;$SHELL'"





echo $$>>pidFile.txt