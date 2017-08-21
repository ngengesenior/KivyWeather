"""
This is a sample app that makes use of the Yahoo weather Api.

"""
import urllib2
import json
import urllib
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.properties import ObjectProperty, StringProperty
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup
from kivy.core.window import Window


class Launcher(Screen):
    def __init__(self, **kwargs):
        super(Launcher, self).__init__(**kwargs)

    def get_text(self):
        return 'This is the application that gives you access to [b]weather[/b] data' \
               ' from around the\n world by simply searching the [b][color=0000ff]location[/color' \
               '][/b] with respect to the Country.\n.To get weather conditions for Berlin, you just\n' \
               'type "Berlin",or "berlin" in the text field to see the weather.\n' \
               'To confirm weather the values returned are real, \nyou can check the conditions for the' \
               ' queried location and yahoo.'

class MainActivity(Screen):
    temperature = ObjectProperty(None)
    pressure = ObjectProperty(None)
    wind_direction = ObjectProperty(None)
    wind_speed = ObjectProperty(None)
    sunrise = ObjectProperty(None)
    sunset = ObjectProperty(None)
    latitude = ObjectProperty(None)
    longitude = ObjectProperty(None)
    humidity = ObjectProperty(None)
    lastBuildDate = ObjectProperty(None)
    description = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MainActivity, self).__init__(**kwargs)

    def get_weather(self, location):
        try:
            baseurl = "https://query.yahooapis.com/v1/public/yql?"
            yql_query = "select * from weather.forecast where woeid in (select woeid" \
                        " from geo.places(1) where text='{}')".format(
                location)
            yql_url = baseurl + urllib.urlencode({'q': yql_query}) + "&format=json"
            result = urllib2.urlopen(yql_url).read()
            data = json.loads(result)
            print data['query']['lang']
            pressure_link = data['query']['results']['channel']['atmosphere']['pressure']
            lastBuild = data['query']['results']['channel']['lastBuildDate']
            descr = data['query']['results']['channel']['description']
            humidity_link = data['query']['results']['channel']['atmosphere']['humidity']
            wind_link = data['query']['results']['channel']['wind']
            wind_direction, wind_speed = wind_link['direction'], wind_link['speed']
            astronomy_link = data['query']['results']['channel']['astronomy']  # error here
            sunrise = astronomy_link['sunrise']
            sunset = astronomy_link['sunset']
            image_link = data['query']['results']['channel']['image']['url']
            item_link = data['query']['results']['channel']['item']
            temp_link = item_link['condition']['temp']
            lat = item_link['lat']
            lon = item_link['long']
            print temp_link
            temp_in_degs = ((int(temp_link) - 32) / 1.8).__format__(".1f")
            self.temperature.text = str(temp_in_degs) + ' ' + u'\u00b0' + "C"
            self.pressure.text = str(pressure_link)  + " in"
            self.longitude.text = str(lon)
            self.latitude.text = str(lat)
            self.sunset.text = str(sunset)
            self.sunrise.text = str(sunrise)
            self.humidity.text = str(humidity_link) + " %"
            self.wind_speed.text = str(wind_speed) + " mph"
            self.wind_direction.text = str(wind_direction)
            self.lastBuildDate.text = str(lastBuild)
            self.description.text = str(descr)
            print data
        except urllib2.URLError as err:
            popup = Popup(id='popup')
            popup.title_align = 'center'
            popup.title = 'Network Error'
            popup.size_hint = None, None
            popup.size = Window.width * 0.5, Window.height * 0.5
            boxcontent = BoxLayout(orientation='vertical')
            boxcontent.add_widget(Label(text='An error in connection occurred'))
            popup.content = boxcontent
            popup.open()
            self.parent.current = 'launcher'

    def on_pre_enter(self, *args):
        self.get_weather("Buea")


class ScreenManagerInstance(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagerInstance, self).__init__(**kwargs)


class MainApp(App):
    def build(self):
        screenmanager = ScreenManagerInstance()

        return screenmanager

    def on_start(self):
        return True
    def on_pause(self):
        return True


if __name__ == '__main__':
    MainApp().run()
