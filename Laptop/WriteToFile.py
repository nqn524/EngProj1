from datetime import datetime
import csv
import atexit

_date = str(datetime.now())
date = _date.replace(':', '-') #basic search replace on the string since windows can't store files with : in the file name

csvfile = open(f"{date}.csv", "w", newline='')
thewrite = csv.writer(csvfile, delimiter=',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)

thewrite.writerow(["x","y","z","t"])

def WriteToFile(x, y, z , t):
    thewrite.writerow([x,y,z,t])

@atexit.register
def CloseFile():
    csvfile.close()
    print("closed")
