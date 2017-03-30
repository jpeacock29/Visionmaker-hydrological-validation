# Input data will be placed in inputs. Figures and sheets will be placed in outputs_1.
mkdir inputs outputs

# download the data from Open NYC
wget https://data.cityofnewyork.us/api/views/hemm-82xw/rows.csv?accessType=DOWNLOAD

# rename and move the downloaded file
mv rows.csv\?accessType\=DOWNLOAD inputs/311_Service_Requests_from_2015.csv

# install any needed packages
pip3 install -r requirements.txt

# run the analysis
echo "Warning: The analysis is memory intensive and may take a moment."
python3 Testing_flood_predictions.py
