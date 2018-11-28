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

matrix = Adafruit_RGBmatrix(32, 2)
degree_sign = u'\N{DEGREE SIGN}'
font7 = ImageFont.truetype(".DejaVuSans-Bold.ttf", 7)
font8 = ImageFont.truetype(".DejaVuSans-Bold.ttf", 8)
lol = LeagueOfLegends('RGAPI-b71a8fe2-804a-4d13-aab9-5ca9b9bca956')
# A name dict for all degree measurements of wind to meteorological names (NNW) etc
WIND_DIRECTION_NAME_DICT = {0: 'N', 10: 'N', 20: 'NNE', 30: 'NNE', 40: 'NE',
                            50: 'NE', 60: 'NE', 70: 'ENE', 80: 'ENE', 90: 'E',
                            100: 'E', 110: 'ESE', 120: 'ESE', 130: 'SE', 140: 'SE',
                            150: 'SE', 160: 'SSE', 170: 'SSE', 180: 'S', 200: 'SSW',
                            190: 'S', 210: 'SSW', 220: 'SW', 230: 'SW', 240: 'SW',
                            250: 'WSW', 260: 'WSW', 270: 'W', 280: 'W', 290: 'WNW',
                            300: 'WNW', 310: 'NW', 320: 'NW', 330: 'NW', 340: 'NNW',
                            350: 'NNW', 360: 'N'}


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


def get_league_stats():
    try:
        summoner = lol.get_summoner_by_name("Finis Aeternum")
        print(summoner)
        return summoner
    except urllib2.URLError:
        print("League call failed. Proceeding...")


def get_rand_x():
    randx = random.randint(0, 15)
    return randx


def get_rand_y():
    randy = random.randint(0, 20)
    return randy


def add_temperature_weather_image(image, curr_weather_temp_int):
    """Adds temperature to the image supplied.

    :param image: The image to add temperature string to
    :param curr_weather_temp_int: The temperature value to add to the image
    """
    draw = ImageDraw.Draw(image)
    if curr_weather_temp_int >= 80:
        draw.text((0, 19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="#EF3B09")
    elif curr_weather_temp_int >= 32:
        draw.text((0, 19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="#0DBA3E")
    else:
        draw.text((0, 19), str(curr_weather_temp_int) + degree_sign, font=font8, fill="42C5F4")


def add_small_sun_weather_image(image):
    """Adds a small sun to weather display area on signboard.

    :param image: image to add the small sun to
    """
    draw = ImageDraw.Draw(image)
    draw.ellipse(((41, 1), (53, 13)), fill="#FFBB00")


def add_three_clouds_weather_image(image):
    """Adds three clouds to weather display area on signboard.

    :param image: image to add three clouds to
    """
    draw = ImageDraw.Draw(image)
    # CLOUD 1
    draw.line((42, 3, 43, 3), fill="#FFFFFF")
    draw.line((40, 4, 45, 4), fill="#FFFFFF")
    draw.line((38, 5, 47, 5), fill="#FFFFFF")
    draw.line((37, 6, 48, 6), fill="#FFFFFF")
    draw.line((37, 7, 48, 7), fill="#FFFFFF")
    draw.line((38, 8, 47, 8), fill="#FFFFFF")
    draw.line((39, 9, 46, 9), fill="#FFFFFF")
    # CLOUD 2
    draw.line((53, 6, 54, 6), fill="#FFFFFF")
    draw.line((51, 7, 56, 7), fill="#FFFFFF")
    draw.line((49, 8, 58, 8), fill="#FFFFFF")
    draw.line((48, 9, 59, 9), fill="#FFFFFF")
    draw.line((48, 10, 59, 10), fill="#FFFFFF")
    draw.line((49, 11, 58, 11), fill="#FFFFFF")
    draw.line((50, 12, 57, 12), fill="#FFFFFF")
    # TINY CLOUD
    draw.line((51, 2, 52, 2), fill="#FFFFFF")
    draw.line((49, 3, 54, 3), fill="#FFFFFF")
    draw.line((50, 4, 53, 4), fill="#FFFFFF")


def add_two_clouds_weather_image(image):
    """Adds two clouds to weather display area on signboard.

    :param image: image to add two clouds to
    """
    draw = ImageDraw.Draw(image)
    # CLOUD 1
    draw.line((42, 3, 43, 3), fill="#FFFFFF")
    draw.line((40, 4, 45, 4), fill="#FFFFFF")
    draw.line((38, 5, 47, 5), fill="#FFFFFF")
    draw.line((37, 6, 48, 6), fill="#FFFFFF")
    draw.line((37, 7, 48, 7), fill="#FFFFFF")
    draw.line((38, 8, 47, 8), fill="#FFFFFF")
    draw.line((39, 9, 46, 9), fill="#FFFFFF")
    # TINY CLOUD
    draw.line((51, 2, 52, 2), fill="#FFFFFF")
    draw.line((49, 3, 54, 3), fill="#FFFFFF")
    draw.line((50, 4, 53, 4), fill="#FFFFFF")


def add_one_cloud_weather_image(image):
    """Adds one cloud to weather display area on signboard.

    :param image: image to add cloud to
    :return:
    """
    draw = ImageDraw.Draw(image)
    # TINY CLOUD
    draw.line((51, 2, 52, 2), fill="#FFFFFF")
    draw.line((49, 3, 54, 3), fill="#FFFFFF")
    draw.line((50, 4, 53, 4), fill="#FFFFFF")


def display_overcast_weather(owm, curr_weather_temp_int, wind_direction_name_dict):
    image_overcast_clouds = Image.new("RGB", (64, 32))
    draw = ImageDraw.Draw(image_overcast_clouds)
    draw.text((0, 3), get_current_time(), font=font8, fill="#FFFFFF")
    add_temperature_weather_image(image_overcast_clouds, curr_weather_temp_int)
    draw.text((29, 15), get_curr_weather_wind_speed(owm), font=font8, fill="#FFFFFF")
    draw.text((29, 23), wind_direction_name_dict[get_curr_weather_wind_direction(owm)], font=font8, fill="#FFFFFF")
    add_three_clouds_weather_image(image_overcast_clouds)
    matrix.SetImage(image_overcast_clouds.im.id, 0, 0)
    time.sleep(30)
    matrix.Clear()


def display_broken_weather(owm, curr_weather_temp_int, wind_direction_name_dict):
    image_broken_clouds = Image.new("RGB", (64, 32))
    draw = ImageDraw.Draw(image_broken_clouds)
    draw.text((0, 3), get_current_time(), font=font8, fill="#FFFFFF")
    add_temperature_weather_image(image_broken_clouds, curr_weather_temp_int)
    draw.text((29, 15), str(get_curr_weather_wind_speed(owm)) + "MPH", font=font8, fill="#FFFFFF")
    draw.text((29, 23), wind_direction_name_dict[get_curr_weather_wind_direction(owm)], font=font8, fill="#FFFFFF")
    add_small_sun_weather_image(image_broken_clouds)
    add_three_clouds_weather_image(image_broken_clouds)
    matrix.SetImage(image_broken_clouds.im.id, 0, 0)
    time.sleep(30)
    matrix.Clear()


def display_scattered_weather(owm, curr_weather_temp_int, wind_direction_name_dict):
    image_scattered_clouds = Image.new("RGB", (64, 32))
    draw = ImageDraw.Draw(image_scattered_clouds)
    draw.text((0, 3), get_current_time(), font=font8, fill="#FFFFFF")
    add_temperature_weather_image(image_scattered_clouds, curr_weather_temp_int)
    draw.text((29, 15), str(get_curr_weather_wind_speed(owm)) + "MPH", font=font8, fill="#FFFFFF")
    draw.text((29, 23), wind_direction_name_dict[get_curr_weather_wind_direction(owm)], font=font8, fill="#FFFFFF")
    add_small_sun_weather_image(image_scattered_clouds)
    add_two_clouds_weather_image(image_scattered_clouds)
    matrix.SetImage(image_scattered_clouds.im.id, 0, 0)
    time.sleep(30)
    matrix.Clear()


def display_few_weather(owm, curr_weather_temp_int, wind_direction_name_dict):
    image_few_clouds = Image.new("RGB", (64, 32))
    draw = ImageDraw.Draw(image_few_clouds)
    draw.text((0, 3), get_current_time(), font=font8, fill="#FFFFFF")
    add_temperature_weather_image(image_few_clouds, curr_weather_temp_int)
    draw.text((29, 15), str(get_curr_weather_wind_speed(owm)) + "MPH", font=font8, fill="#FFFFFF")
    draw.text((29, 23), wind_direction_name_dict[get_curr_weather_wind_direction(owm)], font=font8, fill="#FFFFFF")
    add_small_sun_weather_image(image_few_clouds)
    add_one_cloud_weather_image(image_few_clouds)
    matrix.SetImage(image_few_clouds.im.id, 0, 0)
    time.sleep(30)
    matrix.Clear()


def display_clear_weather(owm, curr_weather_temp_int, wind_direction_name_dict):
    image_clear_sky = Image.new("RGB", (64, 32))
    draw = ImageDraw.Draw(image_clear_sky)
    draw.text((0, 3), get_current_time(), font=font8, fill="#FFFFFF")
    add_temperature_weather_image(image_clear_sky, curr_weather_temp_int)
    draw.text((29, 15), str(get_curr_weather_wind_speed(owm)) + "MPH", font=font8, fill="#FFFFFF")
    draw.text((29, 23), wind_direction_name_dict[get_curr_weather_wind_direction(owm)], font=font8, fill="#FFFFFF")
    draw.ellipse(((39, 1), (51, 13)), fill="#FFBB00")
    matrix.SetImage(image_clear_sky.im.id, 0, 0)
    time.sleep(30)
    matrix.Clear()


def display_thunderstorm_weather(owm, curr_weather_temp_int, wind_direction_name_dict):
    image_thunderstorm = Image.new("RGB", (64, 32))
    draw = ImageDraw.Draw(image_thunderstorm)
    draw.text((0, 3), get_current_time(), font=font8, fill="#FFFFFF")
    add_temperature_weather_image(image_thunderstorm, curr_weather_temp_int)
    draw.text((29, 15), str(get_curr_weather_wind_speed(owm)) + "MPH", font=font8, fill="#FFFFFF")
    draw.text((29, 23), wind_direction_name_dict[get_curr_weather_wind_direction(owm)], font=font8, fill="#FFFFFF")
    # CLOUD 1
    draw.line((42, 3, 43, 3), fill="#BABABA")
    draw.line((40, 4, 45, 4), fill="#BABABA")
    draw.line((38, 5, 47, 5), fill="#BABABA")
    draw.line((37, 6, 48, 6), fill="#BABABA")
    draw.line((37, 7, 48, 7), fill="#BABABA")
    draw.line((38, 8, 47, 8), fill="#BABABA")
    draw.line((39, 9, 46, 9), fill="#BABABA")
    # TINY CLOUD 1
    draw.line((51, 2, 52, 2), fill="#FFFFFF")
    draw.line((49, 3, 54, 3), fill="#FFFFFF")
    draw.line((50, 4, 53, 4), fill="#FFFFFF")
    # TINY CLOUD 2
    draw.line((53, 6, 54, 6), fill="#FFFFFF")
    draw.line((51, 7, 56, 7), fill="#FFFFFF")
    draw.line((52, 8, 55, 8), fill="#FFFFFF")
    # LIGHTNING BOLT
    draw.line((42, 10, 44, 10), fill="#FFED11")
    draw.line((43, 11, 45, 11), fill="#FFED11")
    draw.line((44, 11, 45, 11), fill="#FFED11")
    draw.line((44, 12, 45, 12), fill="#FFED11")
    draw.line((45, 13, 46, 13), fill="#FFED11")
    # RAIN DROPS
    draw.line((51, 5, 52, 5), fill="#0078FF")
    draw.line((52, 6, 52, 6), fill="#0078FF")
    draw.line((52, 9, 52, 10), fill="#0078FF")
    draw.line((54, 10, 54, 11), fill="#0078FF")
    draw.line((55, 9, 55, 9), fill="#0078FF")
    matrix.SetImage(image_thunderstorm.im.id, 0, 0)
    time.sleep(30)
    matrix.Clear()


def display_rain_weather(owm, curr_weather_temp_int, wind_direction_name_dict):
    image_rain = Image.new("RGB", (64, 32))
    draw = ImageDraw.Draw(image_rain)
    draw.text((0, 3), get_current_time(), font=font8, fill="#FFFFFF")
    add_temperature_weather_image(image_rain, curr_weather_temp_int)
    draw.text((29, 15), str(get_curr_weather_wind_speed(owm)) + "MPH", font=font8, fill="#FFFFFF")
    draw.text((29, 23), wind_direction_name_dict[get_curr_weather_wind_direction(owm)], font=font8, fill="#FFFFFF")
    # CLOUD 1
    draw.line((42, 3, 43, 3), fill="#BABABA")
    draw.line((40, 4, 45, 4), fill="#BABABA")
    draw.line((38, 5, 47, 5), fill="#BABABA")
    draw.line((37, 6, 48, 6), fill="#BABABA")
    draw.line((37, 7, 48, 7), fill="#BABABA")
    draw.line((38, 8, 47, 8), fill="#BABABA")
    draw.line((39, 9, 46, 9), fill="#BABABA")
    # TINY CLOUD 1
    draw.line((51, 2, 52, 2), fill="#FFFFFF")
    draw.line((49, 3, 54, 3), fill="#FFFFFF")
    draw.line((50, 4, 53, 4), fill="#FFFFFF")
    # TINY CLOUD 2
    draw.line((53, 6, 54, 6), fill="#FFFFFF")
    draw.line((51, 7, 56, 7), fill="#FFFFFF")
    draw.line((52, 8, 55, 8), fill="#FFFFFF")
    # RAIN DROPS
    draw.line((40, 10, 40, 11), fill="#0078FF")
    draw.line((43, 10, 43, 12), fill="#0078FF")
    draw.line((45, 11, 45, 12), fill="#0078FF")
    draw.line((41, 12, 41, 12), fill="#0078FF")
    draw.line((42, 13, 42, 13), fill="#0078FF")
    draw.line((44, 13, 44, 13), fill="#0078FF")
    draw.line((46, 13, 46, 13), fill="#0078FF")
    draw.line((46, 10, 46, 10), fill="#0078FF")
    draw.line((51, 5, 52, 5), fill="#0078FF")
    draw.line((52, 6, 52, 6), fill="#0078FF")
    draw.line((52, 9, 52, 10), fill="#0078FF")
    draw.line((54, 10, 54, 11), fill="#0078FF")
    draw.line((55, 9, 55, 9), fill="#0078FF")
    matrix.SetImage(image_rain.im.id, 0, 0)
    time.sleep(30)
    matrix.Clear()


def display_snow_weather(owm, curr_weather_temp_int, wind_direction_name_dict):
    image_snow = Image.new("RGB", (64, 32))
    draw = ImageDraw.Draw(image_snow)
    draw.text((0, 3), get_current_time(), font=font8, fill="#FFFFFF")
    add_temperature_weather_image(image_snow, curr_weather_temp_int)
    draw.text((29, 15), str(get_curr_weather_wind_speed(owm)) + "MPH", font=font8, fill="#FFFFFF")
    draw.text((29, 23), wind_direction_name_dict[get_curr_weather_wind_direction(owm)], font=font8, fill="#FFFFFF")
    # SNOWFLAKE 1
    draw.line((37, 2, 39, 4), fill="#FFFFFF")
    draw.line((37, 4, 39, 2), fill="#FFFFFF")
    # SNOWFLAKE 2
    draw.line((57, 3, 58, 3), fill="#FFFFFF")
    draw.line((56, 4, 56, 4), fill="#FFFFFF")
    draw.line((59, 4, 59, 4), fill="#FFFFFF")
    draw.line((57, 5, 58, 5), fill="#FFFFFF")
    # SNOWFLAKE 3
    draw.line((40, 7, 42, 7), fill="#FFFFFF")
    draw.line((41, 6, 41, 8), fill="#FFFFFF")
    # SNOWFLAKE 4
    draw.line((45, 6, 45, 7), fill="#FFFFFF")
    draw.line((46, 5, 46, 6), fill="#FFFFFF")
    # SNOWFLAKE 5
    draw.line((49, 5, 51, 7), fill="#FFFFFF")
    draw.line((49, 7, 51, 5), fill="#FFFFFF")
    # SNOWFLAKE 6
    draw.line((55, 8, 55, 8), fill="#FFFFFF")
    draw.line((55, 10, 57, 8), fill="#FFFFFF")
    # SNOWFLAKE 7
    draw.point((39, 11), fill="#FFFFFF")
    draw.point((38, 12), fill="#FFFFFF")
    draw.point((40, 12), fill="#FFFFFF")
    draw.point((39, 13), fill="#FFFFFF")
    # SNOWFLAKE 8
    draw.point((45, 9), fill="#FFFFFF")
    draw.point((44, 10), fill="#FFFFFF")
    draw.point((46, 10), fill="#FFFFFF")
    draw.point((45, 11), fill="#FFFFFF")
    # SNOWFLAKE 9
    draw.line((49, 12, 51, 12), fill="#FFFFFF")
    draw.line((50, 11, 50, 13), fill="#FFFFFF")
    matrix.SetImage(image_snow.im.id, 0, 0)
    time.sleep(30)
    matrix.Clear()


def display_mist_weather(owm, curr_weather_temp_int, wind_direction_name_dict):
    image_mist = Image.new("RGB", (64, 32))
    draw = ImageDraw.Draw(image_mist)
    draw.text((0, 3), get_current_time(), font=font8, fill="#FFFFFF")
    add_temperature_weather_image(image_mist, curr_weather_temp_int)
    draw.text((29, 15), str(get_curr_weather_wind_speed(owm)) + "MPH", font=font8, fill="#FFFFFF")
    draw.text((29, 23), wind_direction_name_dict[get_curr_weather_wind_direction(owm)], font=font8, fill="#FFFFFF")
    # LINE 1
    for x in range(0, 18):
        line_co1 = 38 + x
        line_co3 = 39 + x
        if line_co1 % 2 == 0:
            line_co2 = 5
            line_co4 = 4
        else:
            line_co2 = 4
            line_co4 = 5
        draw.line((line_co1, line_co2, line_co3, line_co4), fill="#CCCCCC")
    # LINE 2
    for x in range(0, 18):
        line_co1 = 38 + x
        line_co3 = 39 + x
        if line_co1 % 2 == 0:
            line_co2 = 8
            line_co4 = 7
        else:
            line_co2 = 7
            line_co4 = 8
        draw.line((line_co1, line_co2, line_co3, line_co4), fill="#CCCCCC")
    # LINE 3
    for x in range(0, 18):
        line_co1 = 38 + x
        line_co3 = 39 + x
        if line_co1 % 2 == 0:
            line_co2 = 11
            line_co4 = 10
        else:
            line_co2 = 10
            line_co4 = 11
        draw.line((line_co1, line_co2, line_co3, line_co4), fill="#CCCCCC")
    matrix.SetImage(image_mist.im.id, 0, 0)
    time.sleep(30)
    matrix.Clear()


def display_tornado_weather(owm, curr_weather_temp_int, wind_direction_name_dict):
    image_tornado = Image.new("RGB", (64, 32))
    draw = ImageDraw.Draw(image_tornado)
    draw.text((0, 3), get_current_time(), font=font8, fill="#FFFFFF")
    add_temperature_weather_image(image_tornado, curr_weather_temp_int)
    draw.text((29, 15), str(get_curr_weather_wind_speed(owm)) + "MPH", font=font8, fill="#FFFFFF")
    draw.text((29, 23), wind_direction_name_dict[get_curr_weather_wind_direction(owm)], font=font8, fill="#FFFFFF")
    # TORNADO
    draw.line((40, 1, 54, 1), fill="#CCCCCC")
    draw.line((41, 2, 53, 2), fill="#CCCCCC")
    draw.line((42, 3, 52, 3), fill="#CCCCCC")
    draw.line((43, 4, 51, 4), fill="#CCCCCC")
    draw.line((44, 5, 50, 5), fill="#CCCCCC")
    draw.line((44, 6, 50, 6), fill="#CCCCCC")
    draw.line((45, 7, 49, 7), fill="#CCCCCC")
    draw.line((46, 8, 50, 8), fill="#CCCCCC")
    draw.line((47, 9, 49, 9), fill="#CCCCCC")
    draw.line((48, 10, 49, 10), fill="#CCCCCC")
    draw.line((48, 11, 49, 11), fill="#CCCCCC")
    draw.line((48, 12, 49, 12), fill="#CCCCCC")
    draw.point((49, 13), fill="#CCCCCC")
    matrix.SetImage(image_tornado.im.id, 0, 0)
    time.sleep(30)
    matrix.Clear()

def get_ranked_color(summoner_rank):
    if summoner_rank in ['Bronze 5', 'Bronze 4', 'Bronze 3', 'Bronze 2', 'Bronze 1']:
        rank_color = '#CD7F32'
    elif summoner_rank in ['Silver 5', 'Silver 4', 'Silver 3', 'Silver 2', 'Silver 1']:
        rank_color = '#C0C0C0'
    elif summoner_rank in ['Gold 5', 'Gold 4', 'Gold 3', 'Gold 2', 'Gold 1']:
        rank_color = '#FFD700'
    elif summoner_rank in ['Platinum 5', 'Platinum 4', 'Platinum 3', 'Platinum 2', 'Platinum 1']:
        rank_color = '#3F9896'
    elif summoner_rank in ['Diamond 5', 'Diamond 4', 'Diamond 3', 'Diamond 2', 'Diamond 1']:
        rank_color = '#64BFDE'
    else:
        rank_color = "#FFFFFF"
    return rank_color


def get_lp_color(summoner_lp):
    if summoner_lp == 0:
        lp_color = "#FF0000"
    elif summoner_lp <= 75:
        lp_color = "#FFFFFF"
    else:
        lp_color = "#0DBA3E"
    return lp_color


def main():
    # PREPARATION: LEAGUE STUFF
    try:
        summoner_rank = get_league_stats()['rank']
        summoner_league_points = get_league_stats()['league_points']
    except TypeError:
        matrix.Clear()
        image_league_fail2 = Image.new("RGB", (64, 32))
        draw2 = ImageDraw.Draw(image_league_fail2)
        draw2.text((1, 1), "Enter your", font=font7, fill="#FF0000")
        draw2.text((1, 10), "League and", font=font7, fill="#FF0000")
        draw2.text((1, 19), "division:", font=font7, fill="#FF0000")
        matrix.SetImage(image_league_fail2.im.id, 0, 0)
        summoner_rank = input("")
        matrix.Clear()
        image_league_fail3 = Image.new("RGB", (64, 32))
        draw3 = ImageDraw.Draw(image_league_fail3)
        draw3.text((1, 1), "Enter your", font=font7, fill="#FF0000")
        draw3.text((1, 10), "League Points", font=font7, fill="#FF0000")
        matrix.SetImage(image_league_fail3.im.id, 0, 0)
        summoner_league_points = int(input(""))
    # PREPARATION: WEATHER STUFF
    try:
        while True:
            try:
                owm = pyowm.OWM('5c50d5ab850e6a5ea0870a4794df3a9e')
                get_weather = owm.weather_at_id(5146277)
                curr_weather = get_weather.get_weather()
                curr_weather_code = curr_weather.get_weather_code()
                # A name dict for all degree measurements of wind to meteorological names (NNW) etc
                wind_direction_name_dict = {0: 'N', 10: 'N', 20: 'NNE', 30: 'NNE', 40: 'NE', 50: 'NE', 60: 'NE',
                                            70: 'ENE', 80: 'ENE', 90: 'E', 100: 'E', 110: 'ESE', 120: 'ESE', 130: 'SE',
                                            140: 'SE', 150: 'SE', 160: 'SSE', 170: 'SSE', 180: 'S', 190: 'S',
                                            200: 'SSW', 210: 'SSW', 220: 'SW', 230: 'SW', 240: 'SW', 250: 'WSW',
                                            260: 'WSW', 270: 'W', 280: 'W', 290: 'WNW', 300: 'WNW', 310: 'NW',
                                            320: 'NW', 330: 'NW', 340: 'NNW', 350: 'NNW', 360: 'N'}
                # END
                api_failure = False
            except pyowm.exceptions.api_call_error.APICallError:
                print('API Call Failed. Proceeding')
                api_failure = True
            # FIRST STEP: NAME
            for x in range(0, 6):
                matrix.Clear()
                image_name = Image.new("RGB", (64, 32))
                draw = ImageDraw.Draw(image_name)
                draw.text((0, 0), "Eli Vosniak", font=font8, fill="#FFFFFF")
                matrix.SetImage(image_name.im.id, get_rand_x(), get_rand_y())
                time.sleep(5)
                matrix.Clear()
            matrix.Clear()
            # SECOND STEP: LOL
            rank_color = get_ranked_color(summoner_rank)
            lp_color = get_lp_color(summoner_league_points)
            for x in range(0, 3):
                matrix.Clear()
                image_summoner_name = Image.new("RGB", (64, 32))
                draw = ImageDraw.Draw(image_summoner_name)
                draw.text((1, 12), "Finis Aeter num", font=font7, fill="#FFFFFF")
                matrix.SetImage(image_summoner_name.im.id, 0, 0)
                time.sleep(5)
                matrix.Clear()
                image_summoner_rank = Image.new("RGB", (64, 32))
                draw2 = ImageDraw.Draw(image_summoner_rank)
                draw2.text((6, 6), summoner_rank, font=font8, fill=rank_color)
                draw2.text((30, 18), str(summoner_league_points) + "LP", font=font8, fill=lp_color)
                matrix.SetImage(image_summoner_rank.im.id, 0, 0)
                time.sleep(5)
                matrix.Clear()
            # STEP 3: WEATHER
            if not api_failure:
                if curr_weather_code == 804:
                    display_overcast_weather(owm, get_curr_weather_temp(owm), wind_direction_name_dict)
                elif curr_weather_code == 803:
                    display_broken_weather(owm, get_curr_weather_temp(owm), wind_direction_name_dict)
                elif curr_weather_code == 802:
                    display_scattered_weather(owm, get_curr_weather_temp(owm), wind_direction_name_dict)
                elif curr_weather_code == 801:
                    display_few_weather(owm, get_curr_weather_temp(owm), wind_direction_name_dict)
                elif curr_weather_code == 800:
                    display_clear_weather(owm, get_curr_weather_temp(owm), wind_direction_name_dict)
                elif curr_weather_code in [200, 201, 202, 210, 211, 212, 221, 230, 231, 232]:
                    display_thunderstorm_weather(owm, get_curr_weather_temp(owm), wind_direction_name_dict)
                elif curr_weather_code in [300, 301, 302, 310, 311, 312, 313, 314, 321, 500, 501, 502, 503, 504, 511,
                                           520, 521, 522, 531]:
                    display_rain_weather(owm, get_curr_weather_temp(owm), wind_direction_name_dict)
                elif curr_weather_code in [600, 601, 602, 611, 612, 615, 616, 620, 621, 622]:
                    display_snow_weather(owm, get_curr_weather_temp(owm), wind_direction_name_dict)
                elif curr_weather_code in [701, 711, 721, 731, 741, 751, 761, 762]:
                    display_mist_weather(owm, get_curr_weather_temp(owm), wind_direction_name_dict)
                elif curr_weather_code in [781, 900]:
                    display_tornado_weather(owm, get_curr_weather_temp(owm), wind_direction_name_dict)
                else:
                    print('Failed')
    except KeyboardInterrupt:
        print('\nQuitting...')
        matrix.Clear()


main()
