class Passenger:
    def __init__(self, passenger_id, nombre, email, telefono):
        self._id = passenger_id
        self._nombre = nombre
        self._email = email
        self._telefono = telefono

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
    def telefono(self):
        return self._telefono

    def __str__(self):
        return f"Passenger(id={self._id}, nombre={self._nombre}, email={self._email})"