from typeclasses.objects import Object
class Flower(Object):
    key = "flower"
    def on_object_creation(self):
        self.db.desc = f"This is a pretty {self.key}."
class Rose(Flower):
    key = "rose"
