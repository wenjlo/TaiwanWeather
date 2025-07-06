import requests
import json
import pandas as pd
from config import TOKEN
from asset.MySQL import Mysql

def main():
    data = requests.get(
        f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0001-001?Authorization={TOKEN}&format=JSON")
    js_file = json.loads(data.text)
    columns_name = ['record_time', 'station_id', 'station_name', 'station_latitude', 'station_longitude',
                    'county_name', 'town_name', 'weather_description']
    df = pd.DataFrame(columns=columns_name)
    for js in js_file['records']['Station']:
        d = pd.DataFrame(
            [[pd.to_datetime(js['ObsTime']['DateTime']).tz_localize(None), js['StationId'], js['StationName'],
              js['GeoInfo']['Coordinates'][0]['StationLatitude'], js['GeoInfo']['Coordinates'][0]['StationLongitude'],
              js['GeoInfo']['CountyName'], js['GeoInfo']['TownName'], js['WeatherElement']['Weather']]],
            columns=columns_name)
        df = pd.concat([df, d], axis=0)

    mysql = Mysql()
    mysql.write(df, 'station_weather_data', 'weather')
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
