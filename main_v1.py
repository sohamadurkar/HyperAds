from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.video import Video
from kivy.uix.videoplayer import VideoPlayer
from kivy.clock import Clock
from geopy.distance import geodesic
import random

# Set store's location (e.g., a supermarket)
STORE_LOCATION = (51.5007, -0.1246)  # London Eye (example)

class AdBox(BoxLayout):
    def __init__(self, **kwargs):
        super(AdBox, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Add video player
        self.video = VideoPlayer(source='ad.mp4', state='stop', options={'eos': 'stop'})
        self.add_widget(self.video)

        # Start checking location every 5 seconds
        Clock.schedule_interval(self.check_location, 5)

    def get_taxi_location(self):
        # Simulated GPS (you can replace with real GPS later)
        lat = 51.5000 + random.uniform(-0.001, 0.001)
        lon = -0.1246 + random.uniform(-0.001, 0.001)
        return (lat, lon)

    def check_location(self, dt):
        taxi_loc = self.get_taxi_location()
        distance = geodesic(taxi_loc, STORE_LOCATION).meters
        print(f"Taxi Location: {taxi_loc} | Distance to store: {int(distance)}m")

        if distance < 300:  # If within 300 meters
            if self.video.state != 'play':
                print("Within geofence — Playing ad.")
                self.video.state = 'play'
        else:
            if self.video.state != 'stop':
                print("Outside geofence — Stopping ad.")
                self.video.state = 'stop'

class IAlgApp(App):
    def build(self):
        return AdBox()

if __name__ == '__main__':
    IAlgApp().run()
