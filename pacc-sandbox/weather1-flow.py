import httpx
from prefect import flow, task


@task()
def fetch_weather(lat: float, lon: float):
    base_url = "https://api.open-meteo.com/v1/forecast/"
    weather = httpx.get(
        base_url,
        params=dict(latitude=lat, longitude=lon, hourly="temperature_2m"),
    )
    most_recent_temp = float(weather.json()["hourly"]["temperature_2m"][0])
    print(f"Most recent temp C: {most_recent_temp} degrees")
    return most_recent_temp

@flow()
def run_weather_locations(locations):
    
    for key, value in locations.items():
        print(f"Getting weather for {key}")
        fetch_weather(value[0], value[1])
        

if __name__ == "__main__":
    # fetch_weather(38.9, -77.0)
    locations = {
        "New York, NY": [40.74823952552813, -73.9859382965308],
        "Moscow, ID": [46.73195031890992, -116.9986518440434],
        "Seattle, WA": [47.607388194451474, -122.31460634651638]
    }
    run_weather_locations(locations)
