
class plex_signin(object):
    def __init__(self):
        """Class constructor"""
        self.plex_network=None
        self.identifier=None

    def start(self):
        self.display_pin()

    def set_authentication_target(self, plex_network):
        self.plex_network = plex_network

    def display_pin(self, failure=False):
        self.data = self.plex_network.get_signin_pin()
        self.identifier = self.data['id']



    def submit_pin(self):
        result = self.plex_network.check_signin_status(self.identifier)

        if result:
            pass
        else:
            print("Not Successful signed in")
            self.display_pin(True)
