import os
import json

class json_read(dict):
    def __getitem__(self, k):
        try:
            return dict.__getitem__(self, k)
        except KeyError:
            return dict.__getitem__(self, str(k))

def json_memoized(fname, verbose=False):
    def _load():
        with file(fname, 'rb') as f:
            # here, we use json_read as a proxy
            # to allow re-indexing with an integer
            # in a dictionary
            return json.load(f, object_hook=json_read)

    def _dump(obj):
        with file(fname, 'wb') as f:
            return json.dump(obj, f)

    if not os.path.isfile(fname):
        MEMO = {}
        _dump(MEMO)
    else:
        MEMO = _load()

    def func_decorator(f):
        def new_func(arg):
            if arg not in MEMO:
                MEMO[arg] = f(arg)
                if verbose:
                    print '%r -> %r' % (arg, MEMO[arg])
                _dump(MEMO)
            
            return MEMO[arg]
        return new_func

    return func_decorator
        
