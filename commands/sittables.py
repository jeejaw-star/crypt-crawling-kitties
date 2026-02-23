from evennia import Command, CmdSet

class CmdSit(Command):
    """
    Sit down.
    """
    key = "sit"
    def func(self):
        self.obj.do_sit(self.caller)

class CmdStand(Command):
     """
     Stand up.
     """
     key = "stand"
     def func(self):
         self.obj.do_stand(self.caller)


class CmdSetSit(CmdSet):
    priority = 1
    def at_cmdset_creation(self):
        self.add(CmdSit)
        self.add(CmdStand)