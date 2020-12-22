import readline
from datetime import datetime

def read_date(prompt="Date [yyyy, mm, dd]: ", display_current=True, today_default=False):
    fmt = '%Y, %m, %d'
    if display_current:
        print("Today's date is: " + datetime.today().strftime(fmt))
    i = str(input(prompt))
    if i == "" and today_default:
        return datetime.today()
    try:
        return datetime.strptime(i, fmt)
    except ValueError:
        print("Incorrect format. Please enter date in " + fmt + " format.")
        return read_date(prompt)

def read_number(prompt=None, range=None, integer=False):
    if not prompt:
        prompt = "Enter "
        if integer:
            prompt += "an integer "
        else:
            prompt += "a number "
        if range:
            prompt += "from " + str(range[0]) + " to " + str(range[1])
        prompt += ": "
    try:
        if integer:
            n = int(input(prompt))
        else:
            n = float(input(prompt))
        if range and (n < range[0] or n > range[1]):
            raise ValueError()
        return n
    except ValueError:
        print("Invalid input.")
        return read_number(prompt, range, integer)

def confirm_prompt(prompt="Yes/No [y/n]: ", retry=True): # if retry is set to false, will return False if input is invalid
        r = input(prompt).strip().lower()
        if r == "y" or r == "yes" or r == "ye":
            return True
        elif (not retry) or r == "n" or r == "no":
            return False
        else:
            print("Invalid input.")
            return confirm_prompt(prompt)

def menu_select(choices, prompt="Select one of the following: "):
    if not choices:
        return None
    for c in range(0,len(choices)):
        print(str(c) + ") " + choices[c])

    r = input(prompt).strip()
    try:
        i = int(r)
        return i
    except ValueError:
        print("Invalid response.")
        return menu_select(choices, prompt)
    
