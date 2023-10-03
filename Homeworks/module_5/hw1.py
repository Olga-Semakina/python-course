import keyword


class KeyValueStorage:

    def __init__(self, filepath):
        self.__read_file_to_dict__(filepath)

    def __getitem__(self, x):
        return self.__dict__[x]

    def __read_file_to_dict__(self, filepath):
        with open(filepath) as input:
            for line in input:
                key_value = line.replace("\n", "").split("=")
                self.__set__custom_attr__(key_value[0], key_value[1])

    def __set__custom_attr__(self, key, init_value):
        if (keyword.iskeyword(key) or key.isnumeric()):
            raise ValueError("Incorrect key identifier was found", key)

        try:
            value = int(init_value)
        except ValueError:
            value = init_value
        self.__dict__.setdefault(key, value)
