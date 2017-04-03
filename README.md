New York City Engineers for a Sustainable World's (NYC-ESW) validation of the [Visionmaker](https://visionmaker.us/nyc/) environmental modeling system's hydrological model.


- `make.sh` Download the source data and run the analysis in full (may take some time)
- `README.md`: This README
- `requirements.txt`: Required python packages (installed automatically in make.sh)
- `Storm_parameters_figure.ipynb`: Equivalent `Storm_parameters_figure.r` but with embedded figures and nicer formatting
- `Storm_parameters_figure.r`: Plot information about the parameters of the hydrological model
- `Testing_flood_predictions.py`: Mine high-certainty flooding events from reports made to the 311 New York City help line
- `Testing_flood_predictions.ipynb`: `Testing_flood_predictions.py` but with embedded figures and nicer formatting
Visionmaker_modelling_results

./inputs:
311_2015_flood_reports.csv
311_Service_Requests_from_2015.csv
311_Service_Requests_from_2015_short.csv
storm_modelling.csv

- ./outputs:
    - `311_2015_floods.csv`: Each row represents a flooding event found by `Testing_flood_predictions.*` and vital statistics for those flooding events.
    - `flood_events_and_reports_by_location.png`
    - `flood_reports.png`
    - `n_floods_n_outliers_by_esp.png`
    - `results.csv`:  Brief table of vital statistics about the data used in `Testing_flood_predictions.*`
    - `storm_parameters.png`

- ./Visionmaker_modelling_results:
    - `Visionmaker_flood_predictions.csv`
    - `Visionmaker_storm_parameters.csv`
