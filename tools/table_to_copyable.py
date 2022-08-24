def translate(string):
    return "["+ "".join("["+i.replace("%", '') + "],\n" for i in string.replace(' + ', ',').replace(' / ', ',').split())[:-2] + "]"


def transpose(*strings):
    ls = []
    for s in strings:
        ls.append(eval(translate(s)))

    m = len(ls)
    n = len(ls[0])
    out = "["
    for i in range(n):
        new = "["
        for j in range(m):
            new += repr(ls[j][i]) + ','
        new = new[:-1]
        new += "],\n"
        out += new
    out = out[:-2]
    out += ']'
    return out
