import argparse
import urllib.request
import logging
import datetime
import csv
from io import StringIO

def downloadData(url):
    csvData=urllib.request.urlopen(url).read().decode("ascii","ignore") 
    return csvData

dataDict={}

def processData(file):

    data=StringIO(file)
    csv_reader = csv.reader(data, delimiter=',')
    next(csv_reader)
    
    index=2 
    for lines in csv_reader:
        try:
            birthday= datetime.datetime.strptime(lines[2], '%d/%m/%Y').date()
            dataDict[lines[0]] = (lines[1],birthday) 
        except:
            logger.error("Error processing line {} for ID {}".format(index,lines[0]))  
        finally:
            index +=1

def displayPerson(id, personData=dataDict):

    if id in personData.keys():
        print (" Person {} is {} with a birthday of {}". format(id, personData[id][0] , personData[id][1]))

    else:
        print( " No user found with that id")

def main(url):
    print(f"Running main with URL = {url}...")

    try:
        csvData=downloadData(args.url)
    except:

        print("An error has occured. Please try again")
        exit()

    personData=processData(csvData)

    isTrue=True
    while isTrue:
        n=input("Enter ID for lookup: ")
        if int(n)>0:
            displayPerson(n)
        else:
            isTrue=False

if __name__ == "__main__":

    logger=logging.getLogger("Assignment2")
    fh = logging.FileHandler('error.log')
    fh.setLevel(logging.ERROR)
    logger.addHandler(fh)

    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()

    main(args.url)