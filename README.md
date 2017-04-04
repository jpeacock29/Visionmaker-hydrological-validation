New York City Engineers for a Sustainable World's (NYC-ESW) validation of the [Visionmaker](https://visionmaker.us/nyc/) environmental modeling system's hydrological model. See `./report` for full background.

-`.`
    - `make.sh` Download the source data and run the analysis in full (may take some time).
    - `README.md`: This README.
    - `Storm_parameters_figure.ipynb`: Equivalent `Storm_parameters_figure.r` but with embedded figures and nicer formatting.
    - `Storm_parameters_figure.r`: Plot information about the parameters of the Visionmaker hydrological model.
    - `Testing_flood_predictions.py`: Mine high-certainty flooding events from reports made to the 311 New York City help line.
    - `Testing_flood_predictions.ipynb`: Equivalent `Testing_flood_predictions.py` but with embedded figures and nicer formatting.
    - `Visionmaker_flood_predictions.csv`: The flooding events of `./ouputs/311_2015_floods.csv` with the corresponding predictions from Visionmaker.

- `./inputs/`:
    - `storm_modelling.csv`: The parameters used for modeling storms in Visionmaker.
    - (Other inputs are downloaded in `make.sh`.)

- `./outputs/`:
    - `311_2015_floods.csv`: Each row represents a flooding event found by `Testing_flood_predictions.*` and vital statistics for those flooding events.
    - `flood_events_and_reports_by_location.png`: The flood events plotted on top of the thousands of flood reports.
    - `flood_reports.png`: The number of flood reports made per day of 2015.
    - `n_floods_n_outliers_by_esp.png`: Performance of the clustering algorithm for mining flood events.
    - `results.csv`:  Brief table of vital statistics about the data used in `Testing_flood_predictions.*`
    - `storm_parameters.png`: Plot of data from `storm_modelling.csv`.
