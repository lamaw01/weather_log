from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Afternoon:
    weatherCode: int
    weatherDesc: str
    weatherIconUrl: str
    temp: int
    chanceofrain: int
    rainInInches: int


@dataclass
class ForecastOverview:
    date: datetime
    morning: Afternoon
    afternoon: Afternoon
    evening: Afternoon
    night: Afternoon

@dataclass
class CdoModel:
    windDirection: int
    timeZoneId: str
    timeFormat: str
    barometerUnits: str
    windUnits: str
    rainUnits: str
    tempUnits: str
    temperatureFeelLike: int
    temperature: int
    hiTemp: int
    hiTempDate: int
    loTemp: int
    loTempDate: int
    wind: int
    gust: int
    gustAt: int
    humidity: int
    rain: str
    seasonalRain: str
    barometer: str
    barometerTrend: str
    lastReceived: int
    systemLocation: str
    forecastOverview: List[ForecastOverview]
