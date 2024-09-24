from network.models import Person


class PersonParser:
    @classmethod
    def parse(cls, data: dict) -> Person:
        return Person()
