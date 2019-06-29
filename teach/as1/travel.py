"""

"""

__author__ = ""
__date__ = ""


from destinations import Destinations


def main():
    
    # Task 1: Ask questions here
    def input_name():
        username = raw_input('What is your name?')
        return 'Hi,%s!' % username

# Task 2+: Add comparison logic here
    def one_continent():
        print("which continent would you like to travel to?")
        #for destination in Destinations().get_all():
        continent_dict = {"asia":"1","africa":"2","north america":"3","south america":"4","europe":"5","oceania":"6","antarctica":"7"}
        print("Which continent would you like to travel to?")
        print("  1) Asia")
        print("  2) Africa")
        print("  3) North America")
        print("  4) South America")
        print("  5) Europe")
        print("  6）Oceania")
        print("  7) Antarctica")
        you_choose = raw_input('> ')
        return ([k for k,v in continent_dict.items() if v==you_choose])

    for destination in Destinations().get_all():
           # Task 2+: Output final answer here

if __name__ == "__main__":
    main()

