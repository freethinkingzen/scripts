import sys
import json

def getObjectDifferences(object1, object2, fileName1, fileName2):

    differences = {}

    for key, value in object1.items():
        # Check if object2 contains same key as object1
        if key not in object2:
            differences[key] = f"Missing in {fileName2}"

        # Check if both values are equal
        elif object1[key] != object2[key]:

            # Recursion if item is a dictionary
            if isinstance(object1[key], dict) and isinstance(object2[key], dict):
                differences[key] = getObjectDifferences(object1[key], object2[key], fileName1, fileName2)

            elif isinstance(object1[key], list) and isinstance(object2[key], list):
               differences[key] = getListDifferences(object1[key], object2[key], fileName1, fileName2);

            else:
            	differences[key] = {fileName1 : object1[key], fileName2 : object2[key]}

    for key, value in object2.items():
        if key not in differences:
            if key not in object1:
                differences[key] = f"Missing in {fileName1}"


    return differences

def getListDifferences(list1, list2, fileName1, fileName2):
    differences = []

    if(len(list1) != len(list2)):
        return {fileName1 : list1, fileName2 : list2};

    list1.sort();
    list2.sort();

    for i in range(len(list1)):
        if isinstance(list1[i], dict) and isinstance(list2[i], dict):
            differences.append(getObjectDifferences(list1[i], list2[i], fileName1, fileName2))
        else:
            differences.append({fileName1: list1[i], fileName2: list2[i]});

    return differences;

if __name__ == "__main__":

    fileName1 = sys.argv[1]
    fileName2 = sys.argv[2]

    with open(fileName1, "r") as f1:
        object1 = json.loads(f1.read())
    with open(fileName2, "r") as f2:
        object2 = json.loads(f2.read())

    result = getObjectDifferences(object1, object2, fileName1, fileName2)
    print(json.dumps(result, indent=4))
