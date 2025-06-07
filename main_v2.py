import os
# Force Kivy to use ffpyplayer for video decoding
os.environ['KIVY_VIDEO'] = 'ffpyplayer'

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.videoplayer import VideoPlayer
from kivy.clock import Clock

class LocationSimulator:
    """Simulate GPS coordinates moving around"""
    def __init__(self):
        self.locations = [
            (51.4816, -3.1791),  # Near the store
            (51.4820, -3.1800),
            (51.4900, -3.2000),  # Far
            (51.4818, -3.1793),  # Close again
        ]
        self.index = 0

    def get_location(self):
        loc = self.locations[self.index]
        self.index = (self.index + 1) % len(self.locations)
        return loc

class AdApp(App):
    def build(self):
        self.store_lat = 51.4816
        self.store_lon = -3.1791
        self.threshold = 0.0015  # ~150m radius

        self.location_sim = LocationSimulator()
        self.layout = BoxLayout()

        video_path = 'ad.mp4'

        if not os.path.exists(video_path):
            print("❌ Video file not found:", video_path)
        else:
            print("✅ Video file found:", video_path)

        self.player = VideoPlayer(
            source=video_path,
            state='stop',
            options={'eos': 'loop'},
            allow_fullscreen=True
        )
        self.layout.add_widget(self.player)

        Clock.schedule_interval(self.check_location_and_play, 5)  # Every 5 seconds
        return self.layout

    def check_location_and_play(self, dt):
        lat, lon = self.location_sim.get_location()
        print(f"📍 Current simulated location: ({lat}, {lon})")

        if abs(lat - self.store_lat) < self.threshold and abs(lon - self.store_lon) < self.threshold:
            print("📢 Store nearby! Playing ad...")
            self.player.state = 'play'
        else:
            print("❌ Not near the store. Pausing ad.")
            self.player.state = 'stop'

if __name__ == '__main__':
    AdApp().run()
