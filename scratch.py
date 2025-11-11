import csv

def printTable(fileName):
    with open(fileName) as f:
        readingList=csv.reader(f)
        readingList=list(readingList)
   
    NoOfColumns=len(readingList[0])
    WidthOfColumns=[0]*NoOfColumns

    for row in readingList:
        for i, cell in enumerate(row):
                  WidthOfColumns[i] = max(WidthOfColumns[i], len(cell))


    def horizontal():
        return '+'  + '+'.join('-') + '+'
   
    def vertical():
        return '|' + '|'.join(f'{cell}')

       
       
    print(horizontal())
    print(vertical(readingList[0]))

    print(horizontal())
    for row in readingList[:1]:
        print(vertical(row))
    print(horizontal())

printTable('games.txt')