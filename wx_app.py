from kivymd.app import MDApp
from kivymd.uix.widget import MDWidget
from kivy.lang import Builder
from kivy.core.window import Window
import webbrowser
import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import urllib.request as img_get

Window.size = 640, 640

class MainWindow(MDWidget):

    def get_wx(self):


        # grabs database of locations
        
        cities = pd.read_csv("uscities.csv")

        location = self.ids.location.text
        state = self.ids.state.text

        # converts city name to lat/lon for url variables
        city_coordinates = cities[["lat", "lng", "state_name"]].where(cities["city"] == location)
        coordinates = city_coordinates[["lat", "lng"]].where(city_coordinates["state_name"] == state).dropna()

        check = str(coordinates.values).split()
        if len(check) >= 3:
            lat = check[1]
            lon = check[2].strip("]")
            
            url = f"https://forecast.weather.gov/MapClick.php?lat={lat}&lon={lon}"

            site = requests.get(url)
            site_soup = bs(site.content, features="html.parser")
            wx = site_soup.find_all("div", re.compile("forecast-text"))
            time_label = site_soup.find_all("div", re.compile("forecast-label"))

            obs = site_soup.find_all("div", re.compile("pull-left"))

            wx_icons = {"Cloudy": "cloudy.png", "Overcast": "cloudy.png", "Rain": "rainy.png", "Drizzle": "rainy.png","Fair": "sunny.png", "Sunny": "sunny.png","Clear": "sunny.png", "Thunderstorms": "stormy.png", "Wind": "windy.png", "Breezy": "windy.png", "Snow": "snowy.png"}

            # for obs icon pic
            obs_icon_check = f"{obs[0].text}".split()
            for weather in obs_icon_check:
                for icon in wx_icons:
                    if weather == icon:
                        self.ids.ob_icon_image.source = wx_icons[icon]
                        self.ids.ob_icon_image.height = "128dp"

            # current wx
            self.ids.observation.text = f"{obs[0].text}{obs[1].text}"


            forecast_icon_check_0 = f"{wx[0].text}".split()
            for weather_forecast in forecast_icon_check_0:
                for ico in wx_icons:
                    if f"{weather_forecast}".upper == f"{forecast_icon_check_0}".upper:
                        self.ids.forecast_label_0.text = f"{time_label[0].text}"
                        self.ids.forecast_0.text = f"{wx[0].text}"
                        self.ids.forecast_icon_0.source = wx_icons[ico]
                        self.ids.forecast_icon_0.height = "128dp"


            print(f"{weather_forecast}".upper)

            # forecast


            self.ids.forecast_label_1.text = f"{time_label[1].text}"
            self.ids.forecast_1.text = f"{wx[1].text}"
            self.ids.forecast_icon_1.source = "rainy.png"
            self.ids.forecast_icon_1.height = "128dp"

            self.ids.forecast_label_2.text = f"{time_label[2].text}"
            self.ids.forecast_2.text = f"{wx[2].text}"
            self.ids.forecast_icon_2.source = "snowy.png"
            self.ids.forecast_icon_2.height = "128dp"


        else:

            self.ids.observation.text = "No data found! Please make sure the location is entered in this format:\n\n'Dallas' 'Texas'"
            self.ids.ob_icon_image.source = "no_data.png"
            self.ids.ob_icon_image.height = "128dp"
            self.ids.forecast.text = ""


    def clear(self):
        # resets wx data
        self.ids.location.text = ""
        self.ids.state.text = ""
        self.ids.observation.text = " "

        self.ids.radar_id.height = "0dp"

        # resets icons
        self.ids.ob_icon_image.height = "0dp"
        self.ids.ob_icon_image.source = ""

    
    
    def get_radar(self):

        img_get.urlretrieve("https://radar.weather.gov/ridge/standard/CONUS_0.gif", "radar.jpg")

        self.ids.radar_id.source = "radar.jpg"
        self.ids.radar_id.height = self.height

    def update(self):
        webbrowser.open_new_tab("https://github.com/Jdorman1289/wx_app/releases")

    def donate(self):
        webbrowser.open_new_tab("https://ko-fi.com/jessecreates")

    def close_two(self):
        exit()

class Wx(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "LightBlue"
        return Builder.load_file('layouts.kv')


# on launch start main window class
if __name__ == "__main__":
    Wx().run()
