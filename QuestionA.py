# Function that return true if first_line and second_line overlap. first_line and second_line is a tuple where the first element can be the start or end of the line and the second element is the other one
# (Float, Float) (Float, Float) -> Bool
def overlap(first_line, second_line):
    x1, x2 = first_line
    x3, x4 = second_line
    if x1 < x2:
        if ((x1 <= x3) and (x3 <= x2)) or ((x1 <= x4) and (x4 <= x2)):
            return True
    else:
        if ((x2 <= x3) and (x3 <= x1)) or ((x2 <= x4) and (x4 <= x1)):
            return True
    return False
