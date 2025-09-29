

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import datetime
from fix_month_case import fix_month_case

def clean_date(date_str):
    date_str = str(date_str)
    # Strip weekday name and extra spaces
    parts = date_str.split()
    if len(parts) == 2:
        date_only = parts[1]
        return fix_month_case(date_only)
    elif len(parts) == 3:
        date_only = parts[1] + "-" + parts[2]
        return fix_month_case(date_only)
    else:
        
        return date_str 
    

# Example usage


def get_flightaware_info(flight_number):
    options = Options()
    options.add_argument("--headless")  # runs browser invisibly
    driver = webdriver.Chrome(options=options)

    try:
        url = f"https://flightaware.com/live/flight/{flight_number}"
        driver.get(url)

        all_future_data = driver.find_elements(By.CSS_SELECTOR, ".flightPageDataTable")
        origin = driver.find_element(By.CSS_SELECTOR, ".flightPageSummaryOrigin").text
        destination = driver.find_element(By.CSS_SELECTOR, ".flightPageSummaryDestination").text

        # fix these three
        departure_time = driver.find_element(By.CSS_SELECTOR, ".flightPageSummaryDeparture").text
        arrival_time = driver.find_element(By.CSS_SELECTOR, ".flightPageSummaryArrival").text
        date = driver.find_element(By.CSS_SELECTOR, ".flightPageSummaryDepartureDay").text
        #_________________________________________________________________________________

        future_text = ''
        for i in range(len(all_future_data)):
            future_text+=all_future_data[i].text
        
        current_data = [{
            "flight_number": flight_number,
            'date': clean_date(date),
            'departure_time': departure_time.split("\n")[0],
            'origin': origin[:3],
            'arrival_time': arrival_time.split("\n")[0],
            'destination': destination[:3]
        }]
        future_data = extract_flights_from_text(flight_number, future_text)

        return current_data + future_data
            

    finally:
        driver.quit()
def extract_flights_from_text(flight_number, text, max_flights=2):
    #print(text)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    
    flights = []
    i = 0
    header_seen = False

    while i < len(lines):
        line = lines[i]

        # Wait until we hit the start of the first table
        if not header_seen:
            if "Date" in line:
                header_seen = True
                
            i += 1
            continue

        # Break if we hit a second header
        if "Date" in line and header_seen and i!=1:
            
            break

        # Extract 7 lines at a time (day, date, dep time, origin, arr time, destination, aircraft+duration)
        if i + 6 < len(lines):
            day_of_week = lines[i]
            date = lines[i + 1]
            departure_time = lines[i + 2]
            origin = lines[i + 3]
            arrival_time = lines[i + 4]
            destination = lines[i + 5]

            flight = {
                "flight_number": flight_number,
                "date": date,
                "departure_time": departure_time,
                "origin": origin[-3:],
                "arrival_time": arrival_time,
                "destination": destination[-3:],
            }

            flights.append(flight)

            if len(flights) >= max_flights:
                break

            i += 7
        else:
            break

    return flights

# print(get_flightaware_info('DAL786'))
