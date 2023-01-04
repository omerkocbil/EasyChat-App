import os
import __main__

from kivy.animation import Animation
from kivy.properties import ColorProperty

from components.screen import PScreen
from kivy.clock import Clock
from components.toast import toast
from key import rsa_key as RSA

import requests
import json


class LoginScreen(PScreen):
    bg_color = ColorProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_color = self.theme_cls.primary_color
        
    def on_enter(self, *args):
        Clock.schedule_once(self.show_form, 3)

    def show_form(self, time):
        Animation(bg_color=self.theme_cls.bg_normal, d=0.4).start(self)
        Animation(
            d=0.7, scale=0.75, text_color=self.theme_cls.primary_color
        ).start(self.ids.title)
        Animation(d=0.7, pos_hint={"center_y": 0.75}).start(self.ids.intro)
        self.ids.form.disabled = False

    def sign_in(self, username, password):
        LOGIN_POST_API = "http://54.144.168.5/api/login/"
        data = {'username': username,
                'password': password}
        resp = requests.post(url=LOGIN_POST_API, data=data)
        resp = resp.json()
        
        if resp['auth']:
            with open(__main__.get_path('assets/users.json')) as f:
                users = json.load(f)
            
            for i, user in enumerate(users['users']):
                if user['username'] == username:
                    name = user['name']
                    if user.get('public_rsa') is None:
                        public_rsa, private_rsa = RSA.generate_public_and_private_key()
                        #self.update_user(username, public_rsa)
                        self.write_rsa_keys_users_db(i, public_rsa, private_rsa)
                    break
            
            self.ids.username.text = ""
            self.ids.password.text = ""
            
            self.manager.set_current("home")
            toast("Başarıyla giriş yapıldı!")
            
            home_screen = self.manager.get_screen("home")
            home_screen.user = {'username': username, 'name': name}
            home_screen.receive()
            
    def update_user(self, username, public_rsa):
        UPDATE_USER_API = "http://54.144.168.5/api/user/"
        data = {'username': username,
                'public_rsa': public_rsa}
        resp = requests.patch(url=UPDATE_USER_API, data=data)
        print(resp.json())
    
    def write_rsa_keys_users_db(self, index, public_rsa, private_rsa):
        with open(__main__.get_path('assets/users.json')) as file:
            file_data = json.load(file)
            
            file_data['users'][index]['public_rsa'] = public_rsa
            file_data['users'][index]['private_rsa'] = private_rsa
            file.seek(0)
            
            json.dump(file_data, file, indent=4)
