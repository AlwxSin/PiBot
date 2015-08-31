# coding=utf-8
__author__ = 'Alwx'

from extTools import send_text, send_photo, throw_cubes, reboot, abort, toggle_play, log_event, unauthorized
from dictionaries import commands, dnd, kate, unknown
from random import randint
from settings import ADMIN_IDs


def run_command(offset, name, from_id, cmd):
    cmd = cmd.lower()
    cmd = cmd.split(' ')
    main = cmd[0]

    if main in commands:
        send_text(from_id, commands[cmd[0]])

    elif main in dnd:
        send_text(from_id, throw_cubes(cmd))

    elif main in [u'катя', u'kate']:
        i = randint(0, len(kate)-1)
        send_text(from_id, kate[i])

    elif main == '/reboot':
        if from_id in ADMIN_IDs:
            log_event('Reboot by %s' % name)
            send_text(from_id, u'Ушел покурить')
            reboot()
        else:
            unauthorized(from_id, name, cmd)

    elif main == '/abort':
        if from_id in ADMIN_IDs:
            log_event('Aborted by %s' % name)
            send_text(from_id, u'Выключаюсь')
            abort()
        else:
            unauthorized(from_id, name, cmd)

    elif main == '/pause':
        speed = toggle_play()
        if speed:
            text = 'play'
        else:
            text = 'pause'
        send_text(from_id, text)

    else:
        i = randint(0, len(unknown)-1)
        send_text(from_id, unknown[i])
