import numpy.random as random

class WAI:
    def __init__(self):
        self.data = []
        self.persons = {}
        with open("whoami_data.txt", encoding="utf-8") as whi_data:
            for line in whi_data:
                self.data.append(line[:-1])
            
    def get_object(self):
        return random.choice(self.data)

    def add_person(self, id, character):
        self.persons.update({id : character})

    def get_user_answer(self, id):
        return self.persons.get(id, False)

    def remove_person(self, id):
        return self.persons.pop(id, False)
