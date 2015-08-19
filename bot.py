# coding=utf-8
__author__ = 'Alwx'

from settings import ADMIN_IDs, FULL_URL
from extTools import log_event
from commands import send_text, run_command
import requests

requests.packages.urllib3.disable_warnings()  # Подавление InsecureRequestWarning, с которым я пока ещё не разобрался

offset = 0  # ID последнего полученного обновления


def check_updates():
    print 'checking'
    """Проверка обновлений на сервере и инициация действий, в зависимости от команды"""
    global offset
    data = {'offset': offset + 1, 'limit': 10, 'timeout': 5}

    try:
        request = requests.post(FULL_URL + '/getUpdates', data=data)
    except:
        log_event('Error getting updates')
        return False

    if not request.status_code == 200:
        return False
    if not request.json()['ok']:
        return False
    for update in request.json()['result']:
        offset = update['update_id']

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

        if from_id not in ADMIN_IDs and message[0] is '/':
            send_text("You're not authorized to use me!", from_id)
            log_event('Unauthorized: %s' % update)
            continue

        log_event('Message (id%s) from %s (id%s): "%s"' % parameters)

        run_command(*parameters)
