from typeclasses.objects import Object
from commands.command import Command
from evennia import CmdSet
from evennia.utils import interactive
class BaseNPC(Object):
    """A basic npc."""
    def on_object_creation(self):
        self.db.key=None
        self.db.words=[""]
        self.db.seller=False
    def speak_to(self,talker):
        import random
        talker.msg(f"{self.db.key} says {random.choice(self.db.words)}")
class CmdTalk(Command):
    """Talk to a NPC.
    
    Usage:
        talk to <npc's name>"""
    key = "talk to"
    def func(self):
        x=self.caller.location.search(self.args.strip())
        if x:
            x.speak_to(self.caller)
class Blacksmith(BaseNPC):
    """A blacksmith."""

    def at_object_creation(self):
        self.db.key="blacksmith"
        self.db.words=["Hm? I'm busy right now. Come talk to me later.", "Go get me some metal and I'll give you 10 gold."]
        self.db.objects={"sword":[50,100]}
        self.db.seller=True
        self.db.inventory=["sword","shield","horseshoe"]
    def speak_to(self, talker):
        import random
        text=random.choice(self.db.words)
        talker.msg(text)
        if text.startswith("Go"):
            make_quest("get iron","iron","get",self,talker)
    @interactive
    def haggle(self,object,haggler):
        import random
        from evennia import create_object
        x=self.objects[object][0]
        y=self.objects[object][1]
        while True:
            price=random.randint(x,y)
            price2=yield(f"How about {price}?")
            price2=int(price2)
            if price2 < price:
                y=price2
            elif  price2>price:
                x=price2
            else:
                haggler.msg("We'll take it!")
                create_object(object,location=haggler)
                break
class CmdBuy(Command):
    key="buy"
    def parse(self):
        self.args=self.args.strip()
        a,b= self.args.split(" from ")
        self.caller.msg(a)
        self.caller.msg(b)
        self.a=a
        self.b=b

    def func(self):
        from evennia import create_object
        if self.args:
            x=self.caller.location.search(self.b)
            if self.a in x.inventory:
                create_object(key=self.a,location=self.caller.location)

class NPCCommands(CmdSet):
    def on_cmdset_creation(self):
        self.add(CmdTalk)

def make_quest(name,objective,type,asker,taker):
    from . import quests
    from evennia import create_object
    if type=="get":
        x=quests.fetchQuest()
        x.objective=objective
        x.asker=asker
        x.taker=taker
        try:
            taker.db.quests.append(x)
        except:
            taker.db.quests=[x]


