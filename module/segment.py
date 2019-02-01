# segment each list eqaul value
def segment(data):
    lookup = {}
    result = []
    for element in data:
        if element not in lookup:
            target = lookup[element] = [element]
            result.append(target)
        else:
            lookup[element].append(element)
    return result
