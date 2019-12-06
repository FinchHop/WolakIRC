from channel import *

class channel_list:

    def __init__(self):
        self.list_of_channels = []
        self.list_of_channels.append(channel("General"))

    def check_valid_channel(self, channel):
        for x in self.list_of_channels:
            if x.channel_name == channel:
                return True
        
        return False

    def check_user_in_channel(self, channel, user):
        for x in self.list_of_channels:
            if x.channel_name == channel:
                return x.check_if_user_in_channel(user)
        

    def add_channel(self, channel_name):
        self.list_of_channels.append(channel(channel_name))

    def remove(self, channel_name):
        for x in self.list_of_channels:
            if x.channel_name == channel_name:
                self.list_of_channels.remove(x)
                return

    def remove_user_all_channels(self, user):
        for x in self.list_of_channels:
            if x.check_if_user_in_channel(user) == True:
                x.remove_user(user)

    def remove_user_single_channel(self, channel, user):
        for x in self.list_of_channels:
            if x.channel_name == channel:
                return x.remove_user(user)

    def display_all(self):
        chans = ""
        for x in range(len(self.list_of_channels)):
            chans += self.list_of_channels[x].channel_name + "\n"
        return chans


    def add_user_to_channel(self, channel_name, user, conn):
        for x in self.list_of_channels:
            if x.channel_name == channel_name:
                x.add_user(user, conn)
                return True
        
        return False

    def return_users_in_channel(self, channel_name):
        users = ""
        for x in range(len(self.list_of_channels)):
            if self.list_of_channels[x].channel_name == channel_name:
                for j in range(len(self.list_of_channels[x].participants)):
                    if self.list_of_channels[x].participants[j] != None:
                        users += self.list_of_channels[x].participants[j].nickname + "\n"

        return users

    def return_conns_in_channel(self, channel_name):
        conns = []
        for x in self.list_of_channels:
            if x.channel_name == channel_name:
                for y in x.participants:
                    conns.append(y.conn)
        return conns


