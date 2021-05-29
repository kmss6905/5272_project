class User:
    def __init__(self, dao):
        self.id = dao['id']
        self.user_nickname = dao['user_nickname']
        self.user_phone_number = dao['user_phone_number']
        self.user_email = dao['user_email']