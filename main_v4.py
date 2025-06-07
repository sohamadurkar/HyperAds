from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.video import Video
from kivy.clock import Clock
from kivy.core.window import Window

# Set the window size (optional)
Window.size = (800, 480)

class LocationVideoPlayer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        # Define location names and coordinates
        self.location_data = [
            {"name": "Cardiff University Main Building", "coords": (51.4875, -3.1795)},
            {"name": "Cardiff Students' Union (STORE)", "coords": (51.4881, -3.1788)},
            {"name": "Bute Park", "coords": (51.4995, -3.1805)},
            {"name": "Cathays Railway Station", "coords": (51.4878, -3.1789)},
        ]
        self.index = 0

        # Big bold label for current location
        self.location_label = Label(
            text="Starting location...",
            font_size='30sp',
            bold=True,
            size_hint=(1, 0.2),
            color=(1, 0, 0, 1)  # Red color
        )
        self.add_widget(self.location_label)

        # Video player widget
        self.video = Video(source='ad.mp4', state='stop', options={'eos': 'stop'})
        self.video.size_hint = (1, 0.8)
        self.add_widget(self.video)

        # Start checking location every few seconds
        Clock.schedule_interval(self.update_location, 5)

    def update_location(self, dt):
        location = self.location_data[self.index]
        coords = location["coords"]
        name = location["name"]

        # Update label with big bold location name
        self.location_label.text = f"[b]{name}[/b]"
        self.location_label.markup = True  # Enable bold text

        print(f"\U0001F4CD Current simulated location: {coords} - {name}")

        # Store detection
        store_coords = self.location_data[1]["coords"]  # Students’ Union
        near_store = self.is_nearby(coords, store_coords)

        if near_store:
            print("\U0001F4E3 Store nearby! Showing ad...")
            if not self.video.parent:
                self.add_widget(self.video)  # Add video widget back to the layout
            if self.video.state == 'stop':
                self.video.state = 'play'  # Play the video
        else:
            print("\U0001F697 Not near store. Clearing screen...")
            if self.video.parent:
                self.remove_widget(self.video)  # Remove video widget from the layout

        self.index = (self.index + 1) % len(self.location_data)

    def is_nearby(self, loc1, loc2, threshold=0.0008):  # ~80m radius
        lat1, lon1 = loc1
        lat2, lon2 = loc2
        return abs(lat1 - lat2) < threshold and abs(lon1 - lon2) < threshold


class VideoApp(App):
    def build(self):
        return LocationVideoPlayer()


if __name__ == '__main__':
    VideoApp().run()
