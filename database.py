import openpyxl
import time
from openpyxl_image_loader import SheetImageLoader
import os
import pathlib

import mlFunctions

class DatabaseEntry:
    def __init__(self, inputString):
        
        inputlist = inputString.split('~')
        
        self.number = inputlist[0]
        self.irNumber = inputlist[1]
        self.imagePath = inputlist[2]
        self.words = inputlist[3]
        self.status = inputlist[4].replace('\n', "")
        self.classes = inputlist[5]
        self.colourData = inputlist[6]
    
    def __str__(self) -> str:
        output = f"{self.number}~{self.irNumber}~{self.imagePath}~{self.words}~{self.status}~{self.classes}~{self.colourData}"

        return output

def preprocess_database(databasePath, currentPath):
    
    databaseFile = openpyxl.load_workbook(databasePath)

    database = databaseFile['Test']
    image_loader = SheetImageLoader(database)



    entries = []

    for index in range(5, database.max_row+1):
        print(f'Indexing Entry {index+1} out of {database.max_row+1}')
        number = database[f'A{index}'].value
        irNumber = database[f'B{index}'].value
        
        try:
            image = image_loader.get(f'C{index}')

            dir = str(currentPath) + r'\imageDatabase'
            saveLocation = str(currentPath) + r'\imageDatabase\entry_' + str(number) + r'.jpg'
            if not os.path.exists(dir):
                os.mkdir(dir)
            
            image.save(saveLocation)

            colourData = mlFunctions.preproccess_image_colours(saveLocation, 5)

        except ValueError:
            saveLocation = "None"
            colourData = "None"
            pass

        words = database[f'D{index}'].value
        status = database[f'E{index}'].value
        classes = database[f'F{index}'].value

        dataEntryString = "~".join([number, irNumber, words, saveLocation, status, classes, str(colourData)])

        entries.append(DatabaseEntry(dataEntryString))

    outputString = ""

    for entry in entries:
        outputString += str(entry)+'\n'

    return outputString

def save_database(fileSaveLocation, dataToSave):
    with open(fileSaveLocation, 'w') as file:
        file.write(dataToSave)

def read_database(fileSaveLocation):
    with open(fileSaveLocation, 'r') as file:
        data =  file.readlines()

        return [DatabaseEntry(entry) for entry in data]

def checkDatabaseIndexing():
    try:
        with open(databaseToSaveLocation, 'r') as file:
            return True
    except FileNotFoundError:
        return False

def indexDatabase():
    preprocessedData = preprocess_database(databasePath, currentPath)
    save_database(databaseToSaveLocation, preprocessedData)

currentPath = str(pathlib.Path().resolve())
databasePath = r'C:\Users\sammy.LAPTOP-RUR693FV\Desktop\Code\Database.xlsx'
databaseToSaveLocation = currentPath + r'\database.txt'


