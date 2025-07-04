import hashlib

class MyDict:
    __values: list
    __keys: list

    def __init__(self):
        self.__values = []
        self.__keys = []

    def my_hash(self, x):
        key_bytes = str(x).encode('utf-8')
        hash_object = hashlib.sha224(key_bytes)
        return int(hash_object.hexdigest(), 16)

    def __getitem__(self, key):
        for i, my_key in enumerate(self.__keys):
            if self.my_hash(my_key) == self.my_hash(key):
                return self.__values[i]
        raise ValueError("Key not found.")

    def __setitem__(self, key, value):
        for i, my_key in enumerate(self.__keys):
            if self.my_hash(my_key) == self.my_hash(key):
                self.__values[i] = value
                return
        self.__keys.append(key)
        self.__values.append(value)

    def __len__(self):
        return len(self.__values)

    def __repr__(self):
        s = "{"
        for i, my_key in enumerate(self.__keys):
            s += str(my_key) + ": " + str(self.__values[i]) + ", "
        s = s.rstrip(", ") + "}"
        return s

    def get(self, key, default=None):
        for i, my_key in enumerate(self.__keys):
            if self.my_hash(my_key) == self.my_hash(key):
                return self.__values[i]
        return default

#тест
if __name__ == "__main__":
    d = MyDict()
    d["name"] = "Ярослав"
    d["age"] = 19

    print(d)                      
    print(d["name"])               
    print(d.get("age"))           
    print(d.get("unknown"))        
    print(d.get("unknown", "N/A")) 
    print(len(d))                  
