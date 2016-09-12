# Natural sorting
# Thanks to Timo Reunanen (http://code.activestate.com/recipes/285264-natural-string-sorting/#c7)

import re
import unicodedata

def natural(key):
    """natural(key)
    usage:
    >>> sorted(unsorted, key=natural)
    >>> unsorted.sort(key=natural)

    if key is unicode, it simplifies key to ascii using unicodedata.normalize.
    """

    if isinstance(key, str):
        key=key.lower()

        return [int(n) if n else s for n,s in re.findall(r'(\d+)|(\D+)', key)]
    else:
        return key
