en_layout = {
    "1": ["1", "Q", "2"],
    "2": ["2", "1", "3", "Q", "W"],
    "3": ["3", "2", "4", "W", "E"],
    "4": ["4", "3", "5", "E", "R"],
    "5": ["5", "4", "6", "R", "T"],
    "6": ["6", "5", "7", "T", "Y"],
    "7": ["7","6", "8", "Y", "U"],
    "8": ["8","7", "9", "U", "I"],
    "9": ["9","8", "0", "I", "O"],
    "0": ["0","9", "-", "O", "P"],

    "Q": ["Q", "1", "2", "A", "W"],
    "W": ["W", "2", "3", "Q", "E", "A", "S"],
    "E": ["E", "3", "4", "W", "R", "S", "D"],
    "R": ["R", "4", "5", "E", "T", "D", "F"],
    "T": ["T", "5", "6", "R", "Y", "F", "G"],
    "Y": ["Y", "6", "7", "T", "U", "G", "H"],
    "U": ["U", "7", "8", "Y", "I", "H", "J"],
    "I": ["I", "8", "9", "U", "O", "J", "K"],
    "O": ["O", "9", "0", "I", "P", "K", "L"],
    "P": ["P", "0", "-", "O", "L"],

    "A": ["A", "Q", "W", "S", "Z"],
    "S": ["S", "W", "E", "A", "D", "Z", "X"],
    "D": ["D", "E", "R", "S", "F", "X", "C"],
    "F": ["F", "R", "T", "D", "G", "C", "V"],
    "G": ["G", "T", "Y", "F", "H", "V", "B"],
    "H": ["H", "Y", "U", "G", "J", "B", "N"],
    "J": ["J", "U", "I", "H", "K", "N", "M"],
    "K": ["K", "I", "O", "J", "L", "M"],
    "L": ["L", "O", "P", "K", "."],

    "Z": ["Z", "A", "S", "X"],
    "X": ["X", "Z", "S", "D", "C"],
    "C": ["C", "X", "D", "F", "V"],
    "V": ["V", "C", "F", "G", "B"],
    "B": ["B", "V", "G", "H", "N"],
    "N": ["N", "B", "H", "J", "M"],
    "M": ["M", "N", "J", "K"],
    "-": ["0", "P", "_"],
    "_": ["-"],
    ".": ["L"],
    "@": [],
    "/": [],
    "!": [],
    "(": [],
    ")": [],
    "~": [],
    "'": [],
    "*": []
}

def extended_damerau_levenshtein(s1, s2, key_map):
    replace_cost = 0
    length_penalty = 0

    # Remove special characters from s1 and s2, and apply a replacement cost if equal afterward
    for char in [".", "-", "_", ".js"]:
        if (char in s1 or char in s2) and (s1 != s2):
            s1 = s1.replace(char, "")
            s2 = s2.replace(char, "")
            if s1 == s2:
                replace_cost = 0.5

    rows = len(s1) + 1
    cols = len(s2) + 1
    dist = [[0 for x in range(cols)] for y in range(rows)]

    # Initialize distance matrix
    for i in range(1, rows):
        dist[i][0] = i
    for i in range(1, cols):
        dist[0][i] = i

    
    for col in range(1, cols):
        for row in range(1, rows):
            if s1[row - 1] == s2[col - 1]:
                cost = 0  # No cost if characters match
            else:
                
                cost = 0.5 if s1[row - 1].upper() in key_map.get(s2[col - 1].upper(), []) else 2

            dist[row][col] = min(dist[row - 1][col] + 0.5,       
                                 dist[row][col - 1] + 0.5,      
                                 dist[row - 1][col - 1] + cost)   

            if row > 1 and col > 1 and s1[row - 1] == s2[col - 2] and s1[row - 2] == s2[col - 1]:
                dist[row][col] = min(dist[row][col], dist[row - 2][col - 2] + 0.5)

    length_penalty = (abs(len(s1) - len(s2))) * 0.5 if abs(len(s1) - len(s2)) > 1 else 0
    
    distance = dist[rows - 1][cols - 1] + replace_cost

    return distance + length_penalty