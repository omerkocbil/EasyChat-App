from kivy.lang import Builder
from kivy.properties import BooleanProperty, ColorProperty, StringProperty

from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior

from components.boxlayout import PBoxLayout
from core.theming import ThemableBehavior

Builder.load_string(
    """
<ListItem>
    adaptive_height: True
    padding: [dp(8), dp(8)]
    text_color: 1, 1, 1, 1
    text_size: self.width, None

    canvas.before:
        Color:
            rgba:
                self.theme_cls.primary_dark if self.send_by_user \
                else self.theme_cls.primary_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius:
                [dp(8), dp(8), (dp(-5), dp(5)), dp(8)] if self.send_by_user \
                else [(dp(-5), dp(5)), dp(8), dp(8), dp(8)]

    PBoxLayout:
        orientation: 'vertical'
        spacing: dp(7)
        adaptive_height: True
        pos_hint: {"center_y": .5}

        PLabel:
            text: root.username
            underline: True
            adaptive_height: True
            text_color: 'f5f5f5'
            shorten: True
            shorten_from: 'right'
            text_size: self.width, None

        PLabel:
            text: root.text
            font_name: 'LexendLight'
            text_color: '000000'
            adaptive_height: True
            shorten_from: 'right'
            text_size: self.width, None


<-ChatBubble>
    adaptive_height: True
    padding: [dp(8), dp(8)]
    text_color: 1, 1, 1, 1
    text_size: self.width, None

    canvas.before:
        Color:
            rgba:
                self.theme_cls.primary_dark if self.send_by_user \
                else self.theme_cls.primary_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius:
                [dp(8), dp(8), (dp(-5), dp(5)), dp(8)] if self.send_by_user \
                else [(dp(-5), dp(5)), dp(8), dp(8), dp(8)]

    PBoxLayout:
        orientation: 'vertical'
        spacing: dp(7)
        adaptive_height: True
        pos_hint: {"center_y": .5}

        PLabel:
            text: root.username
            underline: True
            adaptive_height: True
            text_color: 'f5f5f5'
            shorten: True
            shorten_from: 'right'
            text_size: self.width, None

        PLabel:
            text: root.text
            font_name: 'LexendLight'
            text_color: '000000'
            adaptive_height: True
            shorten_from: 'right'
            text_size: self.width, None
    """
)


class ListItem(ButtonBehavior, ThemableBehavior, PBoxLayout):
    bg_color = ColorProperty([0, 0, 0, 0])

    username = StringProperty()

    text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_color = self.theme_cls.bg_normal
        self.theme_cls.bind(theme_style=self._update_bg_color)

    def _update_bg_color(self, *args):
        self.bg_color = self.theme_cls.bg_normal

    def on_state(self, instance, value):
        Animation(
            bg_color=self.theme_cls.bg_dark
            if value == "down"
            else self.theme_cls.bg_normal,
            d=0.1,
            t="in_out_cubic",
        ).start(self)

class ChatBubble(ListItem):
    username = StringProperty()
    
    text = StringProperty()

    send_by_user = BooleanProperty()











