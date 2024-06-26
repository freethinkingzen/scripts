import sys
import json

def getObjectDifferences(object1, object2, fileName1, fileName2):

    differences = {}

    for key, value in object1.items():
        # Check if object2 contains same key as object1
        if key not in object2:
            differences[key] = {fileName1 : value, fileName2: "***NOT FOUND***"}

        # Check if both values are equal
        elif object1[key] != object2[key]:

            # Recursion if item is a dictionary
            if isinstance(object1[key], dict) and isinstance(object2[key], dict):
                differences[key] = getObjectDifferences(object1[key], object2[key], fileName1, fileName2)

            # Recursion if item is list
            elif isinstance(object1[key], list) and isinstance(object2[key], list):
               differences[key] = getListDifferences(object1[key], object2[key], fileName1, fileName2);

            else:
            	differences[key] = {fileName1 : object1[key], fileName2 : object2[key]}

    for key, value in object2.items():
        if key not in differences:
            if key not in object1:
                differences[key] = {fileName1 : "***NOT FOUND***", fileName2: value}


    return differences

def getListDifferences(list1, list2, fileName1, fileName2):
    differences = []

    if(len(list1) != len(list2)):
        return {fileName1 : list1, fileName2 : list2};
    list1.sort(key=keyFunction)
    list2.sort(key=keyFunction)

    for i in range(len(list1)):
        # Recursion if item is dict
        if isinstance(list1[i], dict) and isinstance(list2[i], dict):
            itemDiff = getObjectDifferences(list1[i], list2[i], fileName1, fileName2)

        # Recursion if item is list
        elif isinstance(list1[i], list) and isinstance(list2[i], list):
            itemDiff = getListDifferences(list1[i], list2[i], fileName1, fileName2)
        else:
            itemDiff = {fileName1: list1[i], fileName2: list2[i]}

        if itemDiff:
            differences.append(itemDiff)

    return differences;

def keyFunction(item):
    if isinstance(item, dict):
        if not item:
            return "{}"
        dict(sorted(item.items()))
        return list(item.keys())[0]
    elif isinstance(item, list):
        if not item:
            return "[]"
        sorted(item, key=keyFunction)
        return item[0]
    else:
        return str(item)

if __name__ == "__main__":

    fileName1 = sys.argv[1]
    fileName2 = sys.argv[2]

    with open(fileName1, "r") as f1:
        object1 = json.loads(f1.read())
    with open(fileName2, "r") as f2:
        object2 = json.loads(f2.read())

    result = getObjectDifferences(object1, object2, fileName1, fileName2)

    if not result:
        print(f"Contents of {fileName1} and {fileName2} are identical")
    else:
        print(json.dumps(result, indent=4))
