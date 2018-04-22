class Item:
    def __init__(self, name, price, id):
        self._name = name
        self._price = price
        self._id = id

    def returnPrice(self):
        return self._price

    def returnName(self):
        return self._name

    def returnID(self):
        return self._id