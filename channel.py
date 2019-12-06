from members import *

class channel:

    def __init__(self, name):
        self.channel_name = name
        self.participants = []


    def add_user(self, user, conn): #returns if user was added-if not added it's because they were in channel
        self.participants.append(members(user,conn))


    def remove_user(self, user): #Returns true if removed, false if user not found
        removed = False
        for x in self.participants:
            if x.nickname == user:
                self.participants.remove(x)
                removed = True

        return removed

    def check_if_user_in_channel(self, user):
        for x in self.participants:
            if x.nickname == user:
                return True
        return False

    def display(self):
        print(self.channel_name)



