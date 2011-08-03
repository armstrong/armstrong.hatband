from contextlib import contextmanager


# TODO: find a home for this
@contextmanager
def preserve_attr(obj, attr):
    original = getattr(obj, attr)
    yield
    setattr(obj, attr, original)
