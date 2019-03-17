=======
keyname
=======


.. image:: https://img.shields.io/pypi/v/keyname.svg
        :target: https://pypi.python.org/pypi/keyname

.. image:: https://img.shields.io/travis/mmore500/keyname.svg
        :target: https://travis-ci.org/mmore500/keyname

.. image:: https://readthedocs.org/projects/keyname/badge/?version=latest
        :target: https://keyname.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Easily pack and unpack metadata in a filename.


* Free software: MIT license
* Documentation: https://keyname.readthedocs.io.


Usage
--------

Keyname is built around the following file name convention:

- key/value pairs are constructed with :code:`=` between the key and value

- key/value pairs are joined by :code:`+`

- key/value pairs are ordered alphanumerically by key

  - keys beginning with :code:`_` are ordered after keys not beginning with :code:`_`

  - the :code:`ext` (extension) key is always placed last

  - the key :code:`_` is reserved for the original filename

For example,  :code:`key1=val1+key2=val2+_key3=val3+ext=.txt`.

.. code-block:: python3

  from keyname import keyname as kn

  # returns 'key1=val1+key2=val2+_key3=val3+ext=.txt'
  kn.pack({
    'key2' : 'val2',
    'ext' : '.txt',
    'key1' : 'val1',
    '_key3' : 'val3',
  })

  # returns {'key' : 'val', 'ext' : '.txt', '_' : 'path/to/key=val+ext=.txt'}
  kf.unpack('path/to/key=val+ext=.txt')


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
