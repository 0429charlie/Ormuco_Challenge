def greaterthan(s1, s2):
    try:
        int1 = None
        if s1[0] == "-":
            int1 = float(s1[1:])
            int1 = int1 * (-1)
        elif s1[0] == "+":
            int1 = float(s1[1:])
        else:
            int1 = float(s1)
    except:
        return "Please enter an string that start with number or -/+ sign and only include number after first character for the first input"
    try:
        int2 = None
        if s2[0] == "-":
            int2 = float(s2[1:])
            int2 = int2 * (-1)
        elif s2[0] == "+":
            int2 = float(s2[1:])
        else:
            int2 = float(s2)
    except:
        return "Please enter an string that start with number or -/+ sign and only include number after first character for the second input"
    if (int1 == int2):
        return "equal"
    elif (int1 > int2):
        return "greater"
    else:
        return "less"
