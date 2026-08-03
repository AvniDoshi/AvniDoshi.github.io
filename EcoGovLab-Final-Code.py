import datetime as dt
import requests
from urllib.parse import quote
from matplotlib import pyplot as plt

##get the start and end dates of the data the user wants
start = input("Enter start date in YYYY-MM-DD format: ")
end = input("Enter end date in YYYY-MM-DD format: ")
##get the climate data for central valley (lat and lon)
climate_base = "https://climate-api.open-meteo.com/v1/climate?"
climatecv_url = climate_base + "latitude=37&longitude=-120.18&start_date=" + start + "&end_date=" + end + "&models=CMCC_CM2_VHR4&daily=temperature_2m_mean,precipitation_sum,soil_moisture_0_to_10cm_mean,wind_speed_10m_mean"
climatecv_response = requests.get(climatecv_url).json()
##get the air quality data for central valley (lat and lon)
air_base = "https://air-quality-api.open-meteo.com/v1/air-quality?"
##get data for church rock new mexico
climatecr_url = climate_base + "latitude=35.57&longitude=-108.61&start_date=" + start + "&end_date=" + end + "&models=CMCC_CM2_VHR4&daily=temperature_2m_mean,precipitation_sum,soil_moisture_0_to_10cm_mean,wind_speed_10m_mean"
climatecr_response = requests.get(climatecr_url).json()
##find start and end years and the year range for the dates given
start_year = int(start.split("-")[0])
end_year = int(end.split("-")[0])
years = end_year - start_year + 1
##assign data to lists
dates_climate = climatecv_response ['daily']['time']
temps_cv = climatecv_response['daily']['temperature_2m_mean']
precipitation_cv = climatecv_response['daily']['precipitation_sum']
soil_cv = climatecv_response['daily']['soil_moisture_0_to_10cm_mean']
wind_cv = climatecv_response['daily']['wind_speed_10m_mean']
temps_cr = climatecr_response['daily']['temperature_2m_mean']
precipitation_cr = climatecv_response['daily']['precipitation_sum']
soil_cr = climatecr_response['daily']['soil_moisture_0_to_10cm_mean']
wind_cr = climatecr_response['daily']['wind_speed_10m_mean']
##only do the air ones if it exists
if start_year >= 2013:
    # get air quality data
    aircv_url = air_base + "latitude=37&longitude=-120.18&start_date=" + start + "&end_date=" + end + "&hourly=pm2_5,carbon_monoxide,aerosol_optical_depth"
    aircr_url = air_base + "latitude=35.57&longitude=-108.61&start_date=" + start + "&end_date=" + end + "&hourly=pm2_5,carbon_monoxide,aerosol_optical_depth"
    aircv_response = requests.get(aircv_url).json()
    aircr_response = requests.get(aircr_url).json()
    dates_air = aircv_response ['hourly']['time']
    pm_cv = aircv_response['hourly']['pm2_5']
    monoxide_cv = aircv_response['hourly']['carbon_monoxide'] 
    aerosol_cv = aircv_response['hourly']['aerosol_optical_depth'] 
    pm_cr = aircr_response['hourly']['pm2_5']
    monoxide_cr = aircr_response['hourly']['carbon_monoxide']
    aerosol_cr = aircr_response['hourly']['aerosol_optical_depth']
else:
    print("Air quality data only available from 2013 onward. Skipping air quality fetch.")
    aircv_response = {}
    aircr_response = {}

##function where user can get any data point they need
##only works for climate data (bc in days not hours)
def get_data():
    #get the users desired date for obtaining information
    date = input("What date would you like to gather climate data for? (YYYY-MM-DD format): ")
    ##check it is a valid date and assign index
    if date in dates_climate:
        index = dates_climate.index(date)
    else:
        print("Invalid date")
        return
    ##ask for location
    location = input("Would you like data for Central Valley (cv) or Church Rock (cr)?: ")
    ##returnn data
    if location.lower() == "cv":
        temp = temps_cv[index]
        precip = precipitation_cr[index]
        soil = soil_cv[index]
        location = "Central Valley, California"
    elif location.lower() == "cr":
        temp = temps_cr[index]
        precip = precipitation_cr[index]
        soil = soil_cr[index]
        location = "Church Rock, New Mexico"
    else:
        print("Invalid location")
        return
    print(f"On {date} in {location} the average temperature is {temp}°C, the precipitation sum is {precip} mm and the mean soil moisture fraction within 0-10 cm is {soil} m³/m³.")

##function where user can get any data list they need
##only works for climate data (bc in days not hours)
def get_data_list():
    date1 = input("Please enter start of date range (YYYY-MM-DD format): ")
    date2 = input("Please enter end of date range (YYYY-MM-DD format): ")
    index1 = dates_climate.index(date1)
    index2 = dates_climate.index(date2)
    ##ask for location
    location = input("Would you like data for Central Valley (cv) or Church Rock (cr)?: ")
    temp_list = []
    precip_list = []
    soil_list = []
    if location.lower() == "cv":
        for i in range (index1, (index2+1)):
            temp_list.append(temps_cv[i])
            precip_list.append(precipitation_cv[i])
            soil_list.append(soil_cv[i])
    if location.lower() == "cr":
        for i in range (index1, (index2+1)):
            temps_list.append(temps_cr[i])
            precip_list.append(precipitation_cr[i])
            soil_list.append(soil_cr[i])
    print("Temperatures: ", temp_list, "Precipitation data: ", precip_list, "Soil Moisture data: ", soil_list)

##function that allows user to graph any of the data they want by inputing the necessary parameters
##type_name = data type they are graphing
##date_type = air quality or climate
def graph_data(type_name, data_list, unit, location_name, data_type):
    plt.figure()

    if data_type.lower() == "air quality":
        index = [i for i in range(len(aircv_response['hourly']['time']))]
        x_label = f"Number of Hours from {aircv_response['hourly']['time'][0]} to {aircv_response['hourly']['time'][-1]}"
    else:  # climate
        index = [i for i in range(len(climatecv_response['daily']['time']))]
        x_label = f"Number of Days from {climatecv_response['daily']['time'][0]} to {climatecv_response['daily']['time'][-1]}"

    plt.scatter(index, data_list)
    title = f"{type_name} in a {str(years)} Year Period in {location_name}"
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(f"{type_name} ({unit})")
    plt.tight_layout()
    plt.show()

##graphs yearly averages for the data
def graph_year(type_name, data_list, unit, location_name, data_type):
    # Use pre-defined date lists
    if data_type.lower() == "air quality":
        dates_list = dates_air
    else:
        dates_list = dates_climate

    year_avg = []
    curr_sum = 0
    year_count = 0
    year_now = int(dates_list[0].split("-")[0])

    for i, curr in enumerate(data_list):
        curr_date = dates_list[i]
        curr_year = int(curr_date.split("-")[0])

        if curr is not None:
            if curr_year == year_now:
                curr_sum += float(curr)
                year_count += 1
            else:
                if year_count != 0:
                    year_avg.append(curr_sum / year_count)
                year_now = curr_year
                curr_sum = float(curr)
                year_count = 1

    if year_count != 0:
        year_avg.append(curr_sum / year_count)

    year_index = list(range(len(year_avg)))

    ##just dots option
    plt.figure()
    ##plt.scatter(year_index, year_avg)
    ##lines with dots option - more clear for trends
    plt.plot(year_index, year_avg, marker='o')
    title = f"{type_name} in a {years} Year Period in {location_name}"
    plt.title(title)
    plt.xlabel(f"Number of Years from {start} to {end}")
    plt.ylabel(f"{type_name} ({unit})")
    plt.tight_layout()
    plt.show()

##graphs monthly averages of data
def graph_month_avg(type_name, data_list, unit, location_name, data_type):
    # Select correct date list
    if data_type.lower() == "air quality":
        dates_list = dates_air
    else:
        dates_list = dates_climate

    # Initialize starting month and year
    current_year = int(dates_list[0].split("-")[0])
    current_month = int(dates_list[0].split("-")[1])

    month_avg = []
    curr_sum = 0
    month_count = 0

    for i, curr in enumerate(data_list):
        """
        ##uncomment this code if you are unsure when air quality data starts being collected
        ##it will print the first instance of data 
        if curr is not None:
            date = dates_air[i] if data_type == "air quality" else dates_climate[i]
            print(f"First data found at index {i}, {date}: {curr}")
            break  # stop after finding the first

        """
        curr_date = dates_list[i]
        year = int(curr_date.split("-")[0])
        month = int(curr_date.split("-")[1])

        if curr is not None:
            if year == current_year and month == current_month:
                curr_sum += float(curr)
                month_count += 1
            else:
                if month_count != 0:
                    month_avg.append(curr_sum / month_count)
                current_year = year
                current_month = month
                curr_sum = float(curr)
                month_count = 1

    if month_count != 0:
        month_avg.append(curr_sum / month_count)

    month_index = list(range(len(month_avg)))

    plt.figure()
    plt.scatter(month_index, month_avg)
    plt.title(f"{type_name} in a {years} Year Period in {location_name}")
    plt.xlabel(f"Number of Months from {start} to {end}")
    plt.ylabel(f"{type_name} ({unit})") 
    plt.tight_layout()
    plt.show()

graph_month_avg("Average Daily Precipitation", precipitation_cv, "mm", "Central Valley, California", "climate")

"""
graph_year("Average Yearly Temperature", temps_cv, "°C", "Central Valley, California", "climate")
graph_year("Average Daily  Precipitation", precipitation_cv, "mm", "Central Valley, California", "climate")


graph_month_avg("Average Wind Speed", wind_cv, "km/h", "Central Valley, California", "climate")
graph_month_avg("Average Wind Speed", wind_cr, "km/h", "Church Rock, New Mexico", "climate")
graph_year("Average Wind Speed", wind_cv, "km/h", "Central Valley, California", "climate")
graph_year("Average Wind Speed", wind_cr, "km/h", "Church Rock, New Mexico", "climate")
graph_month_avg("Carbon Monoxide", monoxide_cr, "μg/m³", "Church Rock, New Mexico", "air quality")
graph_year("Carbon Monoxide", monoxide_cr, "μg/m³", "Church Rock, New Mexico", "air quality")
graph_month_avg("Aerosol Optical Depth at 550 nm", aerosol_cr, "", "Church Rock, New Mexico", "air quality")
graph_year("Aerosol Optical Depth at 550 nm", aerosol_cr, "", "Church Rock, New Mexico", "air quality")
graph_month_avg("Particulate Matter Smaller than 2.5 µm", pm_cr, "μg/m³", "Church Rock, New Mexico", "air quality")
graph_year("Particulate Matter Smaller than 2.5 µm", pm_cr, "μg/m³", "Church Rock, New Mexico", "air quality")
"""
