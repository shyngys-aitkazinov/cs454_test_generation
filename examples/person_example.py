import random 

class Person:
    def __init__(self, name: str , age: int, sex: str, interest: str) -> None:
        self.name = name 
        self.age = age
        self.sex = sex
        self.interest = interest
        self.phrase = None

    def allowed_to_drink(self, country: str) -> bool:
        if country == "USA":
            if  self.age >= 21:
                return True
            else: 
                return False
        else: 
            if self.age >= 18:
                return True
            else: 
                return False
    
    def calculate_lifespan(self) ->int:
        if self.interest == "fun":
            return self.age + len(self.name) + 3 * len(self.sex)
        else: 
            age = self.age + len(self.sex)
            for i in range(len(self.name)):
                if random.random() > 0.5:
                    age +=1
                else:
                    age -= 1
            return age
    
    def catch_phrase(self, phrase) -> None:
        self.phrase = phrase
    
    def introduce_self(self) -> str:
        print (f'I am {self.name} and my ctach phrase is {self.phrase}')

        if self.phrase != None:
            return self.name + " "+ self. phrase 
        else:
            return self.name

def who_is_older(Person1: Person, Person2: Person) -> Person:
    return max(Person1.age, Person2.age)
