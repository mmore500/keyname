=====
Usage
=====

Keyname is built around the following file name convention:

- key/value pairs are constructed with :code:`=` between the key and value

- key/value pairs are joined by :code:`+`

- key/value pairs are ordered alphanumerically by key

  - keys beginning with :code:`_` are ordered after keys not beginning with :code:`_`

  - the :code:`ext` (extension) key is always placed last

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
  
  # returns {'key' : 'val', 'ext' : '.txt'}
  kf.unpack('path/to/key=val+ext=.txt')
