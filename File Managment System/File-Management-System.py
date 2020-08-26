import os
import time
from datetime import date
from tkinter import *
from tkinter import messagebox
import subprocess
import sqlite3

# Global Vars
today = date.today()  # Non-formatted date and time
saveLoc = "None"  # Location where files are retrieved
wrkDir = "None"  # User chosen directory to save sorted files
year = ""  # Holds current year program is working in
todaystr = today.strftime("%c")  # Holds today's date and time as a string formated
clicked = 0  # Controls directory change frames
clicked2 = 0  # Controls rename dropdown type
dataList = [None] * 2  # Holds Save and Store locations
noData = True  # T/F if there is data in database
# Make sure to add a space after the abbreviation for the user whe saving to database
abrvs = [("P ", "Sermon"), ("S ", "Song"), ("V ", "Verse"), ("T ", "Testimony"), ("PR ", "Prophesy")]
abrvs2 = ["Sermon", "Song", "Verse", "Testimony", "Prophesy", "Misc", "None"]


# Create GUI window
root = Tk()
# Add title to window
root.title("File Management System")
# Making window non-resizable (x,y)
root.resizable(False, False)
# Setting window size
root.geometry("500x250")
# Center window on screen
window_height = 250
window_width = 500
# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
# Do math to get center of screen and window
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2) - 200)
# Place at center, -200 pixels on y axis
root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

# Accessing necessary photos for GUI graphics
photoOut = PhotoImage(file=os.getcwd() + "\\Src\\Folder-Out.png")
photoIn = PhotoImage(file=os.getcwd() + "\\Src\\Folder-In.png")

# Creating instance of the root frame for each GUI frame
mainFrame = Frame(root, width=500, height=250)
settingsFrame = Frame(root, width=500, height=250)
sortingFrame = Frame(root, width=500, height=250)
storageFrame = Frame(root, width=500, height=250)
storageFrame2 = Frame(root, width=500, height=250)
abrvFrame = Frame(root, width=500, height=250)
infoFrame = Frame(root, width=500, height=250)
renameFrame = Frame(root, width=500, height=250)
renameFrame2 = Frame(renameFrame, width=500, height=250)
renameFrame3 = Frame(renameFrame, width=500, height=250)

# Keeping track of last frame, last frame left. For use of back button
lastFrame = mainFrame

# Create global canvas to use for images used in 'change directory' frames
canvas = Canvas(storageFrame, width=77, height=54)

# Creating databases to store info
connSaveLoc = sqlite3.connect(os.getcwd() + '\\Src\\save_location')
connAbbreviations = sqlite3.connect(os.getcwd() + '\\Src\\abrv')

# Create cursors for databases to navigate database
cS = connSaveLoc.cursor()  # for file save locations
cA = connAbbreviations.cursor()  # for file name abbreviations


def setupNewYear(syear):  # New Year Folder Setup

    # creating array of months
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]

    # How many weeks per month
    weeks = [6, 5, 5, 6, 5, 5, 5, 5, 5, 6, 5, 5]
    # days
    days = ["Tuesday", "Thursday", "Sunday"]
    # creating new paths
    ypath = "\\" + syear
    path = wrkDir + ypath
    os.system('cls')  # clears screen
    print("Path: " + path)
    if not os.path.exists(path):
        print("\nSetting up new year...")
        os.mkdir(path)
        time.sleep(1)
        # Un-comment if you want all months and all weeks created for the year. Harder to find recording this way
        """
        print("\n\nSetting up new months...")
        cnt = 1
        cntw = 0
        # Month setup
        for x in months:
            month = "\\{" + str(cnt) + "} " + x
            cnt2 = weeks[cntw]
            cntw += 1
            cnt += 1
            mpath = path + month
            os.mkdir(mpath)
            # Week setup
            while cnt2 >= 1:
                week = "\\week {" + str(cnt2) + "}"
                cnt2 -= 1
                wpath = mpath + week
                os.mkdir(wpath)
                cnt3 = 3
                # day setup 3 days per week
                for x in days:
                    day = "\\" + x
                    dpath = wpath + day
                    os.mkdir(dpath)
                    # adding morning and evening folders to sunday folder
                    if x == "Sunday":
                        evening = "\\Evening"
                        morning = "\\Morning"
                        epath = dpath + evening
                        mornpath = dpath + morning
                        os.mkdir(epath)
                        os.mkdir(mornpath)
        time.sleep(1)
        print("\n\nSetting up weeks...")
        time.sleep(1)
        print("\n\nSetting up days...")
        time.sleep(1)
        """
        print("\n\nSetup Completed")
        time.sleep(2)


def continueYear():  # Sort method of recordings
    os.system('cls')  # clears screen
    global saveLoc
    global wrkDir

    # Get storage data
    queryDataLoc()

    # New Window
    top = Toplevel()
    top.title("File Management System/Sorting Files")
    top.resizable(False, False)
    top.geometry("500x300")

    # Creating slider for window
    scroll = Scrollbar(top, orient=VERTICAL)

    print("Sorting recordings...\n")

    # some var info about file
    fileCreated = ""
    # List of month abbreviations
    monthAbrv = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10,
                 "Nov": 11, "Dec": 12}
    months = {1: "January",2: "February",3: "March",4: "April",5: "May",6: "June",7: "July",8: "August",9: "September",
              10: "October",11: "November",12: "December"}
    # How many days in each month
    monthdays = {"Jan": 31, "Feb": 28, "Mar": 31, "Apr": 30, "May": 31, "Jun": 30, "Jul": 31, "Aug": 31, "Sep": 30,
                 "Oct": 31,"Nov": 30, "Dec": 31}
    # List of day abbreviations
    dayAbrv = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}
    days = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}

    # *******************************************Sorting algorithm ***********************************************
    moveFilesList = []
    filenameList = []

    # Listbox for all file output
    listbox = Listbox(top, width=480, height=18, yscrollcommand=scroll)

    scroll.config(command=listbox.yview)
    scroll.pack(side=RIGHT, fill=Y)

    for filename in os.listdir(saveLoc):

        # Grab when file was created
        fileCreated = time.ctime(os.path.getmtime(saveLoc + "\\" + str(filename)))

        # *************************************************************************************************************
        # *********************CALCULATING DAYS PER MONTH AND WEEKS IN MONTH AND WEEK OF FILE**************************
        # *************************************************************************************************************

        # Fixing leap years
        if int(fileCreated[20:fileCreated.__len__()]) % 4 == 0:
            monthdays["Feb"] = 29
        else:
            monthdays["Feb"] = 28

        # Checking month week setup
        daysfromstartweek = 0
        for k in dayAbrv:
            if k == fileCreated[0:3]:
                daysfromstartweek = dayAbrv.get(k)
        day = int(fileCreated[8:10])
        week = day - daysfromstartweek
        weekCnt = 0
        # Check how much weeks there are
        while week > 0:
            week -= 7
            weekCnt += 1
        # Get the correct day the month starts on
        week = day - daysfromstartweek
        # Subtract number of days not counting the start of weeks days
        week += (-6*weekCnt)
        weekCnt += 1
        week -= weekCnt
        #print("weeks count:", weekCnt)

        # DEBUG
        #monthstart = ""
        #for k in dayAbrv:
        #    daystart = dayAbrv.get(k)
        #    if daystart == abs(week):
        #        monthstart = k

        # *************************************************************************************************************
        # *************************************************************************************************************
        # *************************************************************************************************************

        # Go through the string of fileCreated and grab relevant info
        fday = fileCreated[0:3]
        fmonth = fileCreated[4:7]
        fweek = fileCreated[8:10]
        ftime = fileCreated[11:18]
        fyear = fileCreated[20:fileCreated.__len__()]

        # Printing separator/adding sep to list of output
        listbox.insert(END, "*************************************************")
        print("*************************************************")

        """
        if (fyear != year and not os.path.isdir(wrkDir + "\\" + fyear)) or not(os.path.isdir(wrkDir + "\\" + fyear)):
            print("Year of file does not match current directory... Creating new directory for file")
            time.sleep(3)
            # Un-comment if you would like it to print message that its setting up new year. (Includes a wait of 2 sec)
            # setupNewYear(fyear)
            print("\nDirectory created: " + wrkDir + "\\" + fyear)
        """

        # Showing file that is being worked on
        print("\n'" + filename, end="'")
        listbox.insert(END, filename)

        # Debugging
        #print("Day:", fday)
        #print("Month:", fmonth)
        #print("Week:", fweek)
        #print("Time:", ftime)
        #print("Year:", fyear)

        # Creating paths
        dayPath = ""
        monthPath = ""
        addPath = ""
        addP = False

        # Creating new filename and assigning folders with file markers 'P, V, T, S, PR' and also Misc for no marker
        if filename.find("PR") == 0 and filename[2:3] == " ":
            addP = True
            addPath = "\\Prophecy's"
            print("             Moved to Prophecy's")
            listbox.insert(END, "             Moved to Prophecy's")
        elif filename.find("P") == 0 and filename[1:2] == " ":
            addP = True
            addPath = "\\Sermons"
            print("             Moved to Sermons")
            listbox.insert(END, "             Moved to Sermons")
        elif filename.find("S") == 0 and filename[1:2] == " ":
            addP = True
            addPath = "\\Songs"
            print("             Moved to Songs")
            listbox.insert(END, "             Moved to Songs")
        elif filename.find("T") == 0 and filename[1:2] == " ":
            addP = True
            addPath = "\\Testimony's"
            print("             Moved to Testimony's")
            listbox.insert(END, "             Moved to Testimony's")
        elif filename.find("V") == 0 and filename[1:2] == " ":
            addP = True
            addPath = "\\Verses"
            print("             Moved to Verses")
            listbox.insert(END, "             Moved to Verses")
        else:
            addP = True
            addPath = "\\Misc"
            print("             Moved to Misc")
            listbox.insert(END, "")

    # Creating day path
        for k in dayAbrv:
            if fday == k:
                dayPath = "\\" + days[dayAbrv.get(k)]
        # print(dayPath)

        # Creating week path
        weekPath = "\\week {" + str(weekCnt) + "}"
        # print(weekPath)

        # Creating month path
        for k in monthAbrv:
            if fmonth == k:
                monthPath = "\\{" + str(monthAbrv.get(k)) + "} " + months[monthAbrv.get(k)]
        # print(monthPath)
        # print(today.strftime("%c"))

        # Creating year path
        yearPath = "\\" + fyear

        # Combine path names into 1 string and add to list
        if addP:
            # If its sunday we sort into evening or morning
            if fday == "Sun":
                if int(ftime[0: 2]) < 16:
                    moveFilesList.append(wrkDir + yearPath + monthPath + weekPath + dayPath + "\\Morning" + addPath)
                else:
                    moveFilesList.append(wrkDir + yearPath + monthPath + weekPath + dayPath + "\\Evening" + addPath)
            else:
                moveFilesList.append(wrkDir + yearPath + monthPath + weekPath + dayPath + addPath)
            filenameList.append(filename)
            addP = False
        else:
                print("Error when moving")
        # prints when file was created/ where it was moved to info
        print("         ", fday, fmonth, fweek + " Week{" + str(weekCnt) + "}", fyear)
        listbox.insert(END, "         " + fday + " " + fmonth + " " + fweek + " Week{" +
                            str(weekCnt) + "} " + fyear)

        # Moving files
    #print(moveFilesList)
    moveFiles(moveFilesList, saveLoc, filenameList)
    print("\n\nFiles Successfully moved!")
    listbox.insert(END, "\n\nFiles Successfully moved!")

    # Packing listbox to screen
    listbox.pack(side=LEFT, padx=5, pady=5)


def moveFiles(pathList, source, filenameList):
    # Moves files to new location
    # Counter keeps track of file name position in list
    cnter = 0

    # Printing separator
    print("*************************************************")
    for x in pathList:
        filename = filenameList[cnter]
        #print(x + "\\" + filename)

        # New filename
        if filename.find("PR") == 0:
            newfilename = filename[3:filename.__len__()]
        elif x[len(x) - 4: len(x)] == "Misc":
            newfilename = filename
        else:
            newfilename = filename[2:filename.__len__()]
        # Make first file have a 0 at the end
        try:
            test = int(newfilename[len(newfilename) - 6: len(newfilename) - 4])

        except:
            newfilename = newfilename[0: int(newfilename.__len__() - 4)] + " 0.m4a"

        # Checking if file exists and adding numbers to the end if it does
        renamingprinted = False
        while os.path.isfile(x + "\\" + newfilename):
            # Telling the user that the file has been renamed
            if not renamingprinted:
                print("\nFile '" + newfilename + "' exists renamed too: ", end="")
                renamingprinted = True
            num = newfilename.__len__() - 6
            num2 = newfilename.__len__() - 4
            num3 = int(newfilename[num: num2])
            num = newfilename.__len__() - 5
            newfilename = newfilename[0: num] + str(num3 + 1) + ".m4a"

        # Telling the user what the file has been renamed to
        if renamingprinted:
            print("'" + newfilename + "'")

        # Moving file and deleting prefix
        if not os.path.isdir(x):
            os.makedirs(x)

        os.rename(source + "\\" + filename, x + "\\" + newfilename)
        cnter += 1


def GUISettings():
    global lastFrame
    # Hiding main menu screen widgets
    mainFrame.pack_forget()
    storageFrame.pack_forget()
    storageFrame.place_forget()
    storageFrame2.pack_forget()
    storageFrame2.place_forget()
    abrvFrame.pack_forget()
    infoFrame.pack_forget()
    renameFrame.pack_forget()
    renameFrame2.pack_forget()
    renameFrame3.pack_forget()

    # Set last frame
    lastFrame = settingsFrame

    # Buttons
    mainMenuButton = Button(settingsFrame, text="Main Menu", padx=5, pady=5, command=mainGUI)
    renameFilesButton = Button(settingsFrame, text="Rename Files", padx=5, pady=5, command=renameFilesGUI)
    editSaveLocButton = Button(settingsFrame, text="Edit Directories", padx=5, pady=5, command=editSaveLocGUI)
    editAbrvButton = Button(settingsFrame, text="Edit Abbreviations", padx=5, pady=5, command=editAbvGUI)
    infoButton = Button(settingsFrame, text="How to use", padx=5, pady=5, command=infoScreen)

    # Labels
    mainLabel = Label(settingsFrame, text="SETTINGS", bd=2, relief="solid", padx=5, pady=5)

    # Placing Labels on screen
    mainLabel.place(relx=.5, rely=0, anchor=N)

    # Placing Buttons on screen
    mainMenuButton.place(x=498, y=248, anchor=SE)
    renameFilesButton.place(x=250, y=80, anchor='center')
    editSaveLocButton.place(x=250, y=120, anchor='center')
    editAbrvButton.place(x=250, y=160, anchor='center')
    infoButton.place(x=2, y=248, anchor=SW)

    # Packing all widgets to screen
    settingsFrame.pack()


def popUpConfirmSave(entry):
    global clicked
    global wrkDir
    global saveLoc
    # Create message box
    response = 1
    if clicked == 0:
        response = messagebox.askyesno("Confirm Overwrite", "Are you sure you want to overwrite?")

    if response == 1:
        # Call delete function
        deleteRecord()
        # Call to save new data
        if entry == "" and clicked == 0:
            entry = saveLoc
        elif entry == "" and clicked == 1:
            entry = wrkDir
        saveDataLoc(entry)
        # Set new screen
        clicked = 1
        editSaveLocGUI()


def deleteRecord():
    # Deleting last save location, and store locations.

    # Connect to database
    connSaveLoc = sqlite3.connect(os.getcwd() + '\\Src\\save_location')
    # Create cursor
    cS = connSaveLoc.cursor()

    try:
        # Delete record with oid #1
        cS.execute("DELETE from saveLoc WHERE oid = 1")
        connSaveLoc.commit()
    except Exception:
        print("Error deleting record")


def editSaveLocGUI():  # Method changes between two entry's for directories
    global clicked
    global canvas
    global wrkDir
    global saveLoc
    # Frames
    global storageFrame
    global storageFrame2
    global settingsFrame

    # Remove settings frame
    settingsFrame.pack_forget()

    # Check if clicks =0 then set screen to be first input (rec move from location)
    if clicked == 1:
        # Forget last screen
        storageFrame.pack_forget()
        storageFrame.place_forget()

        # Buttons
        saveButton = Button(storageFrame2, text="Save", padx=5, pady=5,
                            command=lambda: [saveDataLoc(desiredStorageLocationEntry.get()), GUISettings()])

        # Labels
        mainLabel = Label(storageFrame2, text="SETTINGS/DIRECTORIES", bd=2, relief="solid", padx=5, pady=5)
        desiredStorageLocationLable = Label(storageFrame2, text="Enter desired storage location of sorted files"
                                                                "(or click save):")
        currentdesiredStorageLocationLable = Label(storageFrame2, text=("Current: " + wrkDir))

        # Text entry
        desiredStorageLocationEntry = Entry(storageFrame2, width=75, borderwidth=3)

        # Placing Labels on screen
        mainLabel.place(relx=.5, rely=0, anchor=N)
        desiredStorageLocationLable.place(x=250, y=105, anchor=N)
        currentdesiredStorageLocationLable.place(x=250, y=85, anchor=N)

        # Create canvas for image
        canvas = Canvas(storageFrame2, width=78, height=60)
        canvas.place(x=450, y=75, anchor='center')

        # Placing Image Labels on screen
        canvas.create_image(39, 60, anchor=S, image=photoIn)

        # Placing text entry on screen
        desiredStorageLocationEntry.place(relx=.5, rely=.5, anchor=N)

        # Placing Buttons on screen
        saveButton.place(x=250, y=248, anchor=S)

        # Packing items to screen
        storageFrame2.pack()

    if clicked == 0:
        # Get storage info
        queryDataLoc()

        # Buttons
        backButton = Button(storageFrame, text="Back", padx=5, pady=5, command=GUISettings)
        saveButton = Button(storageFrame, text="Save", padx=5, pady=5,
                            command=lambda: [popUpConfirmSave(currentStorageLocationEntry.get()), editSaveLocGUI()])

        # Labels
        mainLabel = Label(storageFrame, text="SETTINGS/DIRECTORIES", bd=2, relief="solid", padx=5, pady=5)
        currentStorageLocationLable = Label(storageFrame, text="  Enter storage location of non-sorted files:  ")
        savedCurrentStorageLocationLable = Label(storageFrame, text=("Current: " + str(saveLoc)))

        # Text entry
        currentStorageLocationEntry = Entry(storageFrame, width=75, borderwidth=3)

        # Placing Labels on screen
        mainLabel.place(relx=.5, rely=0, anchor=N)
        currentStorageLocationLable.place(x=250, y=105, anchor=N)
        savedCurrentStorageLocationLable.place(x=250, y=85, anchor=N)

        # Create canvas for image
        canvas.destroy()
        canvas = Canvas(storageFrame, width=78, height=60)
        canvas.place(x=50, y=75, anchor='center')

        # Placing Image Labels on screen
        canvas.create_image(39, 60, anchor=S, image=photoOut)

        # Placing text entry on screen
        currentStorageLocationEntry.place(relx=.5, rely=.5, anchor=N)

        # Placing Buttons on screen
        backButton.place(x=498, y=248, anchor=SE)
        saveButton.place(x=250, y=248, anchor=S)

        # Packing items to screen
        storageFrame.pack()


def editAbvGUI():
    global abrvs
    # Hiding main menu screen widgets
    settingsFrame.pack_forget()

    # Create scroll frame
    scrollFrame = Frame(abrvFrame)

    # Creating slider for window
    scroll = Scrollbar(scrollFrame, orient=VERTICAL)

    # Listbox for all file output
    listbox = Listbox(scrollFrame, width=25, height=10, yscrollcommand=scroll.set)

    for x in range(0,20):
        listbox.insert(END, x)

    scroll.config(command=listbox.yview)
    scroll.pack(side=RIGHT, fill=Y)

    # Buttons
    backButton = Button(abrvFrame, text="Back", padx=5, pady=5, command=GUISettings)
    addButton = Button(abrvFrame, text="Add", padx=5, pady=5)
    removeButton = Button(abrvFrame, text="Remove", padx=5, pady=5)

    # Labels
    mainLabel = Label(abrvFrame, text="SETTINGS/ABBREVIATIONS", bd=2, relief="solid", padx=5, pady=5)
    desiredStorageLocationsLable = Label(abrvFrame, text="Feature currently in development")
    currentStorageLocationLable = Label(abrvFrame, text="Enter storage location of non-sorted files:")


    # Text entry
    #renameEntry = Entry(abrvFrame, width=75, borderwidth=3)

    # Placing Labels on screen
    mainLabel.place(relx=.5, rely=0, anchor=N)
    desiredStorageLocationsLable.place(x=300, y=105, anchor=N)

    # Placing Listbox
    listbox.pack()
    scrollFrame.place(x=2, y=30)


    # Placing text entry on screen
    #renameEntry.place(relx=.5, rely=.5, anchor=N)

    # Placing Buttons on screen
    backButton.place(x=498, y=248, anchor=SE)
    addButton.place(x=220, y=248, anchor=S)
    removeButton.place(x=280, y=248, anchor=S)

    # packing all widgets to screen
    abrvFrame.pack()


def renameFile(file, abrvIn, filename):
    global abrvs
    global renameFrame
    global renameFrame2
    global clicked2
    print("\nOriginal File Name:", file, "| Chosen Abbreviation:", abrvIn, "| New File Name:", filename)

    # Original file name
    ogFile = ""

    # Has abbreviation been changed?
    abbreviationChange = False

    # Making sure user does not enter a space for the start of a name
    while filename.startswith(" "):
        filename = filename[1:len(filename)]

    # Check no change to name or abbreviation
    if filename == "" and abrvIn == "None":
        filename = file
        print("**No Changes Made**")

    # Check only abbreviation change
    elif filename == "" and abrvIn != "None":
        filename = file
        for tupleAb in abrvs:
            if file.startswith(tupleAb[0]):
                print("###", tupleAb[0])
                print(file[file.find(" ") + 1: len(file)])
                filename = file[file.find(" ") + 1: len(file)]
        abbreviationChange = TRUE
        print("**Abbreviation Changed**")

    # Check only name change
    elif filename != "" and abrvIn == "None":
        for tupleAb in abrvs:
            if file.startswith(tupleAb[0]):
                filename = file[0: file.find(" ") + 1] + filename
            else:
                filename = filename

        print("**File Name Changed**")

    # Check abbreviation and name change
    elif filename != "" and abrvIn != "None":
        abbreviationChange = TRUE
        print("**Abbreviation And File Name Changed**")

    # Find original File name with the .txt or .m4a ect.
    for x in os.listdir(saveLoc):
        if x.startswith(file):
            ogFile = x

    # Rename file
    if abbreviationChange and abrvIn == "Misc":
        # Move files that do not have abbreviation in front to Misc folder
        os.rename(saveLoc + "\\" + ogFile, saveLoc + "\\" + filename + ogFile[len(ogFile) - 4: len(ogFile)])

    elif abbreviationChange and abrvIn != "Misc":
        # Loop through abbreviations saved
        for abvTuple in abrvs:
            # Check if abbreviation chosen is in database
            if abvTuple[1] == abrvIn:
                os.rename(saveLoc + "\\" + ogFile, saveLoc + "\\" + abvTuple[0] + filename +
                          ogFile[len(ogFile) - 4: len(ogFile)])
    else:
        # print("Renaming File:", ogFile + " to", filename)
        os.rename(saveLoc + "\\" + ogFile, saveLoc + "\\" + filename + ogFile[len(ogFile) - 4: len(ogFile)])

    if clicked2 == 0:
        clicked2 = 1
        renameFrame3.pack_forget()
    else:
        clicked2 = 0
        renameFrame2.pack_forget()



    renameFilesGUI()


def updateFrame(frame):
    frame.update()


def updateRenameEntryText(entry, name, frame):
    # Fill text box with name
    entrytext = entry.get()
    if entrytext != "":
        print(entrytext.find(","))
        print(len(entrytext))
        if entrytext.find(",") == len(entrytext) - 1:
            entry.insert(len(entrytext), " " + name)
        elif entrytext.find(", ") == len(entrytext) - 2:
            entry.insert(len(entrytext), name)
    else:
        entry.delete(0, "end")
        entry.insert(0, name)

    # Quit Frame
    frame.destroy()


def namesWindow(entry):
    top = Toplevel()
    top.title("File Management System/Common Names")
    top.resizable(False, False)
    top.geometry("500x250")
    top.geometry("{}x{}+{}+{}".format(window_width, window_height, root.winfo_x(), root.winfo_y()))

    names = ["Vlad Denega", "Vlad Cherneta", "Oleg Strizheus", "Bogdan Strizheus", "Roman Strizheus",
             "Slavka Strizheus", "Andrey Pugach", "Sasha Karpovitch", "Alex Denega"]

    # Create Buttons with names on them
    name1Button = Button(top, text="Vlad Denega", padx=1, pady=1, command=lambda:
                        updateRenameEntryText(entry, names[0], top))
    name2Button = Button(top, text="Alex Denega", padx=1, pady=1, command=lambda:
                         updateRenameEntryText(entry, names[8], top))
    name3Button = Button(top, text="Vlad Cherneta", padx=1, pady=1, command=lambda:
                         updateRenameEntryText(entry, names[1], top))
    name4Button = Button(top, text="Oleg Strizheus", padx=1, pady=1, command=lambda:
                         updateRenameEntryText(entry, names[2], top))
    name5Button = Button(top, text="Bogdan Strizheus", padx=1, pady=1, command=lambda:
                         updateRenameEntryText(entry, names[3], top))
    name6Button = Button(top, text="Roman Strizheus", padx=1, pady=1, command=lambda:
                         updateRenameEntryText(entry, names[4], top))
    name7Button = Button(top, text="Slavka Strizheus", padx=1, pady=1, command=lambda:
                         updateRenameEntryText(entry, names[5], top))
    name8Button = Button(top, text="Andrey Pugach", padx=1, pady=1, command=lambda:
                         updateRenameEntryText(entry, names[6], top))
    name9Button = Button(top, text="Sasha Karpovitch", padx=1, pady=1, command=lambda:
                         updateRenameEntryText(entry, names[7], top))


    # Adding buttons to grid
    name1Button.grid(column=2, row=1, sticky='nesw', padx=2, pady=2)
    name2Button.grid(column=2, row=2, sticky='nesw', padx=2, pady=2)
    name3Button.grid(column=3, row=1, sticky='nesw', padx=2, pady=2)
    name4Button.grid(column=1, row=1, sticky='nesw', padx=2, pady=2)
    name5Button.grid(column=1, row=2, sticky='nesw', padx=2, pady=2)
    name6Button.grid(column=1, row=3, sticky='nesw', padx=2, pady=2)
    name7Button.grid(column=1, row=4, sticky='nesw', padx=2, pady=2)
    name8Button.grid(column=5, row=1, sticky='nesw', padx=2, pady=2)
    name9Button.grid(column=4, row=1, sticky='nesw', padx=2, pady=2)


def deleteListItem(item):
    filename = ""

    print()

    # Get file full file name
    for file in os.listdir(saveLoc):
        # Check to make sure that if nothing is selected things dont get deleted
        if item != "" and file.find(item) != -1:
            filename = file

    if filename != "":
        # Delete file by calling .bat file
        tempBat = open(r'' + os.getcwd() + "\\Src\\temp.bat", 'w+')
        tempBat.write("@echo off \ndel \"" + saveLoc + "\\" + filename + "\"")
        tempBat.close()

        # Call our temp bat file
        subprocess.call([r'' + os.getcwd() + "\\Src\\temp.bat"])
        # Delete our temp bat file
        subprocess.call([r'' + os.getcwd() + "\\Src\\master.bat"])

        # Update frame
        renameFilesGUI()


def renameFilesGUI():
    global renameFrame
    global renameFrame2
    global renameFrame3
    global clicked2
    # Hiding main menu screen widgets
    settingsFrame.pack_forget()
    mainFrame.pack_forget()
    renameFrame2.pack_forget()
    renameFrame3.pack_forget()

    # Create scroll frame
    scrollFrame = Frame(renameFrame)

    # Creating slider for window
    scroll = Scrollbar(scrollFrame, orient=VERTICAL)

    # Listbox for all file output
    listbox = Listbox(scrollFrame, width=25, height=10, yscrollcommand=scroll.set)

    # Create dropdown menu to change file type
    dropClick = StringVar()
    if clicked2 == 0:
        dropClick.set("None")
        dropdown = OptionMenu(renameFrame3, dropClick, *abrvs2)
        dropdown.config(width=10)
        dropdown.place(x=185, y=64, anchor=W)

    elif clicked2 == 1:
        dropClick.set("None")
        dropdown = OptionMenu(renameFrame2, dropClick, *abrvs2)
        dropdown.config(width=10)
        dropdown.place(x=185, y=64, anchor=W)

    # Adding all files in folder to list
    for file in os.listdir(saveLoc):
        while file.startswith(" "):
            os.rename(saveLoc + "\\" + file, saveLoc + "\\" + file[1:len(file)])
            print("Looping")
        if file.find("(autosaved)") < 0:
            listbox.insert(END, file[0:len(file) - 4])

    # Configure scroll bar for listbox
    scroll.config(command=listbox.yview)
    scroll.pack(side=RIGHT, fill=Y)

    # Text entry
    renameEntry = Entry(renameFrame, width=30, borderwidth=3)

    # Buttons
    namesButton = Button(renameFrame, text="Common Names", padx=2, pady=2, command=lambda: namesWindow(renameEntry))
    backButton = Button(renameFrame, text="Back", padx=5, pady=5, command=lambda: backToFrame(lastFrame))
    updateButton = Button(renameFrame, text="Update List", padx=1, pady=1, command=lambda:
                          renameFilesGUI())
    deleteButton = Button(renameFrame, text="Delete", padx=1, pady=1, command=lambda:
                          deleteListItem(listbox.get(ANCHOR)))
    renameButton = Button(renameFrame, text="Rename", padx=5, pady=5, command=lambda: [renameFile(listbox.get(ANCHOR),
                                                                                                  dropClick.get(),
                                                                                                  renameEntry.get())])

    # Labels
    mainLabel = Label(renameFrame, text="SETTINGS/RENAMING", bd=2, relief="solid", padx=5, pady=5)
    newFileNameLabel = Label(renameFrame, text="Enter File Name: ")
    newFileNameLabel2 = Label(renameFrame, text="Do NOT enter anything if\nonly changing file type")
    fileTypeLabel = Label(renameFrame, text="Select File Type:")
    fileTypeLabel2 = Label(renameFrame, text="Select 'None'\nif not\nchanging type")
    clickFileLabel = Label(renameFrame, text="^ Click File ^")


    # Placing Labels on screen
    mainLabel.place(relx=.5, rely=0, anchor=N)
    newFileNameLabel.place(x=340, y=40, anchor=W)
    newFileNameLabel2.place(x=325, y=100, anchor=W)
    fileTypeLabel.place(x=193, y=40, anchor=W)
    fileTypeLabel2.place(x=200, y=108, anchor=W)
    clickFileLabel.place(x=40, y=210, anchor=W)

    # Placing Listbox
    listbox.pack()
    scrollFrame.place(x=2, y=30)


    # Placing text entry on screen
    renameEntry.place(x=300, y=63, anchor=W)

    # Placing Buttons on screen
    backButton.place(x=498, y=248, anchor=SE)
    renameButton.place(x=250, y=248, anchor=S)
    updateButton.place(x=40, y=235, anchor=W)
    deleteButton.place(x=120, y=235, anchor=W)
    namesButton.place(x=390, y=140, anchor='center')


    # packing all widgets to screen

    if clicked2 == 0:
        renameFrame3.pack()
    elif clicked2 == 1:
        renameFrame2.pack()
    renameFrame.pack()


def backToFrame(frame):
    global mainFrame
    global settingsFrame
    if frame == mainFrame:
        mainGUI()
    elif frame == settingsFrame:
        GUISettings()


def infoScreen():
    # Hiding main menu screen widgets
    settingsFrame.pack_forget()
    mainFrame.pack_forget()

    # Buttons
    backButton = Button(infoFrame, text="Back", padx=5, pady=5, command=lambda: backToFrame(lastFrame))

    # Labels
    mainLabel = Label(infoFrame, text="SETTINGS/INFO", bd=2, relief="solid", padx=5, pady=5)
    infoLabel = Label(infoFrame, text="# To sort files just press 'Sort Recordings' on the main menu.\n\n"
                                      "# To edit where files are stored go to 'Settings' then click "
                                      "'Edit Directories'\n\n"
                                      "# You can rename files in the 'Rename Files' menu just follow prompts\n"
                                      "   P John = Sermon (John), S John = Song (John)\n\n"
                                      "# Abbreviations menu is currently in development...\n"
                                      "# Current abbreviations are:\n"
                                      "   P = Preacher, S = Song, V = Verse, PR = Prophecy, T = Testimony"
                      , anchor="e", justify=LEFT)

    # Placing Buttons on screen
    backButton.place(x=498, y=248, anchor=SE)

    # Placing Labels on screen
    mainLabel.place(relx=.5, rely=0, anchor=N)
    infoLabel.place(x=2, y=30, anchor=NW)

    backButton.config()

    # packing all widgets to screen
    infoFrame.pack()


def mainGUI():
    global lastFrame
    # Hiding settings screen widgets
    settingsFrame.pack_forget()
    renameFrame2.pack_forget()
    renameFrame3.pack_forget()
    renameFrame.pack_forget()
    infoFrame.pack_forget()

    # Set last frame
    lastFrame = mainFrame

    # Main Menu Labels
    mainLabel = Label(mainFrame, text="**************************************\n"
                                      "**************MAIN MENU***************\n"
                                      "**************************************")
    mainLabel2 = Label(mainFrame, text="!!Make Sure date and time on computer is correct!!")

    # Main menu buttons
    infoButton = Button(mainFrame, text="How to use", padx=5, pady=5, command=infoScreen)
    settingsButton = Button(mainFrame, text="Settings", padx=5, command=GUISettings)
    sortButton = Button(mainFrame, text="Sort recordings", padx=5, command=continueYear)
    renameButton = Button(mainFrame, text="Rename Files", padx=5, command=renameFilesGUI)

    # Disabling sort button if save file does not exist
    queryDataLoc()
    if noData:
        sortButton = Button(mainFrame, text="Sort recordings", padx=5, state=DISABLED)


    # Adding buttons to window
    sortButton.place(x=250, y=110, anchor='center')
    renameButton.place(x=250, y=140, anchor='center')
    settingsButton.place(x=250, y=200, anchor='center')
    infoButton.place(x=2, y=248, anchor=SW)

    # Placing Labels on screen
    mainLabel.place(x=250, y=2, anchor=N)
    mainLabel2.place(x=250, y=65, anchor='center')

    # Packing widgets into frame
    mainFrame.pack()


def queryDataLoc():  # Go through database and get needed storage info
    global saveLoc
    global wrkDir  # location chosen by user
    global noData
    # Connect to database
    conn = sqlite3.connect(os.getcwd() + '\\Src\\save_location')
    # Create cursor
    cS = conn.cursor()

    # Get info from database
    cS.execute("SELECT *, oid FROM saveLoc")
    records = cS.fetchall()
    # print(records)

    # Getting and assigning directories to vars
    try:
        saveLoc = str(records[0][0])
        wrkDir = str(records[0][1])
        noData = False
    except Exception:
        print("Error no data in table")
        noData = True


def saveDataLoc(data):  # Settings up saves when save button is clicked
    global saveLoc
    global wrkDir  # location chosen by user
    global year
    global clicked
    global dataList
    global storageFrame

    # Connect to database
    connSaveLoc = sqlite3.connect(os.getcwd() + '\\Src\\save_location')
    # Create cursor for database
    cS = connSaveLoc.cursor()  # for file save locations
    # Get previous data

    if clicked == 0:
        # Add data to list
        if data != "":
            dataList[0] = data
        dataList[1] = wrkDir
        clicked += 1
        # print(dataList)
    elif clicked == 1:
        if data != "":
            dataList[1] = data
        # print(dataList)
        # Add data to table in database
        cS.execute("INSERT INTO saveLoc VALUES (:from, :to)",
                   {
                       'from': dataList[0],
                       'to': dataList[1]
                   })

        # Empty list for next entry's
        dataList[0] = None
        dataList[1] = None
        # Commit changes to database
        connSaveLoc.commit()
        clicked = 0


# Checking if data base exists if not create tables for database (Start of program)
try:
    cA.execute("""CREATE TABLE file_abbreviations (
               folder_name text,
               abbreviation text
               )""")
except Exception:
    print("Table file_abbreviations exists")

try:
    cS.execute("""CREATE TABLE saveLoc (
               from_loc text,
               to_loc text
               )""")
except Exception:
    print("Table saveLoc exists")

# Create Master Batch File to call when deleting temp bat files
if not os.path.isfile(os.getcwd() + "\\Src" + "master.bat"):
    batpath = os.getcwd() + "\\Src\\" + "master.bat"

    # Create Path if does not exist
    if not os.path.exists(os.getcwd() + "\\Src"):
        os.mkdir(os.getcwd() + "\\Src\\")
    myBat = open(r'' + batpath, 'w+')
    myBat.write("@echo off \ndel \"" + os.getcwd() + "\\Src\\temp.bat\"")
    myBat.close()


# Calling our GUI main menu function
mainGUI()

# Commit changes to databases
connSaveLoc.commit()
connAbbreviations.commit()

# Closing databases
connAbbreviations.close()
connSaveLoc.close()

# Creating loop for window to run on, loops closes when program is closed
root.mainloop()
