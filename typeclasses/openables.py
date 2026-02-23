from typeclasses.objects import Object
from random import choice
class Chest(Object):
    def on_object_creation(self):
        self.db.contains = choice(["coin","coin","coin","sword","coin"])

    