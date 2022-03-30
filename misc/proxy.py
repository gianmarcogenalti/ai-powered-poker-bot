import argparse

def filter(file):
    newfile = file + 'p1.txt'
    file =  file +'.txt'
    newfile1 = open(newfile,'a')
    newfile1.truncate(0)
    with open(file, "r") as a_file:
        for line in a_file:
            if line[10]  == '?':
                newfile1.write(line)
    newfile1.close()

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--filename")
args = vars(ap.parse_args())
print(args)

pr.filter(args['filename'])
