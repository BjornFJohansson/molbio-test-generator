def parse_student_file(filename):
    __version__="2012-12-04"
    import re, codecs, string
    rows = codecs.open(filename,"r","utf-8").readlines()
    rows.sort()

    names, mecs = [],[]
    undefined_mec = 0

    for row in rows:
        if row.startswith("#"):
            continue
        if row.strip():
            row = "".join(x for x in row if x not in string.punctuation)
            mec=re.search("[\d|a|A|e|E]\d{4,5}",row)
            if mec:
                mec=mec.group(0)
            else:
                undefined_mec+=1
                mec="NA"+str(undefined_mec)
            name = re.sub("[\d|a|A|e|E]\d{4,5}","",row).strip()
            name = re.sub("ORD","",name).strip()
            name = re.sub("T-E","",name).strip()
            if mec in mecs:
                print mec,names[mecs.index(mec)]
                print mec,name
                raise ValueError("two entries with the same mec!")
            names.append(name)
            mecs.append(mec)
    assert len(mecs)==len(names)
    return mecs,names

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(description='Parse options')
    parser.add_argument("-f","--file", nargs = 1)

    args = parser.parse_args()

    mecs,names = parse_student_file(args.file[0])

    for mec,name in zip(mecs,names):
        print "mec#",mec,"name:", name
    print "totally", len(mecs), "students"


