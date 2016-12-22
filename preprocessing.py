import pandas as pd

def load_data():
    """
    Load 311 data, check how many rows have a value for which location
    columns and select only relevant columns
    """

    data = pd.read_csv('inputs/311_Service_Requests_from_2015.csv')

    # A fifth of these have no address, so the 1/10th with no latitude is probably as good as it gets.
    print('Fraction of reports with attribute')
    for col in ['Incident Address', 'Latitude', 'Longitude', 'Descriptor']:
        print(col + '\t' + str(data[col].isnull().mean()))

    select_cols = ['Unique Key', 'Created Date', 'Closed Date', 'Complaint Type',
                   'Descriptor', 'Latitude', 'Longitude']
    data[select_cols].to_csv(open(INPUT_PATH + '311_2015_short.csv', 'w'), index=False)


def filter_311(d):
    """
    We find that Complaint Types with descriptors containing "flood" can be either "Sewer",
    "Public Toilet" or some sort of lighting. By inspection, only Sewer is relevant.
    """

    flood_data = d[(d.Descriptor.fillna('').str.lower().str.contains('flood'))
                      & (d['Complaint Type'] == 'Sewer')
                      & (d.Latitude.notnull())]

    # clean up column names
    flood_data.columns = [col.lower().replace(' ', '_') for col in flood_data.columns]

    flood_data.created_date = pd.to_datetime(flood_data.created_date)

    flood_data.to_csv(INPUT_PATH + '311_2015_flooding.csv', index=False)


load_data()
data = pd.read_csv(INPUT_PATH + '311_2015_short.csv')
filter_311()
