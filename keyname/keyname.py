# -*- coding: utf-8 -*-

import os

"""Main module."""


def unpack(filename):

    return {
        k : v
        for k, v in [
            str.split('=')
            for str in os.path.basename(filename).split('+')
        ] + [ ('_', filename) ]
    }


def pack(dict):

    regular = {}
    underscore = {}
    ext = 'None'

    stringified = {str(k): str(v) for k, v in dict.items()}
    stringified.pop('_', None)

    for k, v in stringified.items():

        assert not any(c in k or c in v for c in ('=', '+'))
        assert len(k)

        if k == 'ext':
            ext = str(v)
        elif k[0] == '_':
            underscore[k] = v
        else:
            regular[k] = v

    return '+'.join([ k + '=' + v
        for k, v in
        sorted(regular.items())
        + sorted(underscore.items())
        + [('ext', ext)]
    ])
