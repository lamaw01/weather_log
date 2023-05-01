import mysql.connector
import requests
import json
import pandas
from datetime import datetime
from types import SimpleNamespace

from cdo_model import CdoModel


def request_api():
    try:
        result = requests.get('https://www.weatherlink.com/embeddablePage/getData/20581289a1894399b84bb774171f2848')
        print(result.status_code)
        if(result.status_code == 200):
            data = result.text
            jsonData = result.json()
            x = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
            model = CdoModel(
                windDirection = x.windDirection,
                timeZoneId = x.timeZoneId,
                timeFormat = x.timeFormat,
                barometerUnits = x.barometerUnits,
                windUnits = x.windUnits,
                rainUnits = x.rainUnits,
                tempUnits = x.tempUnits,
                temperatureFeelLike = x.temperatureFeelLike,
                temperature = x.temperature,
                hiTemp = x.hiTemp,
                hiTempDate = x.hiTempDate,
                loTemp = x.loTemp,
                loTempDate = x.loTempDate,
                wind = x.wind,
                gust = x.gust,
                gustAt = x.gustAt,
                humidity = x.humidity,
                rain = x.rain,
                seasonalRain = x.seasonalRain,
                barometer = x.barometer,
                barometerTrend = x.barometerTrend,
                lastReceived = x.lastReceived,
                systemLocation = x.systemLocation,
                forecastOverview = x.forecastOverview)
            insert_log(model,jsonData)
    except Exception as e:
        print(e)

def insert_log(cdoModel: CdoModel, jsonData):
   try:
      forecastData = json.dumps(jsonData["forecastOverview"])
      lastReceived=pandas.to_datetime(cdoModel.lastReceived,unit='ms')
      hiTempDate=pandas.to_datetime(cdoModel.hiTempDate,unit='ms')
      loTempDate=pandas.to_datetime(cdoModel.loTempDate,unit='ms')
      gustAt=pandas.to_datetime(cdoModel.gustAt,unit='ms')
     
      #connect db
      mydb = mysql.connector.connect(
         host="172.21.3.25",
         database="autocctv",
         user="autocctv",
         password="autocctv123"
      )
      cursor = mydb.cursor()
      #insert query
      sql = "INSERT INTO cdo_weather_logs (windDirection,timeFormat,barometerUnits,windUnits,rainUnits,tempUnits,temperatureFeelLike,temperature,hiTemp,hiTempDate,loTemp,loTempDate,wind,gust,gustAt,humidity,rain,seasonalRain,barometer,barometerTrend,lastReceived,systemLocation,forecastOverview) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
      val = (cdoModel.windDirection,cdoModel.timeFormat,cdoModel.barometerUnits,cdoModel.windUnits,cdoModel.rainUnits,cdoModel.tempUnits,cdoModel.temperatureFeelLike,cdoModel.temperature,cdoModel.hiTemp,hiTempDate,cdoModel.loTemp,loTempDate,cdoModel.wind,cdoModel.gust,gustAt,cdoModel.humidity,cdoModel.rain,cdoModel.seasonalRain,cdoModel.barometer,cdoModel.barometerTrend,lastReceived,cdoModel.systemLocation,forecastData)
      cursor.execute(sql, val)
      mydb.commit()
      print(cursor.rowcount, "record inserted.")
      cursor.close()
      mydb.close()
   except mysql.connector.Error as err:
      print('insert_log',err)


request_api()