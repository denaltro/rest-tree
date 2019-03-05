class Leaf:
    _text = None
    _parent_id = None

    def __init__(self, id, name):
        if not id or not isinstance(id, str):
            raise ValueError(
                'Could not make leaf model without required attributes')

        if not name or not isinstance(name, str):
            raise ValueError(
                'Could not make leaf model without required attributes')

        self.id = id
        self.name = name

    @property
    def text(self):
        if not self._text:
            self._text = '{} {}'.format(self.id, self.name)
        return self._text

    @property
    def parent_id(self):
        if not self._parent_id:
            self._parent_id = self._get_parent_id()
        return self._parent_id

    def _get_parent_id(self):
        if not self.id:
            return None

        arr = self.id.split('.')
        if len(arr) == 1:
            return None
        return '.'.join(arr[:-1])

    def json(self):
        return self.__dict__

    @staticmethod
    def get_with_parents_array(id):
        if not id:
            return None

        arr = id.split('.')
        length = len(arr)
        if length == 1:
            return None

        result = []
        for i in range(0, length):
            result.append('.'.join(arr[0:i+1]))
        return result
