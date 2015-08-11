import csv
from random import randint
import linecache



def picker():
    with open("answers.csv", "r") as answers:
        print "hello"


def clue_to_dict(clue_str):
    raw_list = clue_str.split(",")
    # print raw_list
    if len(raw_list) == 4:
        clue_dict = {"Category": raw_list[0], "Value": raw_list[1], "Clue": raw_list[2], "Answer": raw_list[3]}
    else:
        category = []
        clue = []
        answer = raw_list[-1]
        for i in range(len(raw_list)):
            if raw_list[i][0] == "$" or raw_list[i] == "Final Jeopardy!":
                value_index = i
            else: pass
        for i in range(0,value_index):
            category.append(raw_list[i])
        for i in range(value_index+1,len(raw_list)-1):
            clue.append(raw_list[i])
        final_category = ",".join(category)
        final_clue = ",".join(clue)
        clue_dict = {"Category": final_category, "Value": raw_list[value_index], "Clue": final_clue, "Answer": answer}
    return clue_dict


def printer(clue_dict):
    print clue_dict["Category"] + " for " + clue_dict["Value"]
    print clue_dict["Clue"]
    raw_input("")
    print clue_dict["Answer"]


def random_question():
    clue = None
    while clue is None:
        choice = 1
        while choice % 2 != 0:
            choice = randint(0,309764) # 608325 is the number of lines in wordlist.txt
        clue = linecache.getline("answers.csv", choice).strip("\n")
    return clue


def test():
    choice = 271596
    clue = linecache.getline("answers.csv", choice)
    return clue.strip("\n")


if __name__ == "__main__":
    print "JEOPARDY!"
    print
    print "Press enter to move the game along."
    print 'Type "quit" to quit.'
    print
    while True:
        try:
            printer(clue_to_dict(random_question()))
        except UnboundLocalError:
            print "ERROR! moving along..."
            printer(clue_to_dict(random_question()))
        print "----------"
        keep_going = raw_input("")
        if keep_going == "quit":
            break