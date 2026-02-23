from typeclasses.objects import Object
from commands.command import Command
class CmdQuests(Command):
    """View your current quests.
    
    Usage:
        quests"""
    key = "quests"
    def func(self):
        self.caller.msg(self.caller.db.quests)

class defaultQuest(Object):
    """The default quest class for Crypt Crawlin' Kitties"""

    def at_object_creation(self):
        self.key = "quest"
        self.objective=None

class fetchQuest(defaultQuest):
    """A simple quest where you go get something for someone"""

    def at_object_creation(self):
        self.key = "fetch"
        self.objective="<item to get>"
        self.asker=None
        self.reward="10 gold coins"
        self.taker=None

    def at_quest_completion(self):
        from evennia import create_object
        if self.taker.location == self.asker.location:
            for i in range(10):
                create_object("coin",location=self.taker)
    
    def at_quest_taken(self):
        self.taker=self.location

class CmdFinishQuest(Command):
    """Finish a quest.
    
    Usage:
        finish <quest name>"""
    key = "finish"
    def func(self):
        x=self.caller.db.quests
        if self.args in x:
            a=x.index(self.args)
            y=x[a]
            y.at_quest_completion()
