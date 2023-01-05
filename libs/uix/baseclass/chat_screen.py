from kivy.animation import Animation
from kivy.properties import DictProperty, ListProperty, StringProperty
from kivy.clock import Clock

from components.boxlayout import PBoxLayout
from components.dialog import PDialog
from components.screen import PScreen
from components.toast import toast
from key import aes_key as AES

import urllib3
http = urllib3.PoolManager()

import json


class ChatScreen(PScreen):
    user = DictProperty()
    chat = DictProperty()
    aes = DictProperty()
    title = StringProperty()
    chat_logs = ListProperty()
    partipicant = ListProperty()

    def on_enter(self, *args):
        Clock.schedule_interval(self.check_notification, 0.5)
    
    def on_leave(self, *args):
        Clock.unschedule(self.check_notification)
    
    def check_notification(self, time):
        GET_NOTIF_API = "http://54.144.168.5/api/notification/"

        resp = http.request('GET', GET_NOTIF_API, fields={'username': self.user['username']})
        resp = json.loads(resp.data.decode('utf-8'))
        
        if resp['notification']:
            chat = resp['info'].get(str(self.chat['id']))
            if chat is not None:
                if chat['sender'] != self.user['username']:
                    self.chat_logs.append(
                        {
                            "text": '[color=f5f5f5]' + '[u]'+self.get_name_and_title(chat['sender'])[0]+'[/u]' + '\n' + '[color=000000]' + AES.decrypt(chat['last_message'], key=self.aes['key'], nonce=self.aes['nonce']),
                            "send_by_user": False,
                        }
                    )
        
                GET_CONV_API = "http://54.144.168.5/api/getgroupchat"

                resp = http.request('GET', GET_CONV_API, fields={'id': self.chat['id'], 'username': self.user['username']})
                resp = json.loads(resp.data.decode('utf-8'))
        
        self.scroll_to_bottom()
    
    def get_name_and_title(self, username):
        GET_USER_API = "http://54.144.168.5/api/user"

        resp = http.request('GET', GET_USER_API)
        data = json.loads(resp.data.decode('utf-8'))
        
        for user in data:
            if user['username'] == username:
                return user['name'], user['title']

    def send(self, text):
        if not text:
            toast("Lütfen mesaj girin!")
            return

        SEND_MSG_API = "http://54.144.168.5/api/send/"
        data = {'chat_id': self.chat['id'],
                'username': self.user['username'],
                'message': AES.encrypt(text, self.aes['key'], self.aes['nonce'])}

        resp = http.request('GET', SEND_MSG_API, fields=data)
        
        self.chat_logs.append(
            {"text": '[color=000000]' + text, "send_by_user": True, "pos_hint": {"right": 1}}
        )
        
        self.scroll_to_bottom()
        self.ids.field.text = ""
    
    def receive(self, chat_id, is_group):
        if is_group:
            GET_CONV_API = "http://54.144.168.5/api/getgroupchat"

            resp = http.request('GET', GET_CONV_API, fields={'id': chat_id, 'username': self.user['username']})
            data = json.loads(resp.data.decode('utf-8'))

            self.partipicant = data['users']
            for message in data['messages']:
                self.chat_logs.append(
                    {
                        "text": '[color=000000]' + AES.decrypt(message['message'], key=self.aes['key'], nonce=self.aes['nonce']) if self.user['username']==message['username'] else '[color=f5f5f5]' + '[u]'+self.get_name_and_title(message['username'])[0]+'[/u]' + '\n' + '[color=000000]' + AES.decrypt(message['message'], key=self.aes['key'], nonce=self.aes['nonce']),
                        "send_by_user": True if self.user['username']==message['username'] else False,
                        "pos_hint": {"right": 1} if self.user['username']==message['username'] else {"left": 1}
                    }
                )
            
        self.scroll_to_bottom()

    def show_user_info(self):
        about_partipicants = "Katılımcılar:\n"
        for p in self.partipicant:
            name, title = self.get_name_and_title(p)
            about_partipicants += title + " - " + name + "\n"

        PDialog(
            content=UserInfoDialogContent(
                about = "Bu grup TK1878 sefer sayılı uçuş için görevli olan tüm personelin rahatça iletişim kurabilmesi adına otomatik olarak oluşturulmuştur.",
                image = "assets/images/thy.png",
                partipicant = about_partipicants,
            )
        ).open()

    def scroll_to_bottom(self):
        rv = self.ids.chat_rv
        box = self.ids.box
        if rv.height < box.height:
            Animation.cancel_all(rv, "scroll_y")
            Animation(scroll_y=0, t="out_quad", d=0.5).start(rv)


class UserInfoDialogContent(PBoxLayout):
    about = StringProperty()
    image = StringProperty()
    partipicant = StringProperty()
