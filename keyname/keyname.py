# -*- coding: utf-8 -*-

import os
from string import ascii_letters

import more_itertools as mit
from retry import retry

"""Main module."""


def unpack(filename, source_attr=True):

    res = {
        k : v
        for k, v in [
            str.split('=', 1) # maxsplit=1
            if '=' in str else (str, '')
            for str in os.path.basename(filename).split('+')
        ]
    }

    if source_attr:
        res['_'] = filename

    return res

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

def demote( keyname_string ):
    assert '~' not in keyname_string
    assert '%' not in keyname_string
    return keyname_string.replace(
        '+', '~'
    ).replace(
        '=', '%'
    )

def promote( demoted_keyname_string ):
    assert '+' not in demoted_keyname_string
    assert '=' not in demoted_keyname_string
    return demoted_keyname_string.replace(
        '~', '+'
    ).replace(
        '%', '='
    )

def chop( keyname_string, mkdir=False, logger=None ):
    chopped_path = "/".join(
        ".../".join(
            map("".join, mit.chunked(path_part, 200))
        )
        for path_part in keyname_string.split("/")
    )

    # handle file extention getting chopped apart
    # solution:
    # 1. remove last .../
    # 2. rechop basename every 100 characters
    # 3. remove last .../
    # to ensure at least 100 contiguous characters at end
    if (
        os.path.dirname(chopped_path).endswith("...")
        and all(
            c in "." + ascii_letters for c in os.path.basename(chopped_path)
        )
        and os.path.dirname(chopped_path)[:-3].rstrip(
            ascii_letters
        ).endswith(".")
    ):
        # remove last occurence of .../
        chopped_path = chopped_path[::-1].replace("/...", "", 1)[::-1]

        rechopped_basename = ".../".join(
            map("".join, mit.chunked(os.path.basename(chopped_path), 100))
        )[::-1].replace("/...", "", 1)[::-1]  # remove last .../

        chopped_path = f"{os.path.dirname(chopped_path)}/{rechopped_basename}"

    if mkdir:
        retry(
            tries=10,
            delay=1,
            max_delay=10,
            backoff=2,
            jitter=(0, 4),
            logger=logger,
        )(os.makedirs)(
            os.path.dirname(chopped_path), exist_ok=True
        )
    return chopped_path

def rejoin( chopped_keyname_path ):
    return chopped_keyname_path.replace(".../", "")
