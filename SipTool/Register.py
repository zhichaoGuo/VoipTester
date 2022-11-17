class Register:
    def __init__(self):
        self.register_dict = {}
        self.all_account = set()

    def __contains__(self, item):
        if item in self.register_dict.values():
            return True
        else:
            return False

    def is_register(self, account: str):
        if account in self.all_account:
            return True
        else:
            return False

    def add(self, account: str, sip_port: int):
        if not self.is_register(account):
            self.all_account.add(account)
            self.register_dict[account] = sip_port

    def update(self, account: str, sip_port: int):
        if not self.is_register(account):
            return False
        self.register_dict[account] = sip_port

    def query(self, account):
        if self.is_register(account):
            return self.register_dict[account]
        else:
            return False

    def remove(self, account):
        if self.is_register(account):
            self.register_dict.pop(account)
            return True
        else:
            return False
