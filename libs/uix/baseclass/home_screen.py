from kivy.properties import ListProperty, DictProperty

from components.boxlayout import PBoxLayout
from components.dialog import PDialog
from components.screen import PScreen
from key import aes_key as AES

import requests
import json

import os
import __main__

class HomeScreen(PScreen):

    chats = ListProperty()
    user = DictProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def on_enter(self, *args):
        self.receive()
    
    def receive(self):
        self.chats = []
        
        GET_CHATS_API = "http://54.144.168.5/api/getchats/"
        resp = requests.get(url=GET_CHATS_API)
        self.data = resp.json()
        
        #self.data = sorted(self.data, key=lambda x: x['last_activity'])
        
        for chats in self.data:
            aes_key, aes_nonce = self.get_aes_keys(chats["id"])
            is_exist, message, sender = self.check_notification(chats['id'])
            
            message_sender = ""
            if is_exist:
                if sender==self.user['username']:
                    message_sender = "Sen"
                else:
                    message_sender = self.get_name_and_title(sender)[0]
            else:
                if chats['last_sender']==self.user['username']:
                    message_sender = "Sen"
                else:
                    message_sender = self.get_name_and_title(chats['last_sender'])[0]
            
            chat_data = {
                "text": chats["name"],
                "secondary_text": message_sender + ': ' + AES.decrypt(message, key=aes_key, nonce=aes_nonce) if is_exist else message_sender + ': ' + AES.decrypt(chats["last_message"], key=aes_key, nonce=aes_nonce),
                "image": "assets/images/thy.png",
                "unread_messages": is_exist,
                "on_release": lambda x={
                    "name": chats["name"],
                    **chats,
                }: self.goto_chat_screen(x),
            }
            self.chats.append(chat_data)

    def get_aes_keys(self, chat_id):
        with open(__main__.get_path('assets/chats.json')) as file:
            file_data = json.load(file)
        
        for chat in file_data['chats']:
            if chat['chat_id'] == chat_id:
                return chat['AES_KEY'], chat['AES_nonce']
    
    def get_name_and_title(self, username):
        GET_USER_API = "http://54.144.168.5/api/user"
        resp = requests.get(url=GET_USER_API)
        data = resp.json()
        
        for user in data:
            if user['username'] == username:
                return user['name'], user['title']
    
    def check_notification(self, chat_id):
        GET_NOTIF_API = "http://54.144.168.5/api/notification/"
        resp = requests.get(url=GET_NOTIF_API, params={'username': self.user['username']})
        resp = resp.json()
        
        is_exist = False
        message, sender = "", ""
        if resp['notification']:
            if resp['info'].get(str(chat_id)) is not None:
                is_exist = True
                message = resp['info'][str(chat_id)]['last_message']
                sender = resp['info'][str(chat_id)]['sender']
        
        return is_exist, message, sender
    
    def goto_chat_screen(self, chat_data):
        self.manager.set_current("chat")
        chat_screen = self.manager.get_screen("chat")
        chat_screen.user = self.user
        chat_screen.chat = chat_data
        chat_screen.chat_logs = []
        chat_screen.title = chat_data["name"]
        
        aes_key, aes_nonce = self.get_aes_keys(chat_data['id'])
        chat_screen.aes = {'key': aes_key, 
                           'nonce': aes_nonce}
        
        chat_screen.receive(chat_data['id'], is_group=chat_data['is_group'])

    def show_menu(self):
        PDialog(content=MenuDialogContent()).open()


class MenuDialogContent(PBoxLayout):
    pass