# -*- coding: utf-8 -*-

import os

"""Main module."""


def unpack(filename):

    return {
        k : v
        for k, v in [
            str.split('=', 1) # maxsplit=1 
            if '=' in str else (str, '')
            for str in os.path.basename(filename).split('+')
        ] + [ ('_', filename) ]
    }


def pack(dict):

    regular = {}
    underscore = {}
    ext = {}

    stringified = {str(k): str(v) for k, v in dict.items()}
    stringified.pop('_', None)

    for k, v in stringified.items():

        assert not any(c in k or c in v for c in ('=', '+'))

        if k == 'ext':
            ext[k] = v
        elif k.startswith('_'):
            underscore[k] = v
        else:
            regular[k] = v

    return '+'.join([ k + '=' + v
        for k, v in
        sorted(regular.items())
        + sorted(underscore.items())
        + sorted(ext.items())
    ])
