

def request(question, choices):
    print(question)
    print("\n\t".join(str(1 + i)+" : " + str(choice) for i, choice in enumerate(choices)))
    ans = input("\t --> ")
    while not ans.isnumeric() and 1 <= int(ans) <= len(choices):
        ans = input("\t --> ")
    return int(ans) - 1


def answer_yn(question, default=True):
    print(question + " (default: "+("yes" if default else "no")+")")
    ans = input("\t --> ")
    while ans.lower() not in ["", "yes", "y", "no", "n"]:
        ans = input("\t --> ")
    if ans == "":
        return default
    else:
        return ans in ["yes", "y"]
