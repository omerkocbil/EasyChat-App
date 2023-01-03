from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.event import EventDispatcher
from kivy.properties import ColorProperty, OptionProperty
from kivy.utils import get_color_from_hex as gch

from core import font_definitions


class ThemeManager(EventDispatcher):
    primary_color = ColorProperty("feb437")

    primary_light = ColorProperty("feb437")

    primary_dark = ColorProperty("feb437")

    bg_normal = ColorProperty()

    bg_light = ColorProperty()

    bg_dark = ColorProperty()

    text_color = ColorProperty()

    theme_style = OptionProperty("Light", options=["Light", "Dark"])

    def on_theme_style(self, instance, value):
        Window.clearcolor = gch("F5F5F5" if value == "Light" else "121212")
        if value == "Light":
            self.text_color = "2F2F31"
            self.bg_light = "F5F5F5"
            self.bg_dark = "F5F5F5"
            self.bg_normal = "F5F5F5"
        else:
            self.text_color = "2F2F31"
            self.bg_light = "F5F5F5"
            self.bg_dark = "F5F5F5"
            self.bg_normal = "F5F5F5"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        font_definitions.register_fonts()
        Clock.schedule_once(
            lambda x: self.on_theme_style(None, self.theme_style)
        )


class ThemableBehavior(EventDispatcher):
    def __init__(self, **kwargs):
        self.theme_cls = App.get_running_app().theme_cls
        super().__init__(**kwargs)
