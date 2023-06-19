numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']

def get_unit(x):
    if isinstance(x, str):
        for char in range(len(x)):
            if x[char] not in numbers:
                return x[char:]
    else:
        return x

def delete_unit(x):
    if isinstance(x, str):
        for char in range(len(x)):
            if x[char] not in numbers:
                return float(x[0:char:1])
        return float(x)
    else:
        return float(0)
