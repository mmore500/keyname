# -*- coding: utf-8 -*-

import os

"""Main module."""


def unpack(filename):

    return {
        key : value
        for key, value in (
            str.split('=')
            for str in os.path.basename(filename).split('+')
        )
    }


def pack(dict):

    regular = {}
    underscore = {}
    ext = None

    for k,v in dict.items():

        assert not any(c in str(k) or c in str(v) for c in ('=', '+'))

        if k == 'ext':
            ext = v
        elif k[0] == '_':
            underscore[k] = v
        else:
            regular[k] = v

    return '+'.join([ str(k) + '=' + str(v)
        for k,v in
        sorted(regular.items())
        + sorted(underscore.items())
        + [('ext', ext)]
    ])
