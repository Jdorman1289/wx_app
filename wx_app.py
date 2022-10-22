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

            self.ids.observation.text = f"Current Conditions for {location} {state} {obs[0].text}{obs[1].text}"
            self.ids.forecast.text = f"Forecast for {location} {state} \n\n{time_label[0].text}: {wx[0].text} \n\n{time_label[1].text}: {wx[1].text} \n\n{time_label[2].text}: {wx[2].text} \n\n{time_label[3].text}: {wx[3].text} \n\n{time_label[4].text}: {wx[4].text}\n\n{time_label[5].text}: {wx[5].text}\n\n"

    def clear(self):
        self.ids.location.text = ""
        self.ids.state.text = ""
        self.ids.observation.text = " "
        self.ids.forecast.text = " "
    
    
    def get_radar(self):

        img_get.urlretrieve("https://radar.weather.gov/ridge/standard/CONUS_0.gif", "radar.jpg")

        self.ids.radar_id.source = "radar.jpg"
        self.ids.radar_id.height = self.height

    def update(self):
        webbrowser.open_new_tab("https://github.com/Jdorman1289/wx_app/releases")

    def donate(self):
        webbrowser.open_new_tab("https://ko-fi.com/jessecreates")


class Wx(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        return Builder.load_file('layouts.kv')


# on launch start main window class
if __name__ == "__main__":
    Wx().run()
