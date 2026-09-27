class TeamMember:
    def __init__(self, id, nombre, email, slack_user, rol):
        self._id = id
        self._nombre = nombre
        self._email = email
        self._slack_user = slack_user
        self._rol = rol

    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre

    @property
    def email(self):
        return self._email

    @property
    def slack_user(self):
        return self._slack_user

    @property
    def rol(self):
        return self._rol

    def __str__(self):
        return f"{self._nombre} <{self._email}> [{self._rol}]"
