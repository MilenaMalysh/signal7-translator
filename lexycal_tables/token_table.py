
import deserializer


class TokenTable(list):
    def __init__(self, name, start_id=0):
        super(TokenTable, self).__init__(deserializer.parse_ascii(name))
        if self.__len__() == 0 and start_id:
            self.start_id = start_id
        else:
            self.start_id = self.__len__()

    def find(self, value):
        return next((item for item in self if item['body'] == value), None)

    def __contains__(self, item):
        return any(elem['id'] == item['id'] for elem in self) or any(elem['body'] == item['body'] for elem in self)


class IndentTable(TokenTable):
    start_id = 0

    def __init__(self, name, start_id=0, output_name=""):
        super(TokenTable, self).__init__(deserializer.parse_table(name))
        self.output_name = output_name
        if self.__len__() == 0:
            self.start_id = start_id
        else:
            self.start_id = self[-1]['id']

    def register(self, x):
        if type(x) is str:
            self.append(dict([('id', self.start_id), ('body', x)]))
            self.start_id += 1
            return self[-1]
        else:
            raise TypeError('indent must be str.')

    def serialize(self):
        with open(self.output_name, 'wb') as f:
            for elem in self:
                f.write(str(elem['body']) + " " + str(elem['id']) + "\n")