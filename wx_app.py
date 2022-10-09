from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.factory import Factory
import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import urllib.request as img_get


# The different screens
class MainWindow(Screen):

    def get_wx(self):
        # grabs database of locations
        
        cities = pd.read_csv("uscities.csv")

        location = self.ids.location.text
        state = self.ids.state.text

        # converts city name to lat/lon for url variables
        city_coordinates = cities[["lat", "lng", "state_name"]].where(cities["city"] == location)
        coordinates = city_coordinates[["lat", "lng"]].where(city_coordinates["state_name"] == state).dropna()

        check = str(coordinates.values).split()
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
    
    def popup_menu(self, value):
        if value == "Help":
            Factory.help_page().open()
            self.ids.drop_menu.text = "..."
        elif value == "About":
            Factory.about_page().open()
            self.ids.drop_menu.text = "..."
    
    

class WindowTwo(Screen):
    
    def get_radar(self):

        img_get.urlretrieve("https://radar.weather.gov/ridge/standard/CONUS_0.gif", "radar.jpg")

        self.ids.radar_id.source = "radar.jpg"

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('layouts.kv')



class Wx(App):
    def build(self):
        return kv


# on launch start main window class
if __name__ == "__main__":
    Wx().run()
