# ref: https://stackoverflow.com/questions/24346872/python-equivalent-of-a-given-wget-command
import wget
import pandas as pd

# get metadata of datasets, had to be obtained manually
ids = ["BSC18CA12-01", "BSC00CA12-01", "BSC06CA12-01", "BSC12CA12-01"]
start_dates = ["20210304", "20210304", "20210304", "20210303"]
end_dates = ["20240627", "20240627", "20240627", "20240627"]
end_dates = ["20231016", "20240210", "20231016", "20231015"]

init_times = ["02", "08", "14", "20"]

for i in zip(start_dates, end_dates, ids, init_times):
    start_date = i[0]
    end_date = i[1]
    forecast_id = i[2]
    init_time = i[3]
    print("Get data for " + forecast_id + " from dates " + start_date + " to " + end_date + "; init_time is " + init_time)
    
    # generate dates of interest, which is all available data for each dataset
    # ref: https://stackoverflow.com/questions/59882714/python-generating-a-list-of-dates-between-two-dates
    dates = pd.date_range(start=start_date, end=end_date)
    dates = dates.strftime('%Y%m%d').tolist()

    # download datasets in specified dates
    for date in dates:
        # build URL string to download from and directory & filename to download to
        url = "https://firesmoke.ca/forecasts/" + forecast_id + "/" + date + init_time + "/dispersion.nc"
        directory = "/Users/arleth/Mount/firesmoke/" + forecast_id + "/dispersion_" + date + ".nc"
        wget.download(url, out=directory)
    
