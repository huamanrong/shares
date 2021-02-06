class LoginServer:
    def __init__(self, root, account, password, frame_page, logger):
        self.root = root
        self.account = account
        self.password = password
        self.frame_page = frame_page
        self.logger = logger

    def login(self):
        print('hello world')
