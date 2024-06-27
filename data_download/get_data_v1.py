# ref: https://realpython.com/python-download-file-from-url/
import requests
import pandas as pd
from datetime import datetime

# get metadata of datasets, had to be obtained manually
ids = ["BSC18CA12-01", "BSC00CA12-01", "BSC06CA12-01", "BSC12CA12-01"]
start_dates = ["20210304", "20210304", "20210304", "20210303"]
end_dates = ["20231016", "20240210", "20231016", "20231015"]
# ref: https://www.freecodecamp.org/news/python-datetime-now-how-to-get-todays-date-and-time/
# ref: https://www.programiz.com/python-programming/datetime/strftime
today = datetime.now().strftime('%Y%m%d')

init_times = ["02", "08", "14", "20"]

# try downloading all files starting the day after dataset's corresponding end date
for i in zip(end_dates, ids, init_times):
    end_date = i[0]
    forecast_id = i[1]
    init_time = i[2]
    print("Get data for " + forecast_id + " from dates " + end_date + " to " + today + "; init_time is " + init_time)
    
    # generate dates of interest, which is all available data for each dataset
    # ref: https://stackoverflow.com/questions/59882714/python-generating-a-list-of-dates-between-two-dates
    dates = pd.date_range(start=end_date, end=today)
    dates = dates.strftime('%Y%m%d').tolist()

    # download datasets in specified dates
    for date in dates:
        # build URL string to download from and directory & filename to download to
        url = "https://firesmoke.ca/forecasts/" + forecast_id + "/" + date + init_time + "/dispersion.nc"
        directory = "/usr/sci/scratch_nvme/arleth/basura_total/" + forecast_id + "/dispersion_" + date + ".nc"
        
        # request from download URL
        response = requests.get(url, stream=True)
        # get response header
        header = response.headers
        # download file if we see 'save as' content type
        # ref: https://stackoverflow.com/questions/20508788/do-i-need-content-type-application-octet-stream-for-file-download
        if 'Content-Type' in header and header['Content-Type'] == 'application/octet-stream':
            with open(directory, mode="wb") as file:
                file.write(response.content)
                print(f"Downloaded file {directory}")
        else: #otherwise inspect header's Content-Type
            print(header['Content-Type'])
        print('------')
