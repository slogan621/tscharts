#Open a file named Products.txt. Return a set containing all the unique drug names.
def drug_set(file):
    ret = set()
    file_opened = open(file,"r")
    for line in file_opened:
        drug = (line.strip().split('\t'))[5]
        ret.add(drug)
    file_opened.close()
    return ret
drug_set("Products.txt")
