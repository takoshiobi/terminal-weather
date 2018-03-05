from colors import *
import sys
import requests
from collections import namedtuple

def kelvin_to_celsius(temp):
    """
    Convert Kelvin to Celsius
    :param temp: temperature in Kelvin
    :type temp: float
    :return: temperature in Celsius 
    :rtype: int
    """
    return int(temp - 273.15)

def set_icon(main):
    """
    Set weather icon
    :param main: weather status
    :type main: str
    :return: icon
    :rtype: str
    """
    data = {'Clear': '☀', 'Clouds': '☁', 'Rain': '☂', 'Snow': '❄', 'Thunderstorm': '☈', 'Drizzle': '☃', 'Extreme': '⚠'}
    try:
        return data[main]
    except KeyError:
        return ''

def display_weather(city):
    """
    Convert json file to classic dict
    :param city: city
    :type city: str
    :return: json output for selected city
    :rtype: dict
    """
    link = 'http://api.openweathermap.org/data/2.5/weather?q='+city+'&APPID=8d76659e3f514c793ad5a7efba3feaea'
    r = requests.get(link)
    d = r.json()
    if d["cod"] != "404":
        return {"city" : d["name"], "country" : d["sys"]["country"], "long" : d["coord"]["lon"], "lat" : d["coord"]["lat"],
                   "wind speed" : d["wind"]["speed"], "wind deg" : d["wind"]["deg"], "clouds" : d["clouds"]["all"],
                   "main" : d["weather"][0]["main"], "temp" : kelvin_to_celsius(d["main"]["temp"]), "temp max" : d["main"]["temp_max"],
                   "temp min" : d["main"]["temp_min"], "pressure" : d["main"]["pressure"], "humidity" : d["main"]["humidity"]}
    else:
        return "City not found"
    
if __name__ == "__main__":
    argv = str(sys.argv[1])
    d = display_weather(argv)
    if d != "City not found":
        print(REVERSE + CBEIGE + "CURRENT WEATHER ".center(80) + '\x1b[0m')
        print(CWHITE2 + "[" + CEND + "City: " + REVERSE + BLUE2 + argv + CEND + CWHITE2 + "]" + CEND + CBLUE + "           Longitude: " + CEND + CGREEN2 + str(d["long"]) + CEND)
        print(CWHITE2 + "[" + CEND + "Country: " + REVERSE + BLUE2 + d["country"] + CEND + CWHITE2 + "]" + CEND + CBLUE + "           Latitude: " + CEND + CGREEN2 + str(d["lat"]) + CEND)
        print("Temperature: " + CRED2 + str(d["temp"]) + "°C " + CEND + CYELLOW + set_icon(d["main"]) + CEND)
        print(" ")

        def table(rows):
          if len(rows) > 1:
            headers = rows[0]._fields
            lens = []
            for i in range(len(rows[0])):
              lens.append(len(max([x[i] for x in rows] + [headers[i]],key=lambda x:len(str(x)))))
            formats = []
            hformats = []
            for i in range(len(rows[0])):
              if isinstance(rows[0][i], int):
                formats.append("%%%dd" % lens[i])
              else:
                formats.append("%%-%ds" % lens[i])
              hformats.append("%%-%ds" % lens[i])
            pattern = " | ".join(formats)
            hpattern = " | ".join(hformats)
            separator = "-+-".join(['-' * n for n in lens])
            print (CBEIGE + hpattern % tuple(headers) + CEND)
            print (separator)
            _u = lambda t: t if isinstance(t, str) else t
            for line in rows:
                print (pattern % tuple(_u(t) for t in line))
          elif len(rows) == 1:
            row = rows[0]
            hwidth = len(max(row._fields,key=lambda x: len(x)))
            for i in range(len(row)):
              print ("%*s = %s" % (hwidth,row._fields[i],row[i]))

        Row = namedtuple('Row',['Temperature','Wind','Cloudiness', 'Humidity', 'Pressure'])
        putdata1 = Row("current: " + str(d["temp"]) + "°C", "speed: " + str(d["wind speed"]) + " m/s", str(d["clouds"])+"%",
                       str(d["humidity"])+"%", str(d["pressure"])+" hPa")
        putdata2 = Row("max: " + str(kelvin_to_celsius(d["temp max"])) + "°C", "deg: " + str(d["wind deg"]), "/", "/", "/")
        putdata3 = Row("min: " + str(kelvin_to_celsius(d["temp min"])) + "°C", "/", "/", "/", "/")
                       
        table([putdata1, putdata2, putdata3])
    else:
        print(CRED2 + 'City not found' + CEND)
    
    
