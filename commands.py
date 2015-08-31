# coding=utf-8
__author__ = 'Alwx'

from extTools import send_text, send_photo, throw_cubes, reboot, abort, toggle_play
from dictionaries import commands, dnd, kate, unknown
from random import randint


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
        reboot(name)
        send_text(from_id, u'Ушел покурить')

    elif main == '/abort':
        send_text(from_id, u'Выключаюсь')
        abort(name)

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
