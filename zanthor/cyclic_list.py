# file: cycling list.
# purpose: a pointer to the current item is needed.
#     A goto_next method is needed.  Which cycles over the next idx.


try:
    from UserList import UserList
except ImportError:
    try:
        from collections import UserList
    except ImportError:
        UserList = list


class cyclic_list(UserList):
    def __init__(self, *args, **kwargs):
        UserList.__init__(self, *args, **kwargs)
        self.idx = 0
        if not hasattr(self, "data"):
            self.data = self

    def __iter__(self):
        self.idx = 0
        return self

    def __next__(self):
        if self.idx >= len(self.data):
            raise StopIteration
        result = self.data[self.idx]
        self.idx += 1
        return result

    def next(self):
        """increments the cursor, and returns the new current idx."""

        self.idx += 1

        if self.idx >= len(self.data):
            self.idx = 0

        return self.idx

    def nextone(self):
        i = self.next()
        return self.data[i]

    def prev(self):
        """decrements the cursor, and returns the new current idx."""
        self.idx -= 1

        if self.idx < 0:
            self.idx = len(self.data) - 1

        return self.idx

    def cur(self):
        """returns the element at the current cursor."""
        return self.data[self.idx]

    def set_cur(self, idx):
        """Sets the current cursor to the given idx."""
        self.idx = idx


if __name__ == "__main__":
    c = cyclic_list([1, 2, 3, 4])
    print((c.idx))
    next(c)
    print((c.idx))
    next(c)
    print((c.idx))
    next(c)
    print((c.idx))
    next(c)
    print((c.idx))

    for x in range(5):
        c.prev()
        print((c.idx))

    for x in range(5):
        print(c.nextone())
