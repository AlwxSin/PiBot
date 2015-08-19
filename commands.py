# coding=utf-8
__author__ = 'Alwx'

from extTools import send_text, send_photo, throw_cubes, reboot
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

    # elif main == '/reboot':
    #     reboot(name)
    #     send_text(from_id, u'Ушел покурить')

    else:
        i = randint(0, len(unknown)-1)
        send_text(from_id, unknown[i])
