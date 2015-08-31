# coding=utf-8
__author__ = 'Alwx'
import time
import requests
import subprocess
import sys
from random import randint
from settings import FULL_URL, PI_KODI_URL
from dictionaries import get_player, play_pause


def log_event(text):
    """
    Процедура логгирования
    """
    # ToDo: 1) Запись лога в файл

    event = '%s >> %s' % (time.ctime(), text)

def send_text(chat_id, text, counter=0):
    """Отправка текстового сообщения по chat_id
    ToDo: повторная отправка при неудаче"""
    log_event('Sending to %s: %s' % (chat_id, text))
    data = {'chat_id': chat_id, 'text': text}
    request = requests.post(FULL_URL + '/sendMessage', data=data)
    if not request.status_code == 200:
        if counter < 5:
            send_text(chat_id, text, counter + 1)
        return False
    return request.json()['ok']


def send_photo(chat_id, photo_id):
    """Отправка фото по его идентификатору выбранному контакту"""
    data = {'chat_id': chat_id, 'photo': photo_id}
    request = requests.post(FULL_URL + '/sendPhoto', data=data)
    return request.json()['ok']


def throw_cubes(cmd):
    if len(cmd) > 1:
        k = int(cmd[1])
    else:
        k = 1

    dice = int(cmd[0][1:])
    k = int(k)

    result = 0
    for i in range(k):
        result += randint(1, dice)

    return result


def reboot():
    command = "/usr/bin/sudo /sbin/reboot"

    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]


def abort():
    sys.exit(0)


def toggle_play():
    player = requests.post(PI_KODI_URL, json=get_player)

    if player.status_code == 200:
        play_pause['params']['playerid'] = player.json()['result'][0]['playerid']

        toggle = requests.post(PI_KODI_URL, json=play_pause)
        if toggle.status_code == 200:
            return toggle.json()['result']['speed']


def unauthorized(from_id, name, cmd):
    send_text(from_id, "You're not authorized to use this command!")
    log_event('Unauthorized: %s %s %s' % (from_id, name, cmd))
