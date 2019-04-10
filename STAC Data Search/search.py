import urllib.request
import json, re


def getLinks(url):
        with urllib.request.urlopen(url) as response:
                html = response.read()

        parsed_json = json.loads(html)

        li = []

        for link in parsed_json['links']:
                if((not link['rel']=='self') and (not link['rel']=='root') and (not link['rel']=='parent')):
                        li.append(link['href'].split('/')[0])
        return li

def printList(li):
        i = 1
        for el in li:
                print(el, end=" ")
                if(i%20 == 0):
                        print("")
                i+=1
        print("\n")

# def getListCameras():
        

def chooseCamera():
        listCameras = getLinks('https://cbers-stac-0-6.s3.amazonaws.com/CBERS4/catalog.json')

        print("* * * Choosing Camera * * *\n")
        print("Here is a list of available cameras:")
        printList(listCameras)

        camera = input("Please enter a camera name from the list of available cameras: ")
        while(camera not in listCameras):
                camera = input("You entered " + camera + ", this is not on the list of available cameras, please enter an available camera: ")
        print("\n")
        return camera

def choosePath(camera):
        listPaths = getLinks('https://cbers-stac-0-6.s3.amazonaws.com/CBERS4/' + camera + '/catalog.json')

        print("* * * Choosing Path * * *\n")
        print("Here is a list of the available paths for the " + camera + " camera:")
        printList(listPaths)

        path = input("Please enter a path number from the list of available paths for the " + camera + " camera: ")
        while(path not in listPaths):
                path = input("You entered " + path + ", this is not on the list of available paths for the " + camera + " camera, please enter an available path: ")
        print("\n")
        return path

def chooseRow(camera, path):
        listRows = getLinks('https://cbers-stac-0-6.s3.amazonaws.com/CBERS4/' + camera + '/' + path + '/catalog.json')

        print("* * * Choosing Row * * *\n")
        print("Here is a list of the available rows for the " + camera + " camera and path " + path +":")
        printList(listRows)

        row = input("Please enter a row number from the list of available rows for the " + camera + " camera and path " + path + ": ")
        while(row not in listRows):
                row = input("You entered " + row + ", this is not on the list of available rows for the " + camera + " camera and path " + path + ", please enter an available row: ")
        print("\n")
        return row

def chooseItem(camera, path, row):
        listItems = getLinks('https://cbers-stac-0-6.s3.amazonaws.com/CBERS4/' + camera + '/' + path + '/' + row + '/catalog.json')

        print("* * * Choosing Item * * *\n")
        print("Here is a list of the available items for the " + camera + " camera and path " + path + "and row " + row + ":")
        printList(listItems)

        item = input("Please enter an item from the list of available items for the " + camera + " camera and path " + path + " and row " + row + ": ")
        while(item not in listItems):
                item = input("You entered " + item + ", this is not on the list of available items for the " + camera + " camera and path " + path + " and row " + row + ", please enter an available item: ")
        print("\n")
        return item

listItems = []
camera = chooseCamera()
path = choosePath(camera)
row = chooseRow(camera, path)
item = chooseItem(camera, path, row)
if(item not in listItems):
        listItems.append(item)

while(input("Would you like to select another item from the " + camera + " camera and path " + path + " and row " + row + "? (yes/no): ") == "yes"):
        item = chooseItem(camera, path, row)
        if(item not in listItems):
                listItems.append(item)


print("You have selected the items: ")
print(listItems)