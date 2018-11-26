#!/usr/bin/python
import time
import random
import pyowm
import urllib2
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from datetime import datetime
from leagueoflegends import LeagueOfLegends, RiotError
from rgbmatrix import Adafruit_RGBmatrix

matrix = Adafruit_RGBmatrix(32,2)
degree_sign = u'\N{DEGREE SIGN}'
font7 = ImageFont.truetype(".DejaVuSans-Bold.ttf", 7)
font8 = ImageFont.truetype(".DejaVuSans-Bold.ttf", 8)
lol = LeagueOfLegends('RGAPI-b71a8fe2-804a-4d13-aab9-5ca9b9bca956')

try:
    owm = pyowm.OWM('5c50d5ab850e6a5ea0870a4794df3a9e')
    get_weather = owm.weather_at_id(5146277)
    curr_weather = get_weather.get_weather()
except pyowm.exceptions.api_call_error.APICallError:
    print('API Call Failed. Proceeding...')
    APIFailure = True
#A name dict for all degree measurements of wind to meteorological names (NNW) etc
WIND_DIRECTION_NAME_DICT = {0: 'N', 10: 'N', 20: 'NNE', 30: 'NNE', 40: 'NE',
                            50:'NE', 60:'NE', 70:'ENE', 80:'ENE', 90:'E',
                            100:'E', 110:'ESE', 120:'ESE', 130:'SE', 140:'SE',
                            150:'SE', 160:'SSE', 170:'SSE', 180:'S', 190:'S',
                            200:'SSW', 210:'SSW', 220:'SW', 230:'SW', 240:'SW',
                            250:'WSW', 260:'WSW', 270:'W', 280:'W', 290:'WNW',
                            300:'WNW', 310:'NW', 320:'NW', 330:'NW', 340:'NNW',
                            350:'NNW', 360:'N'}
def get_current_time():
    return str(datetime.now().time().strftime('%H:%M'))
def get_curr_weather_temp(owm):
    get_weather = owm.weather_at_id(5146277)
    curr_weather = get_weather.get_weather()
    return int(round(curr_weather.get_temperature('fahrenheit')['temp']))
def get_curr_weather_wind_speed(owm):
    get_weather = owm.weather_at_id(5146277)
    curr_weather = get_weather.get_weather()
    return int(round(curr_weather.get_wind()['speed'] * 2.23694))
def get_curr_weather_wind_direction(owm):
    get_weather = owm.weather_at_id(5146277)
    curr_weather = get_weather.get_weather()
    return int(round(curr_weather.get_wind()['deg'], -1))
def get_LeagueStats():
    try:
        summoner = lol.get_summoner_by_name("Finis Aeternum")
        print(summoner)
        return summoner
    except urllib2.URLError:
        print("League call failed. Proceeding...")
def getRandX():
    randx = random.randint(0,15)
    return randx
def getRandY():
    randy = random.randint(0,20)
    return randy
def displayTemperature(image, curr_weather_temp_int):
    """Adds temperature to the image supplied.

    Keyword arguments:
    image -- the image to add temperature string to
    curr_weather_temp_int -- the temperature value to add to the image
    """
    draw = ImageDraw.Draw(image)
    if curr_weather_temp_int >= 80:
        draw.text((0,19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="#EF3B09")
    elif curr_weather_temp_int >= 32 and curr_weather_temp_int < 80:
        draw.text((0,19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="#0DBA3E")
    else:
        draw.text((0,19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="42C5F4")
def displayOvercast(curr_weather_temp_int, wind_direction_name_dict):
    image_overcast_clouds = Image.new("RGB", (64,32))
    draw = ImageDraw.Draw(image_overcast_clouds)
    draw.text((0,3), get_current_time(), font=font8, fill="#FFFFFF")
    if curr_weather_temp_int >= 80:
        draw.text((0,19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="#EF3B09")
    elif curr_weather_temp_int >= 32 and curr_weather_temp_int < 80:
        draw.text((0,19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="#0DBA3E")
    else:
        draw.text((0,19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="42C5F4")
    draw.text((29,15), get_curr_weather_wind_speed(owm), font=font8, fill="#FFFFFF")
    draw.text((29,23), wind_direction_name_dict[get_curr_weather_wind_direction(owm)], font=font8, fill="#FFFFFF")
    #CLOUD 1
    draw.line((42,3,43,3), fill = "#FFFFFF")
    draw.line((40,4,45,4), fill = "#FFFFFF")
    draw.line((38,5,47,5), fill = "#FFFFFF")
    draw.line((37,6,48,6), fill = "#FFFFFF")
    draw.line((37,7,48,7), fill = "#FFFFFF")
    draw.line((38,8,47,8), fill = "#FFFFFF")
    draw.line((39,9,46,9), fill = "#FFFFFF")
    #CLOUD 2
    draw.line((53,6,54,6), fill = "#FFFFFF")
    draw.line((51,7,56,7), fill = "#FFFFFF")
    draw.line((49,8,58,8), fill = "#FFFFFF")
    draw.line((48,9,59,9), fill = "#FFFFFF")
    draw.line((48,10,59,10), fill = "#FFFFFF")
    draw.line((49,11,58,11), fill = "#FFFFFF")
    draw.line((50,12,57,12), fill = "#FFFFFF")
    #TINY CLOUD
    draw.line((51,2,52,2), fill = "#FFFFFF")
    draw.line((49,3,54,3), fill = "#FFFFFF")
    draw.line((50,4,53,4), fill = "#FFFFFF")
    matrix.SetImage(image_overcast_clouds.im.id, 0, 0)
    time.sleep(30)
    matrix.Clear()
def displayBroken(curr_weather_temp_int, wind_direction_name_dict):
    image_broken_clouds = Image.new("RGB", (64, 32))
    draw = ImageDraw.Draw(image_broken_clouds)
    draw.text((0,3), get_current_time(), font=font8, fill="#FFFFFF")
    if curr_weather_temp_int >= 80:
        draw.text((0,19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="#EF3B09")
    elif curr_weather_temp_int >= 32 and curr_weather_temp_int < 80:
        draw.text((0,19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="#0DBA3E")
    else:
        draw.text((0,19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="#42C5F4")
    draw.text((29,15), str(get_curr_weather_wind_speed(owm)) + "MPH", font=font8, fill="#FFFFFF")
    draw.text((29,23), wind_direction_name_dict[get_curr_weather_wind_direction(owm)], font=font8, fill="#FFFFFF")
    #SUN
    draw.ellipse(((41,1), (53,13)), fill = "#FFBB00")
    #CLOUD 1
    draw.line((42,3,43,3), fill = "#FFFFFF")
    draw.line((40,4,45,4), fill = "#FFFFFF")
    draw.line((38,5,47,5), fill = "#FFFFFF")
    draw.line((37,6,48,6), fill = "#FFFFFF")
    draw.line((37,7,48,7), fill = "#FFFFFF")
    draw.line((38,8,47,8), fill = "#FFFFFF")
    draw.line((39,9,46,9), fill = "#FFFFFF")
    #CLOUD 2
    draw.line((53,6,54,6), fill = "#FFFFFF")
    draw.line((51,7,56,7), fill = "#FFFFFF")
    draw.line((49,8,58,8), fill = "#FFFFFF")
    draw.line((48,9,59,9), fill = "#FFFFFF")
    draw.line((48,10,59,10), fill = "#FFFFFF")
    draw.line((49,11,58,11), fill = "#FFFFFF")
    draw.line((50,12,57,12), fill = "#FFFFFF")
    #TINY CLOUD
    draw.line((51,2,52,2), fill = "#FFFFFF")
    draw.line((49,3,54,3), fill = "#FFFFFF")
    draw.line((50,4,53,4), fill = "#FFFFFF")
    matrix.SetImage(image_broken_clouds.im.id, 0, 0)
    time.sleep(30)
    matrix.Clear()
def displayScattered(curr_weather_temp_int, wind_direction_name_dict):
    image_scattered_clouds = Image.new("RGB", (64,32))
    draw = ImageDraw.Draw(image_scattered_clouds)
    draw.text((0,3), get_current_time(), font=font8, fill="#FFFFFF")
    if curr_weather_temp_int >= 80:
        draw.text((0,19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="#EF3B09")
    elif curr_weather_temp_int >= 32 and curr_weather_temp_int < 80:
        draw.text((0,19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="#0DBA3E")
    else:
        draw.text((0,19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="42C5F4")
    draw.text((29,15), str(get_curr_weather_wind_speed(owm)) + "MPH", font=font8, fill="#FFFFFF")
    draw.text((29,23), wind_direction_name_dict[get_curr_weather_wind_direction(owm)], font=font8, fill="#FFFFFF")
    #SUN
    draw.ellipse(((41,1), (53,13)), fill = "#FFBB00")
    #CLOUD 1
    draw.line((42,3,43,3), fill = "#FFFFFF")
    draw.line((40,4,45,4), fill = "#FFFFFF")
    draw.line((38,5,47,5), fill = "#FFFFFF")
    draw.line((37,6,48,6), fill = "#FFFFFF")
    draw.line((37,7,48,7), fill = "#FFFFFF")
    draw.line((38,8,47,8), fill = "#FFFFFF")
    draw.line((39,9,46,9), fill = "#FFFFFF")
    #TINY CLOUD
    draw.line((51,2,52,2), fill = "#FFFFFF")
    draw.line((49,3,54,3), fill = "#FFFFFF")
    draw.line((50,4,53,4), fill = "#FFFFFF")
    matrix.SetImage(image_scattered_clouds.im.id, 0, 0)
    time.sleep(30)
    matrix.Clear()
def displayFew(curr_weather_temp_int, wind_direction_name_dict):
    image_few_clouds = Image.new("RGB", (64,32))
    draw = ImageDraw.Draw(image_few_clouds)
    draw.text((0,3), get_current_time(), font=font8, fill="#FFFFFF")
    if curr_weather_temp_int >= 80:
        draw.text((0,19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="#EF3B09")
    elif curr_weather_temp_int >= 32 and curr_weather_temp_int < 80:
        draw.text((0,19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="#0DBA3E")
    else:
        draw.text((0,19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="#42C5F4")
    draw.text((29,15), str(get_curr_weather_wind_speed(owm)) + "MPH", font=font8, fill="#FFFFFF")
    draw.text((29,23), wind_direction_name_dict[get_curr_weather_wind_direction(owm)], font=font8, fill="#FFFFFF")
    #SUN
    draw.ellipse(((41,1), (53,13)), fill = "#FFBB00")
    #TINY CLOUD
    draw.line((51,2,52,2), fill = "#FFFFFF")
    draw.line((49,3,54,3), fill = "#FFFFFF")
    draw.line((50,4,53,4), fill = "#FFFFFF")
    matrix.SetImage(image_few_clouds.im.id, 0, 0)
    time.sleep(30)
    matrix.Clear()
def displayClear(curr_weather_temp_int, wind_direction_name_dict):
    image_clear_sky = Image.new("RGB", (64,32))
    draw = ImageDraw.Draw(image_clear_sky)
    draw.text((0,3), get_current_time(), font=font8, fill="#FFFFFF")
    if curr_weather_temp_int >= 80:
        draw.text((0,19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="#EF3B09")
    elif curr_weather_temp_int >= 32 and curr_weather_temp_int < 80:
        draw.text((0,19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="#0DBA3E")
    else:
        draw.text((0,19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="#42C5F4")
    draw.text((29,15), str(get_curr_weather_wind_speed(owm)) + "MPH", font=font8, fill="#FFFFFF")
    draw.text((29,23), wind_direction_name_dict[get_curr_weather_wind_direction(owm)], font=font8, fill="#FFFFFF")
    draw.ellipse(((39,1), (51,13)), fill="#FFBB00")
    matrix.SetImage(image_clear_sky.im.id, 0, 0)
    time.sleep(30)
    matrix.Clear()
def displayThunderstorm(curr_weather_temp_int, wind_direction_name_dict):
    image_thunderstorm = Image.new("RGB", (64,32))
    draw = ImageDraw.Draw(image_thunderstorm)
    draw.text((0,3), get_current_time(), font=font8, fill="#FFFFFF")
    if curr_weather_temp_int >= 80:
        draw.text((0,19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="#EF3B09")
    elif curr_weather_temp_int >= 32 and curr_weather_temp_int < 80:
        draw.text((0,19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="#0DBA3E")
    else:
        draw.text((0,19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="#42C5F4")
    draw.text((29,15), str(get_curr_weather_wind_speed(owm)) + "MPH", font=font8, fill="#FFFFFF")
    draw.text((29,23), wind_direction_name_dict[get_curr_weather_wind_direction(owm)], font=font8, fill="#FFFFFF")
    #CLOUD 1
    draw.line((42,3,43,3), fill = "#BABABA")
    draw.line((40,4,45,4), fill = "#BABABA")
    draw.line((38,5,47,5), fill = "#BABABA")
    draw.line((37,6,48,6), fill = "#BABABA")
    draw.line((37,7,48,7), fill = "#BABABA")
    draw.line((38,8,47,8), fill = "#BABABA")
    draw.line((39,9,46,9), fill = "#BABABA")
    #TINY CLOUD 1
    draw.line((51,2,52,2), fill = "#FFFFFF")
    draw.line((49,3,54,3), fill = "#FFFFFF")
    draw.line((50,4,53,4), fill = "#FFFFFF")
    #TINY CLOUD 2
    draw.line((53,6,54,6), fill = "#FFFFFF")
    draw.line((51,7,56,7), fill = "#FFFFFF")
    draw.line((52,8,55,8), fill = "#FFFFFF")
    #LIGHTNING BOLT
    draw.line((42,10,44,10), fill = "#FFED11")
    draw.line((43,11,45,11), fill = "#FFED11")
    draw.line((44,11,45,11), fill = "#FFED11")
    draw.line((44,12,45,12), fill = "#FFED11")
    draw.line((45,13,46,13), fill = "#FFED11")
    #RAIN DROPS
    draw.line((51,5,52,5), fill = "#0078FF")
    draw.line((52,6,52,6), fill = "#0078FF")
    draw.line((52,9,52,10), fill = "#0078FF")
    draw.line((54,10,54,11), fill = "#0078FF")
    draw.line((55,9,55,9), fill = "#0078FF")
    matrix.SetImage(image_thunderstorm.im.id, 0, 0)
    time.sleep(30)
    matrix.Clear()
def displayRain(curr_weather_temp_int, wind_direction_name_dict):
    image_rain = Image.new("RGB", (64,32))
    draw = ImageDraw.Draw(image_rain)
    draw.text((0,3), get_current_time(), font=font8, fill="#FFFFFF")
    if curr_weather_temp_int >= 80:
        draw.text((0,19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="#EF3B09")
    elif curr_weather_temp_int >= 32 and curr_weather_temp_int < 80:
        draw.text((0,19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="#0DBA3E")
    else:
        draw.text((0,19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="#42C5F4")
    draw.text((29,15), str(get_curr_weather_wind_speed(owm)) + "MPH", font=font8, fill="#FFFFFF")
    draw.text((29,23), wind_direction_name_dict[get_curr_weather_wind_direction(owm)], font=font8, fill="#FFFFFF")
    #CLOUD 1
    draw.line((42,3,43,3), fill = "#BABABA")
    draw.line((40,4,45,4), fill = "#BABABA")
    draw.line((38,5,47,5), fill = "#BABABA")
    draw.line((37,6,48,6), fill = "#BABABA")
    draw.line((37,7,48,7), fill = "#BABABA")
    draw.line((38,8,47,8), fill = "#BABABA")
    draw.line((39,9,46,9), fill = "#BABABA")
    #TINY CLOUD 1
    draw.line((51,2,52,2), fill = "#FFFFFF")
    draw.line((49,3,54,3), fill = "#FFFFFF")
    draw.line((50,4,53,4), fill = "#FFFFFF")
    #TINY CLOUD 2
    draw.line((53,6,54,6), fill = "#FFFFFF")
    draw.line((51,7,56,7), fill = "#FFFFFF")
    draw.line((52,8,55,8), fill = "#FFFFFF")
    #RAIN DROPS
    draw.line((40,10,40,11), fill = "#0078FF")
    draw.line((43,10,43,12), fill = "#0078FF")
    draw.line((45,11,45,12), fill = "#0078FF")
    draw.line((41,12,41,12), fill = "#0078FF")
    draw.line((42,13,42,13), fill = "#0078FF")
    draw.line((44,13,44,13), fill = "#0078FF")
    draw.line((46,13,46,13), fill = "#0078FF")
    draw.line((46,10,46,10), fill = "#0078FF")
    draw.line((51,5,52,5), fill = "#0078FF")
    draw.line((52,6,52,6), fill = "#0078FF")
    draw.line((52,9,52,10), fill = "#0078FF")
    draw.line((54,10,54,11), fill = "#0078FF")
    draw.line((55,9,55,9), fill = "#0078FF")
    matrix.SetImage(image_rain.im.id, 0, 0)
    time.sleep(30)
    matrix.Clear()
def displaySnow(curr_weather_temp_int, wind_direction_name_dict):
    image_snow = Image.new("RGB", (64,32))
    draw = ImageDraw.Draw(image_snow)
    draw.text((0,3), get_current_time(), font=font8, fill="#FFFFFF")
    if curr_weather_temp_int >= 80:
        draw.text((0,19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="#EF3B09")
    elif curr_weather_temp_int >= 32 and curr_weather_temp_int < 80:
        draw.text((0,19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="#0DBA3E")
    else:
        draw.text((0,19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="#42C5F4")
    draw.text((29,15), str(get_curr_weather_wind_speed(owm)) + "MPH", font=font8, fill="#FFFFFF")
    draw.text((29,23), wind_direction_name_dict[get_curr_weather_wind_direction(owm)], font=font8, fill="#FFFFFF")
    #SNOWFLAKE 1
    draw.line((37,2,39,4), fill = "#FFFFFF")
    draw.line((37,4,39,2), fill = "#FFFFFF")
    #SNOWFLAKE 2
    draw.line((57,3,58,3), fill = "#FFFFFF")
    draw.line((56,4,56,4), fill = "#FFFFFF")
    draw.line((59,4,59,4), fill = "#FFFFFF")
    draw.line((57,5,58,5), fill = "#FFFFFF")
    #SNOWFLAKE 3
    draw.line((40,7,42,7), fill = "#FFFFFF")
    draw.line((41,6,41,8), fill = "#FFFFFF")
    #SNOWFLAKE 4
    draw.line((45,6,45,7), fill = "#FFFFFF")
    draw.line((46,5,46,6), fill = "#FFFFFF")
    #SNOWFLAKE 5
    draw.line((49,5,51,7), fill = "#FFFFFF")
    draw.line((49,7,51,5), fill = "#FFFFFF")
    #SNOWFLAKE 6
    draw.line((55,8,55,8), fill = "#FFFFFF")
    draw.line((55,10,57,8), fill = "#FFFFFF")
    #SNOWFLAKE 7
    draw.point((39,11), fill = "#FFFFFF")
    draw.point((38,12), fill = "#FFFFFF")
    draw.point((40,12), fill = "#FFFFFF")
    draw.point((39,13), fill = "#FFFFFF")
    #SNOWFLAKE 8
    draw.point((45,9), fill = "#FFFFFF")
    draw.point((44,10), fill = "#FFFFFF")
    draw.point((46,10), fill = "#FFFFFF")
    draw.point((45,11), fill = "#FFFFFF")
    #SNOWFLAKE 9
    draw.line((49,12,51,12), fill = "#FFFFFF")
    draw.line((50,11,50,13), fill = "#FFFFFF")
    matrix.SetImage(image_snow.im.id, 0, 0)
    time.sleep(30)
    matrix.Clear()
def displayMist(curr_weather_temp_int, wind_direction_name_dict):
    image_mist = Image.new("RGB", (64,32))
    draw = ImageDraw.Draw(image_mist)
    draw.text((0,3), get_current_time(), font=font8, fill="#FFFFFF")
    if curr_weather_temp_int >= 80:
        draw.text((0,19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="#EF3B09")
    elif curr_weather_temp_int >= 32 and curr_weather_temp_int < 80:
        draw.text((0,19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="#0DBA3E")
    else:
        draw.text((0,19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="#42C5F4")
    draw.text((29,15), str(get_curr_weather_wind_speed(owm)) + "MPH", font=font8, fill="#FFFFFF")
    draw.text((29,23), wind_direction_name_dict[get_curr_weather_wind_direction(owm)], font=font8, fill="#FFFFFF")
    #LINE 1
    for x in xrange(0,18):
        lineCO1 = 38 + x
        lineCO3 = 39 + x
        if lineCO1 % 2 == 0:
            lineCO2 = 5
            lineCO4 = 4
        else:
            lineCO2 = 4
            lineCO4 = 5
        draw.line((lineCO1, lineCO2, lineCO3, lineCO4), fill = "#CCCCCC")
    #LINE 2
    for x in xrange(0,18):
        lineCO1 = 38 + x
        lineCO3 = 39 + x
        if lineCO1 % 2 == 0:
            lineCO2 = 8
            lineCO4 = 7
        else:
            lineCO2 = 7
            lineCO4 = 8
        draw.line((lineCO1, lineCO2, lineCO3, lineCO4), fill = "#CCCCCC")
    #LINE 3
    for x in xrange(0,18):
        lineCO1 = 38 + x
        lineCO3 = 39 + x
        if lineCO1 % 2 == 0:
            lineCO2 = 11
            lineCO4 = 10
        else:
            lineCO2 = 10
            lineCO4 = 11
        draw.line((lineCO1, lineCO2, lineCO3, lineCO4), fill = "#CCCCCC")
    matrix.SetImage(image_mist.im.id, 0, 0)
    time.sleep(30)
    matrix.Clear()
def displayTornado(curr_weather_temp_int, wind_direction_name_dict):
    image_tornado = Image.new("RGB", (64,32))
    draw = ImageDraw.Draw(image_tornado)
    draw.text((0,3), get_current_time(), font=font8, fill="#FFFFFF")
    if curr_weather_temp_int >= 80:
        draw.text((0,19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="#EF3B09")
    elif curr_weather_temp_int >= 32 and curr_weather_temp_int < 80:
        draw.text((0,19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="#0DBA3E")
    else:
        draw.text((0,19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="#42C5F4")
    draw.text((29,15), str(get_curr_weather_wind_speed(owm)) + "MPH", font=font8, fill="#FFFFFF")
    draw.text((29,23), wind_direction_name_dict[get_curr_weather_wind_direction(owm)], font=font8, fill="#FFFFFF")
    #TORNADO
    draw.line((40,1,54,1), fill = "#CCCCCC")
    draw.line((41,2,53,2), fill = "#CCCCCC")
    draw.line((42,3,52,3), fill = "#CCCCCC")
    draw.line((43,4,51,4), fill = "#CCCCCC")
    draw.line((44,5,50,5), fill = "#CCCCCC")
    draw.line((44,6,50,6), fill = "#CCCCCC")
    draw.line((45,7,49,7), fill = "#CCCCCC")
    draw.line((46,8,50,8), fill = "#CCCCCC")
    draw.line((47,9,49,9), fill = "#CCCCCC")
    draw.line((48,10,49,10), fill = "#CCCCCC")
    draw.line((48,11,49,11), fill = "#CCCCCC")
    draw.line((48,12,49,12), fill = "#CCCCCC")
    draw.point((49,13), fill = "#CCCCCC")
    matrix.SetImage(image_tornado.im.id, 0, 0)
    time.sleep(30)
    matrix.Clear()
def main():
    #PREPARATION: LEAGUE STUFF
    try:
        summonerRank = get_LeagueStats()['rank']
        summonerName = "Finis Aeternum"
        summoner_LeaguePoints = get_LeagueStats()['league_points']
    except TypeError:
        matrix.Clear()
        image_LeagueFail2 = Image.new("RGB", (64,32))
        draw2 = ImageDraw.Draw(image_LeagueFail2)
        draw2.text((1,1), "Enter your", font=font7, fill = "#FF0000")
        draw2.text((1,10), "League and", font=font7, fill = "#FF0000")
        draw2.text((1,19), "division:", font=font7, fill = "#FF0000")
        matrix.SetImage(image_LeagueFail2.im.id, 0, 0)
        summonerRank = raw_input("")
        matrix.Clear()
        image_LeagueFail3 = Image.new("RGB", (64,32))
        draw3 = ImageDraw.Draw(image_LeagueFail3)
        draw3.text((1,1), "Enter your", font=font7, fill = "#FF0000")
        draw3.text((1,10), "League Points", font=font7, fill = "#FF0000")
        matrix.SetImage(image_LeagueFail3.im.id, 0, 0)
        summoner_LeaguePoints = int(raw_input(""))
    #PREPARATION: WEATHER STUFF
    try:
        while True:
            APIFailure = False
            try:
                owm = pyowm.OWM('5c50d5ab850e6a5ea0870a4794df3a9e')
                get_weather = owm.weather_at_id(5146277)
                curr_weather = get_weather.get_weather()
                curr_weather_code = curr_weather.get_weather_code()
                curr_weather_wind_speed = str(int(round(curr_weather.get_wind()['speed'] * 2.23694))) + "MPH"
                curr_weather_wind_direction = int(round(curr_weather.get_wind()['deg'], -1))
                #A name dict for all degree measurements of wind to meteorological names (NNW) etc
                wind_direction_name_dict = {0:'N', 10:'N', 20:'NNE', 30:'NNE', 40:'NE', 50:'NE', 60:'NE', 70:'ENE', 80:'ENE', 90:'E', 100:'E', 110:'ESE', 120:'ESE', 130:'SE', 140:'SE', 150:'SE', 160:'SSE', 170:'SSE', 180:'S', 190:'S', 200:'SSW', 210:'SSW', 220:'SW', 230:'SW', 240:'SW', 250:'WSW', 260:'WSW', 270:'W', 280:'W', 290:'WNW', 300:'WNW', 310:'NW', 320:'NW', 330:'NW', 340:'NNW', 350:'NNW', 360:'N'}
                #END
                APIFailure = False
            except pyowm.exceptions.api_call_error.APICallError:
                print('API Call Failed. Proceeding')
                APIFailure = True
            #FIRST STEP: NAME
            for x in xrange(0,6):
                matrix.Clear()
                image_name = Image.new("RGB", (64,32))
                draw = ImageDraw.Draw(image_name)
                draw.text((0,0), "Eli Vosniak", font=font8, fill="#FFFFFF")
                matrix.SetImage(image_name.im.id, getRandX(), getRandY())
                time.sleep(5)
                matrix.Clear()
            matrix.Clear()
            #SECOND STEP: LOL
            if summonerRank in ['Bronze 5', 'Bronze 4', 'Bronze 3', 'Bronze 2', 'Bronze 1']:
                rankColor = '#CD7F32'
            elif summonerRank in ['Silver 5', 'Silver 4', 'Silver 3', 'Silver 2', 'Silver 1']:
                rankColor = '#C0C0C0'
            elif summonerRank in ['Gold 5', 'Gold 4', 'Gold 3', 'Gold 2', 'Gold 1']:
                rankColor = '#FFD700'
            elif summonerRank in ['Platinum 5', 'Platinum 4', 'Platinum 3', 'Platinum 2', 'Platinum 1']:
                rankColor = '#3F9896'
            elif summonerRank in ['Diamond 5', 'Diamond 4', 'Diamond 3', 'Diamond 2', 'Diamond 1']:
                rankColor = '#64BFDE'
            else:
                rankColor = "#FFFFFF"
            if summoner_LeaguePoints == 0:
                LPColor = "#FF0000"
            elif summoner_LeaguePoints > 0 and summoner_LeaguePoints <= 75:
                LPColor = "#FFFFFF"
            else:
                LPColor = "#0DBA3E"
            for x in xrange(0,3):
                matrix.Clear()
                image_summonerName = Image.new("RGB", (64,32))
                draw = ImageDraw.Draw(image_summonerName)
                draw.text((1,12), "Finis Aeter num", font=font7, fill="#FFFFFF")
                matrix.SetImage(image_summonerName.im.id, 0, 0)
                time.sleep(5)
                matrix.Clear()
                image_summonerRank = Image.new("RGB", (64,32))
                draw2 = ImageDraw.Draw(image_summonerRank)
                draw2.text((6,6), summonerRank, font=font8, fill=rankColor)
                draw2.text((30,18), str(summoner_LeaguePoints) + "LP", font=font8, fill = LPColor)
                matrix.SetImage(image_summonerRank.im.id, 0, 0)
                time.sleep(5)
                matrix.Clear()
            #STEP 3: PUBG
            if PUBGChickenDinner == None and PUBGTopTen == None:
                None
            elif PUBGChickenDinner != None and PUBGTopTen == None:
                image_PUBGWins = Image.new("RGB", (64,32))
                draw = ImageDraw.Draw(image_PUBGWins)
                draw.text((1,1), "Number of", font = font7, fill = "#E2B279")
                draw.text((1,10), "Chicken Dinners", font = font7, fill = "#E2B279")
                draw.text((1,19), "this wipe", font = font7, fill = "#E2B279")
                draw.text((50,18), PUBGChickenDinner, font = ImageFont.truetype(".DejaVuSans-Bold.ttf", 12), fill = "#FFFFFF")
                matrix.SetImage(image_PUBGWins.im.id, 0, 0)
                time.sleep(30)
            elif PUBGChickenDinner == None and PUBGTopTen != None:
                image_PUBGTopTen = Image.new("RGB", (64,32))
                draw2 = ImageDraw.Draw(image_PUBGTopTen)
                draw2.text((1,1), "Number of", font = font7, fill = "#FFD700")
                draw2.text((1,10), "Top Tens", font = font7, fill = "#FFD700")
                draw2.text((1,19), "this wipe", font = font7, fill = "#FFD700")
                draw2.text((50,18), PUBGTopTen, font = ImageFont.truetype(".DejaVuSans-Bold.ttf", 12), fill = "#FFFFFF")
                matrix.SetImage(image_PUBGTopTen.im.id, 0, 0)
                time.sleep(30)
            else:
                for x in xrange(0,3):
                    image_PUBGWins = Image.new("RGB", (64,32))
                    draw = ImageDraw.Draw(image_PUBGWins)
                    draw.text((1,1), "Number of", font = font7, fill = "#E2B279")
                    draw.text((1,10), "Chicken Dinners", font = font7, fill = "#E2B279")
                    draw.text((1,19), "this wipe", font = font7, fill = "#E2B279")
                    draw.text((50,18), PUBGChickenDinner, font = ImageFont.truetype(".DejaVuSans-Bold.ttf", 12), fill = "#FFFFFF")
                    matrix.SetImage(image_PUBGWins.im.id, 0, 0)
                    time.sleep(5)
                    image_PUBGTopTen = Image.new("RGB", (64,32))
                    draw2 = ImageDraw.Draw(image_PUBGTopTen)
                    draw2.text((1,1), "Number of", font = font7, fill = "#FFD700")
                    draw2.text((1,10), "Top Tens", font = font7, fill = "#FFD700")
                    draw2.text((1,19), "this wipe", font = font7, fill = "#FFD700")
                    draw2.text((50,18), PUBGTopTen, font = ImageFont.truetype(".DejaVuSans-Bold.ttf", 12), fill = "#FFFFFF")
                    matrix.SetImage(image_PUBGTopTen.im.id, 0, 0)
                    time.sleep(5)
            #STEP 4: WEATHER
            if APIFailure == True:
                None
            else:
                if curr_weather_code == 804:
                    displayOvercast()
                elif curr_weather_code == 803:
                    displayBroken()
                elif curr_weather_code == 802:
                    displayScattered()
                elif curr_weather_code == 801:
                    displayFew()
                elif curr_weather_code == 800:
                    displayClear()
                elif curr_weather_code in [200, 201, 202, 210, 211, 212, 221, 230, 231, 232]:
                    displayThunderstorm()
                elif curr_weather_code in [300, 301, 302, 310, 311, 312, 313, 314, 321, 500, 501, 502, 503, 504, 511, 520, 521, 522, 531]:
                    displayRain()
                elif curr_weather_code in [600, 601, 602, 611, 612, 615, 616, 620, 621, 622]:
                    displaySnow()
                elif curr_weather_code in [701, 711, 721, 731, 741, 751, 761, 762]:
                    displayMist()
                elif curr_weather_code in [781, 900]:
                    displayTornado()
                else:
                    None
                    print('Failed')
    except KeyboardInterrupt:
        print('\nQuitting...')
        matrix.Clear()
main()