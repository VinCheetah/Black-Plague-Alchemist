from math import inf

input_str = "\t --> "

def request(question, choices):
    print(question)
    for i, choice in enumerate(choices):
        print("\t"+str(1 + i)+" : " + str(choice) + "\n")
    ans = input(input_str)
    while not ans.isnumeric() and 1 <= int(ans) <= len(choices):
        ans = input(input_str)
    return int(ans) - 1


def answer_yn(question, default=True):
    print(question + " (default: "+("yes" if default else "no")+")")
    ans = input(input_str)
    while ans.lower() not in ["", "yes", "y", "no", "n"]:
        ans = input(input_str)
    if ans == "":
        return default
    else:
        return ans in ["yes", "y"]


def request_number(question, min_val=-inf, max_val=inf, ans_type=int):
    print(question)
    ans = input(input_str)
    while not ans.isnumeric() and min_val <= ans_type(ans) <= max_val:
        ans = input(input_str)
    return ans_type(ans)

