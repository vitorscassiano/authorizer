def Any(cls):
    class Any(cls):
        def __eq__(self, other):
            return True
    return Any()
