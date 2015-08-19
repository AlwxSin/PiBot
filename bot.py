# coding=utf-8
__author__ = 'Alwx'

from settings import ADMIN_IDs, FULL_URL
from extTools import log_event
from commands import send_text, run_command
import requests

requests.packages.urllib3.disable_warnings()  # Подавление InsecureRequestWarning, с которым я пока ещё не разобрался

offset = 0  # ID последнего полученного обновления


def check_updates():
    """Проверка обновлений на сервере и инициация действий, в зависимости от команды"""
    global offset
    data = {'offset': offset + 1, 'limit': 10, 'timeout': 5}

    try:
        r = requests.post(FULL_URL + '/getUpdates', data=data)
    except:
        log_event('Error getting updates')
        return False

    if not r.status_code == 200:
        return False
    if not r.json()['ok']:
        return False
    for update in r.json()['result']:
        offset = update['update_id']

        offset_file = open('offset', 'r')  # Грязный хак. TODO пока не будет отслеживания
        old_offset = int(offset_file.read())
        offset_file.close()

        if old_offset >= offset:
            continue

        offset_file = open('offset', 'w')
        offset_file.write(str(offset))
        offset_file.close()

        if 'message' not in update or 'text' not in update['message']:
            log_event('Unknown update: %s' % update)
            continue

        from_id = update['message']['chat']['id']
        if 'username' in update['message']['chat']:
            username = update['message']['chat']['username']
        elif 'first_name' in update['message']['chat']:
            username = update['message']['chat']['first_name']
        elif 'last_name' in update['message']['chat']:
            username = update['message']['chat']['last_name']

        message = update['message']['text']

        parameters = (offset, username, from_id, message)

        if from_id not in ADMIN_IDs and message.startswith('/'):
            send_text(from_id, "You're not authorized to use me!")
            log_event('Unauthorized: %s' % update)
            continue

        log_event('Message (id%s) from %s (id%s): "%s"' % parameters)

        run_command(*parameters)
