from PersonFactory import year_died


class Person:
    def __init__(self, year_born,year_died,first_name,
                 last_name,gender,spouse,is_founding_ancestor):
        self.year_born = year_born
        self.year_died = year_died
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.spouse = None #initialize default as no spouse
        self.children = []
        self.is_founding_ancestor = is_founding_ancestor

    #Accessors
    def get_year_born(self):
        return self.year_born

    def get_year_died(self):
        return self.first_name

    #get age based on year input
    def get_age(self,curr_year):
        if curr_year <= self.year_born:
            return 0
        return curr_year - self.year_born

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_gender(self):
        return self.gender

    def get_spouse(self):
        return self.spouse

    def has_spouse(self):
        return self.spouse is not None

    def get_children(self):
        return self.children

    def is_first_ancestor(self):
        return self.is_founding_ancestor

    #mutators
    def set_spouse(self,spouse):
        self.spouse = spouse

    def add_child(self,child):
        self.children.append(child)

    def can_have_children(self,curr_year):
        age = self.get_age(curr_year)
        return 25 <= age <= 45

