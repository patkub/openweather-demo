import requests

#
# Patrick Kubiak
#
# What was wrong?
# 1) Not checking for success of response properly
# 2) 'current' key instead of 'main' for current weather
# 3) Added 'wind_' prefix to 'speed', 'gust' and 'deg' keys
#
# Improvements:
#   * Changed get_api_key to use with...open which automatically closes file handler
#   * Refactored to use a single print weather method
#   * Linted/formatted code automatically with black (https://github.com/psf/black)
#       - To install black on linux/osx:
#           - python3 -m pip install black
#               - or just "pip3" instead of "python3 -m pip" on most systems
#         It's probably python instead of python3 on Windows
#
#       - To automatically format weather.py with black:
#           - black weather.py

#
#  Function to read in my own API key.
#
#  This way I can give out the code, but not give out my personal key.
#  This is standard practice when putting code up on github, etc...
#
#  Edits: changed to with...open which automatically closes file handler
def get_api_key():
    with open("my_ver_own_api_key.txt", "r") as f:
        my_api_key = f.read()
    return my_api_key.rstrip()


# print weather info
def print_weather(current_weather, temp, wind_gust, title):
    print(f"\t\t\t{title}\n")
    print("\t\t\tTEMPERATURE             = ", temp, " deg F")
    print("\t\t\tHUMIDITY                = ", current_weather["humidity"], " percent")
    print("\t\t\tATMOSPHERIC PRESSURE    = ", current_weather["pressure"], " hPascals")

    print("\t\t\tWIND SPEED              = ", current_weather["wind_speed"], " knots")
    print("\t\t\tWIND GUSTS (10 mins)    = ", wind_gust, " knots")
    print("\t\t\tWIND ANGLE              = ", current_weather["wind_deg"], " deg")

    print("\n\n\n")


# load api key from file
API_KEY = get_api_key()

# format request with api key
# RIT
cmd = "https://api.openweathermap.org/data/2.5/onecall?lat=43.0850&lon=-77.6719&units=imperial&appid={}".format(
    API_KEY
)

try:
    response = requests.get(cmd)
    # check success
    response.raise_for_status()
    # good to go
    json_object = response.json()

    # ########################################################################
    #
    #  Get the main temperature values:
    #
    current_weather = json_object["current"]

    #
    # Use a command like this to find out what keys are available to you,
    # and what their values are.
    #
    # for key in main_weather.keys() :
    #     print( key , "\t== ", main_weather[ key ] )
    print("\n\n\n")
    print_weather(
        current_weather,
        current_weather["temp"],
        json_object["hourly"][0]["wind_gust"],
        "Today's Weather",
    )

    # tomorrow's daily data is next index
    tomorrow_weather = json_object["hourly"][24]

    print_weather(
        tomorrow_weather,
        tomorrow_weather["temp"],
        tomorrow_weather["wind_gust"],
        "Tomorrow's Weather",
    )

except requests.exceptions.HTTPError as err:
    print(err)
