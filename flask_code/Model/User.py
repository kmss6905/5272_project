class User:
    def __init__(self, user_email, passwd_hash=None,authenticated=False):
        self.user_email = user_email
        self.passwd_hash = passwd_hash
        self.authenticated = authenticated

    def __repr__(self):
        r = {
            'user_email': self.user_email,
            'passwd_hash': self.passwd_hash,
            'authenticated': self.authenticated,
        }
        return str(r)

    def can_login(self, pass_hash):
        return self.passwd_hash == pass_hash

    def is_active(self):
        return True

    def get_id(self):
        return self.user_id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False