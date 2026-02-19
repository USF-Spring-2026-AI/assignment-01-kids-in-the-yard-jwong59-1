#2 person attributes

import Person
import PersonFactory
import PersonFactory as pf
import random

#methods:
    #geenerating family tree
    #respond to user queries
class FamilyTree:

    def __init__(self):
        #initialize factory instance
        self.factory = pf.PersonFactory()
        #first ancestors setup
        self.progenitor1 = self.factory.make_progenitor("Desmond","Jones","Male",1950)
        self.progenitor2 = self.factory.make_progenitor("Molly","Smith","Female",1950)
        #set progenitors as spouses
        self.progenitor1.set_spouse(self.progenitor2)
        self.progenitor2.set_spouse(self.progenitor1)

        # list of all descendants of ancestors
        self.all_family = []

        #add to family list
        self.all_family.append(self.progenitor1)
        self.all_family.append(self.progenitor2)

    #accessors:
    def get_total_family(self):
        return len(self.all_family)

    def generate_descendant_tree(self, max_year):
        """
        :param max_year: int
        :return: None

        Generate tree starting with progenitor couple
        BFS to process by generation
        """
        print(f"Generating family tree...")
        #add one of the progenitor to queue randomly
        progenitor = random.choice([self.progenitor1,self.progenitor2])
        queue = [progenitor]
        while queue:
            curr_person: Person = queue.pop()
            year_born = curr_person.get_year_born()

            # Spouse probabilistic assignment, if not progenitor
            elder_parent_age = curr_person.get_year_born()
            if curr_person != progenitor and self.factory.has_spouse(year_born):
                #set spouse details
                spouse = self.factory.make_spouse(year_born,max_year)

                if spouse:
                    curr_person.set_spouse(spouse)
                    spouse.set_spouse(curr_person)
                    #pick the older of the two spouses
                    elder_parent_age = min(spouse.get_year_born(),
                                           curr_person.get_year_born())
                    self.all_family.append(spouse)

            #determine num of children & birth years
            child_birth_yrs = self.factory.make_child_birth_years(elder_parent_age,
                                                                  curr_person.has_spouse())

            #generate children
            for birth in child_birth_yrs:
                # Stop tree generation once we pass the max_year window
                if birth > max_year:
                    continue
                #create child with unique child name
                child = self.factory.make_descendant(birth,curr_person.get_last_name())
                while not child.is_unique_name(curr_person):
                    name, gender = self.factory.make_first_name_and_gender(birth)
                    child.set_first_name(name)
                    child.set_gender(gender)
                #add to parents
                curr_person.add_child(child)
                #added to all people list
                self.all_family.append(child)
                #add child to queue
                queue.append(child)

        print(f"Family Tree Generated!")

    #returns dictionary of duplicate names
    def get_duplicates(self):
        names_map = {}

        #populate people into hashmap
        for person in self.all_family:
            full_name = person.get_full_name()
            names_map[full_name] = names_map.get(full_name,0)+1

        #filter hashmap for duplicates, return list
        return [name for name,val in names_map.items() if val > 1]

    #total people by year
    def get_total_by_year(self):
        total_by_year = {}

        #populate hashmap by decades
        for person in self.all_family:
            #group by decade category
            decade = PersonFactory.decades(person.get_year_born())[:-1]
            total_by_year[decade] = total_by_year.get(decade,0)+1
        return total_by_year

#main menu loop
def main():
    tree = FamilyTree()
    tree.generate_descendant_tree(max_year=2120)
    print("=" * 20)
    while True:
        print(f"Are you interested in:")
        print(f"(T)otal number of people in the tree")
        print(f"Total (N)umber of people in the tree by decade")
        print(f"All (D)uplicated names in the tree")
        print(f"(E)xit menu.")

        user_input = input("> ")
        choice = user_input.strip().upper()
        #exit option
        if choice == "E":
            break
        #print total people option
        elif choice == "T":
            total_family = tree.get_total_family()
            print(f"The tree contains {total_family} people total.")
        #print duplicates option
        elif choice == "D":
            duplicates = tree.get_duplicates()
            number = len(duplicates)
            #grammar logic
            prep, s  = "are", "s"
            if number == 1:
                are, s = "is", ""
            print(f"There {prep} {number} duplicate name{s} in the tree: ")

            if number >= 1:
                for name in duplicates:
                    print(f" * {name}")
        #print total number of people by year option
        elif choice == "N":
            total_by_decade = tree.get_total_by_year()
            print(f"Number of people by decade: ")
            #print year: number of people
            for decade in sorted(total_by_decade.keys()):
                print(f"{decade} : {total_by_decade[decade]} ")
        elif choice == "Q":
            for people in tree.all_family:
                print(people.get_full_name())
        #invalid choice case
        else:
            print(f"<{choice}> is an invalid choice")

        print(f"\nReturning to main menu...")
        print("="*20)

if __name__ == "__main__":
    main()