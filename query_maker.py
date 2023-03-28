# quotation marks to search for multiple words “climate change” ->“climate+change”
# OR “heart|myocardial infarction|attack” -> %7C
# exclude -> mercury+–ford
# allintitle:”agaricus bisporus”

# Given two lists, returns the string with the permutation of all the elements separated by OR
def all_permutations(l1,l2):
    out = ""

    for e1 in l1:
        for e2 in l2:
            if e1 != e2:
                out += r'"' + e1.replace(" ", "+") + "+" + e2.replace(" ", "+") + r'"' + r"%7C"
    return out[:-3]