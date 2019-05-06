import numpy as np

class StringHelper:
    #Longest common substring of two strings
    @staticmethod
    def LCS(s1, s2):
        
        l1 = len(s1)
        l2 = len(s2)
        f = np.zeros((l1 + 1, l2 + 1), np.int32)
        for i in range(l1):
            for j in range(l2):
                if s1[i] == s2[j]:
                    f[i+1][j+1] = f[i][j] + 1
                else:
                    f[i+1][j+1] = np.max([f[i][j+1], f[i+1][j]])
        return f[l1][l2]

    @staticmethod
    def is_contain(data, pat, eps = 0.7):
        if data == "" or pat == "":
            return -1
        str_len = len(data)
        pat_len = len(pat)
        best_score = 0
        id = 0
        if pat_len > str_len:
            if StringHelper.LCS(data, pat) / pat_len >= eps:
                return 0
        for i in range(str_len - pat_len + 1):
            score = float(StringHelper.LCS(data[i:i+pat_len], pat)) / pat_len
            if score > best_score:
                best_score = score
                id = i
        if best_score >= eps:
            return id
        return -1

    @staticmethod
    def normalize_str(data):
        data = data.strip()
        table = [["!", "1"], ["%", "3"], ["$", "8"], ["§", "8"], ["ö", "ô"], ["Ñ", "N"],
                 ["Š", "S"], ["ø", "ô"], ["@", "ô"], ["ð", "ô"], ["†", "T"], ["!", "l"], ["Ÿ", "Y"],
                 ["ƒ", "f"], ["€", "e"], ["#", "H"], ["ä", "a"], ["Ä", "A"], ["ÿ", "y"], ["⁄", "/"]]
        #noises = "ˆ“‹„”`*¿Ï‡'"
        #°
        f = open("src/replace_table.txt")
        for line in f:
            size = len(line)
            data = data.replace(line[0], line[1])
        noises = open("src/noisy_chars.txt") 
        for noise in noises:
            for c in noise:
                data = data.replace(c, "")
        return data

    @staticmethod
    def normalize_result(result):
        result = result.strip()
        r = len(result) - 1
        noises = ".|{}()_+-<>: ˆ“[]?,=*#^'~Ä;/"
        while r >= 0 and result[r] in noises:
            r -= 1
        l = 0
        while l < len(result) and result[l] in noises:
            l += 1

        result = result[l:r + 1]
        return result
    @staticmethod
    def normalize_blocks(blocks):
        size = len(blocks)
        for i in range(size):
            blocks[i] = StringHelper.normalize_str(blocks[i])
        return blocks
