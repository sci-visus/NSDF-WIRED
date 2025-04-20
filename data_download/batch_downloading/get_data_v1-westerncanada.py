# ref: https://realpython.com/python-download-file-from-url/
import requests
import pandas as pd
import multiprocessing
import time
from datetime import datetime

# get metadata of datasets, had to be obtained manually
ids = ["BSC00WC04-01"]
start_dates = ["20210315"]
end_dates = ["20241021"]
# ref: https://www.freecodecamp.org/news/python-datetime-now-how-to-get-todays-date-and-time/
# ref: https://www.programiz.com/python-programming/datetime/strftime
# got data for up to 06-26-2024
today = datetime.now().strftime('%Y%m%d')
init_times = ["08"]

# create list of urls and directory tuples, indicating where to download from and to
queries = []

# try downloading all files starting the day after dataset's corresponding end date
for i in zip(start_dates, end_dates, ids, init_times):
    start_date = i[0]
    end_date = i[1]
    forecast_id = i[2]
    init_time = i[3]
    
    # generate dates of interest, which is all available data for each dataset
    # ref: https://stackoverflow.com/questions/59882714/python-generating-a-list-of-dates-between-two-dates
    dates = pd.date_range(start=start_date, end=end_date)
    dates = dates.strftime('%Y%m%d').tolist()

    # download datasets in specified dates
    for date in dates:
        # build URL string to download from and directory & filename to download to
        url = "https://firesmoke.ca/forecasts/" + forecast_id + "/" + date + init_time + "/dispersion.nc"
        directory = "/usr/sci/scratch_nvme/arleth/download/" + forecast_id + "/dispersion_" + date + ".nc"
        queries.append([url, directory])
        
def download_query(q):
    url = q[0]
    directory = q[1]
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

 # create frames, capturing issues 
with multiprocessing.Pool() as pool:
    # Start a timer to measure how long the conversion takes
    start_time = time.time()
    print('starting')
    issues = pool.map(download_query, queries)
    print('done!')
    # End the timer and print the elapsed time
    end_time = time.time()
    print(f'Total elapsed time: {end_time - start_time}')
