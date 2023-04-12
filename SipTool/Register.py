class Register:
    """
    注册器：维护一个字典，里边储存在注册上的账号和相应的端口
    register_dict={ “1501”：5061，
                    “1502”：5063 }
    """
    def __init__(self):
        self.register_dict = {}
        self.all_account = set()

    def __contains__(self, item):
        if item in self.register_dict.values():
            return True
        else:
            return False

    def is_register(self, account: str):
        """
        查询账号是否注册在表中
        :param account: 查询的账号
        :return:
        """
        if account in self.all_account:
            return True
        else:
            return False

    def add(self, account: str, sip_port: int):
        """
        添加账号和端口到注册表中
        :param account: 添加的账号
        :param sip_port: 添加的端口
        :return:
        """
        if not self.is_register(account):
            self.all_account.add(account)
            self.register_dict[account] = sip_port

    def update(self, account: str, sip_port: int):
        """
        更新注册表中账号对应的端口
        :param account: 更新的账号
        :param sip_port: 更新的端口
        :return:
        """
        if not self.is_register(account):
            return False
        self.register_dict[account] = sip_port

    def query(self, account):
        """
        查询账号注册的端口
        :param account:
        :return:
        """
        if self.is_register(account):
            return self.register_dict[account]
        else:
            return False

    def remove(self, account):
        """
        移除注册表中的账号
        :param account:移除的账号
        :return:
        """
        if self.is_register(account):
            self.register_dict.pop(account)
            return True
        else:
            return False
