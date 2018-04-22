from Item import Item

class Ticket(Item):
    def __init__(self, name, price, id):
        Item.__init__(self, name, price, id)

