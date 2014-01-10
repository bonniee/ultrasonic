import argparse

def levenshteinDistance(s1,s2):
    if len(s1) > len(s2):
        s1,s2 = s2,s1
    distances = range(len(s1) + 1)
    for index2,char2 in enumerate(s2):
        newDistances = [index2+1]
        for index1,char1 in enumerate(s1):
            if char1 == char2:
                newDistances.append(distances[index1])
            else:
                newDistances.append(1 + min((distances[index1],
                                             distances[index1+1],
                                             newDistances[-1])))
        distances = newDistances
    return distances[-1]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="evaluater")
    parser.add_argument('sent', help="Original")
    parser.add_argument('received', help="Received text")
    args = parser.parse_args()

    print levenshteinDistance(args.sent, args.received)