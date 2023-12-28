# -*- coding: utf-8 -*-

import os
from pathlib import Path
from string import ascii_letters

import more_itertools as mit
from retry import retry

"""Main module."""

def _ellipses() -> str:
    if os.name == "nt":  # windows
        return "---"
    else:
        return "..."

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
    chunk_size = int(os.environ.get("KEYNAME_CHOP_CHUNK_SIZE", 200))
    if chunk_size <= 1:
        raise ValueError(
            f"""bad chunk size {chunk_size}, KEYNAME_CHOP_CHUNK_SIZE={
                os.environ.get('KEYNAME_CHOP_CHUNK_SIZE', None)
            }""",
        )
    chopped_path = os.sep.join(
        f"{_ellipses()}{os.sep}".join(
            map("".join, mit.chunked(path_part, chunk_size))
        )
        for path_part in keyname_string.split(os.sep)
    )

    # handle file extention getting chopped apart
    # solution:
    # 1. remove last .../
    # 2. rechop basename every 100 characters
    # 3. remove last .../
    # to ensure at least 100 contiguous characters at end
    if (
        os.path.dirname(chopped_path).endswith(_ellipses())
        and all(
            c in "." + ascii_letters for c in os.path.basename(chopped_path)
        )
        and os.path.dirname(chopped_path)[:-3].rstrip(
            ascii_letters
        ).endswith(".")
    ):
        # remove last occurence of .../
        chopped_path = chopped_path[::-1].replace(f"{os.sep}{_ellipses()}", "", 1)[::-1]

        rechopped_basename = f"{_ellipses()}{os.sep}".join(
            map("".join, mit.chunked(os.path.basename(chopped_path), 100))
        )[::-1].replace(f"{os.sep}{_ellipses()}", "", 1)[::-1] # remove last .../

        chopped_path = Path(os.path.dirname(chopped_path)) / rechopped_basename


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
    return str(Path(chopped_path))

def rejoin( chopped_keyname_path ):
    return chopped_keyname_path.replace(f"{_ellipses()}{os.sep}", "")
