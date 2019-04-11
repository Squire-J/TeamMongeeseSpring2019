import urllib.request
import json, re

catalog = "https://cbers-stac-0-6.s3.amazonaws.com/CBERS4/"

def getLinks(url):
        with urllib.request.urlopen(url) as response:
                html = response.read()

        parsed_json = json.loads(html)

        li = []

        for link in parsed_json['links']:
                if((not link['rel']=='self') and (not link['rel']=='root') and (not link['rel']=='parent')):
                        li.append(link['href'].split('/')[0])
        return li

def printList(li, numPerRow):
        i = 1
        for el in li:
                print(el, end=" ")
                if(i%numPerRow == 0):
                        print("")
                i+=1
        print("\n")

# def getListCameras():
        

def chooseCamera():
        listCameras = getLinks(catalog + 'catalog.json')

        print("* * * Choosing Camera * * *\n")
        print("Here is a list of available cameras:")
        printList(listCameras, 20)

        camera = input("Please enter a camera name from the list of available cameras: ")
        while(camera not in listCameras):
                camera = input("You entered " + camera + ", this is not on the list of available cameras, please enter an available camera: ")
        print("\n")
        return camera

def choosePath(camera):
        listPaths = getLinks(catalog + camera + '/catalog.json')

        print("* * * Choosing Path * * *\n")
        print("Here is a list of the available paths for the " + camera + " camera:")
        printList(listPaths, 20)

        path = input("Please enter a path number from the list of available paths for the " + camera + " camera: ")
        while(path not in listPaths):
                path = input("You entered " + path + ", this is not on the list of available paths for the " + camera + " camera, please enter an available path: ")
        print("\n")
        return path

def chooseRow(camera, path):
        listRows = getLinks(catalog + camera + '/' + path + '/catalog.json')

        print("* * * Choosing Row * * *\n")
        print("Here is a list of the available rows for the " + camera + " camera and path " + path +":")
        printList(listRows, 20)

        row = input("Please enter a row number from the list of available rows for the " + camera + " camera and path " + path + ": ")
        while(row not in listRows):
                row = input("You entered " + row + ", this is not on the list of available rows for the " + camera + " camera and path " + path + ", please enter an available row: ")
        print("\n")
        return row

def chooseItems(camera, path, row):
        listItems = getLinks(catalog + camera + '/' + path + '/' + row + '/catalog.json')

        print("* * * Choosing Item * * *\n")
        print("Here is a list of the available items for the " + camera + " camera and path " + path + "and row " + row + ":")
        printList(listItems, 3)

        item = input("Please enter an item from the list of available items for the " + camera + " camera and path " + path + " and row " + row + ": ")
        while(item not in listItems):
                item = input("You entered " + item + ", this is not on the list of available items for the " + camera + " camera and path " + path + " and row " + row + ", please enter an available item: ")
        print("\n")
        items = [camera + "/" + path + "/" + row + "/" + item]
        listItems.remove(item)
        if(len(listItems)==0):
                return items

        while(input("Would you like to select another item from the " + camera + " camera and path " + path + " and row " + row + "? (yes/no): ") == "yes"):
                print("Here is a list of the remaining available items for the " + camera + " camera and path " + path + " and row " + row + ":")
                printList(listItems, 3)
                item = input("Please enter an item from the list of available items for the " + camera + " camera and path " + path + " and row " + row + ": ")
                while(item not in listItems):
                        item = input("You entered " + item + ", this is not on the list of available items for the " + camera + " camera and path " + path + " and row " + row + ", please enter an available item: ")
                print("\n")
                items.append(camera + "/" + path + "/" + row + "/" + item)
                listItems.remove(item)
                if(len(listItems)==0):
                        return items

        return items

listItems = []


camera = chooseCamera()
path = choosePath(camera)
row = chooseRow(camera, path)
items = chooseItems(camera, path, row)

while(input("Would you like to select more items? (yes/no): ") == "yes"):
        print("\n")
        camera = chooseCamera()
        path = choosePath(camera)
        row = chooseRow(camera, path)
        items.extend(chooseItems(camera, path, row))

print("You have selected the items: ")
print(items)