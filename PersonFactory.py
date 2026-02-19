#reading csv files
#get methods
#read files methods
import random
import pandas as pd
import numpy as np
from sympy.physics.units import frequency

import Person

#converts year into corresponding decade. "YYYYs"
def decades(year):
    return str((year // 10) * 10) + "s"

class PersonFactory:
    def __init__(self):
        self.birth_marriage = None
        self.first_names = None
        self.last_names = None
        self.gender_name_prob = None
        self.life_expectancy = None
        self.rank_prob = None

        #load files
        self.read_files()

    def read_files(self):
        print("Reading Files...")
        self.birth_marriage = pd.read_csv("birth_and_marriage_rates.csv")
        self.first_names = pd.read_csv("first_names.csv")
        self.last_names = pd.read_csv("last_names.csv")
        self.gender_name_prob = pd.read_csv("gender_name_probability.csv")
        self.life_expectancy = pd.read_csv("life_expectancy.csv")
        self.rank_prob = pd.read_csv("rank_to_probability.csv")

    def make_progenitor(self, first_name,last_name,gender,year_born):
        year_died = self.make_year_died(year_born)
        first_name,last_name, gender = first_name,last_name,gender
        return Person.Person(year_born,year_died,first_name,last_name,gender)

    #creates a direct descendant
    def make_descendant(self,year_born,last_name):
        #initialize descendant information
        year_died = self.make_year_died(year_born)
        first_name, gender = self.make_first_name_and_gender(year_born)
        return Person.Person(year_born,year_died,first_name,last_name,gender)

    # first name (gendered) returns first name and gender
    def make_first_name_and_gender(self, year_born):
        #compute decade
        decade = decades(year_born)
        #select gender by probability and decade
        gend_nm = self.gender_name_prob
        gender_pb = gend_nm[gend_nm["decade"] == decade]
        gender = np.random.choice(gender_pb["gender"],p=gender_pb["probability"])

        #choose name
        first_nm = self.first_names
        nm_sel = first_nm[(first_nm['gender'] == gender) & (first_nm['decade'] == decade)]

        #normalize probabilities to sum = 1
        # https://numpy.org/doc/stable/reference/random/generated/numpy.random.choice.html
        probs = nm_sel['frequency'] / nm_sel['frequency'].sum()
        name = np.random.choice(nm_sel['name'],p=probs)
        return name, gender

    # last name if no direct ancestors
    def make_last_name(self, year_born):
        # compute decade
        decade = decades(year_born)
        last_name_pool = self.last_names.loc[self.last_names['Decade'] == decade]

        # initialize rank probabilities
        ranks = [float(elem) for elem in self.rank_prob.columns.tolist()]
        # normalize probabilities to sum = 1
        total = sum(ranks)
        norm_ranks = [num / total for num in ranks]
        # return chosen name
        # https://numpy.org/doc/stable/reference/random/generated/numpy.random.choice.html
        return np.random.choice(last_name_pool['LastName'], p=norm_ranks)

    def make_year_died(self,year_born):
        # locate Period life expectancy at birth
        life_ex = self.life_expectancy
        exp = life_ex.loc[life_ex['Year'] == year_born, "Period life expectancy at birth"].iloc[0]
        # randomly generate length +/- 10 years
        death_year = exp + year_born
        return death_year + np.random.randint(-10, 10)

    # bool: will they have a spouse
    def will_have_spouse(self,year_born):
        # compute decade
        decade = decades(year_born)
        birth_marr = self.birth_marriage
        # locate marriage rate based on decade
        marr_rate = birth_marr.loc[birth_marr['decade'] == decade, "marriage_rate"].iloc[0]
        # decide if there is a spouse based on marr rate
        return random.random() < marr_rate

    #makes a spouse for person by that person's birth year
    def make_spouse(self,year_born,max_year):
        #initialize spouse information
        sp_year_born = year_born + np.random.randint(-10,10)
        #if year_born > max_year, no spouse yet
        if sp_year_born > max_year:
            return None
        sp_year_died = self.make_year_died(sp_year_born)
        sp_first_name,sp_gender = self.make_first_name_and_gender(sp_year_born)
        sp_last_name = self.make_last_name(sp_year_born)

        #create spouse person object
        return Person.Person(sp_year_born,sp_year_died,sp_first_name,
                             sp_last_name,sp_gender)


    # returns a list of children birth_years
    def make_child_birth_years(self, year_born, has_spouse):
        decade = decades(year_born)
        birth_rate = self.birth_marriage.loc[self.birth_marriage['decade'] == decade, "birth_rate"].iloc[0]
        # determine number of children by rate
        num_children = round(birth_rate + np.random.uniform(-1.5, 1.5))
        # with no spouse, should be 1 less
        if not has_spouse:
            num_children = max(0, num_children - 1)
        # return empty list for no children
        if num_children == 0:
            return []
        # pick a random year if 1 child
        if num_children == 1:
            return [int(year_born + np.random.randint(25,45))]
        # https://stackoverflow.com/questions/6683690/making-a-list-of-evenly-spaced-numbers-in-a-certain-range-in-python
        # find evenly spaced birth years for 2+ children
        else:
            children = np.round(np.linspace(year_born + 25, year_born + 45, num=num_children, dtype=int))
            return children