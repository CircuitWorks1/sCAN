'''
Created on Feb 17, 2019

This is a python script that parses the data of 2 CSV files, that were created using combination of CAN(controller area network) 
capture hardware and software. The script generates an output file, producing information showing how many times each hex value appears,
the hex values locations inside the IDs, and the frequency of changes in values between the two CSVs. This CAN data was produced by my motorcycle's
ECM(Engine Control Module). The purpose of these CAN capture sessions, and the script used to analyze them, is to reverse engineer 
the ECM and CAN definitions, so that I can design after market parts and software to interface with the ECM.

@author: Derrick
'''

import csv
# create a list of all potential hex values and format them similar to the hex values represented in the CAN capture data
hexlist = [hex(x) for x in range(256)]
hexlist = [s.replace('0x', '') for s in hexlist]
hexlist = [s.zfill(2) for s in hexlist]

print("", file=open("output.html", "w")) # create output file one
print("", file=open("output2.html", "w")) # create output file two

# user input to choose number of rows in the CSV you would like to scan. I typically scan 1000 to 5000 rows to assure enough
# data is gathered for accurate comparison
print("Number of lines you would like to scan:")
maxline = int(input())
# This is a variable used to keep track of the amount of times the checkfile1 function has been called to assign ID appearance
#count list to the correct global variable
ranonce = 0

# A dictionary of all the IDs with no leading zeros
idnozerosdict = dict.fromkeys(['100', '201', '202', '251', '300', '301', '302', '303', '304', '305', '306', '307',
                               '308', '400', '410', '420', '421', '422', '423', '430', '440', '450', '451', '460',
                               '461', '462', '463', '464', '465', '466', '467', '468', '469', '700', '701'])

# A dictionary of all the IDs with leading zeros
idzerosdict = dict.fromkeys(['00000100', '00000201', '00000202', '00000251', '00000300', '00000301', '00000302',
                             '00000303', '00000304', '00000305', '00000306', '00000307', '00000308', '00000400',
                             '00000410', '00000420', '00000421', '00000422', '00000423', '00000430', '00000440',
                             '00000450', '00000451', '00000460', '00000461', '00000462', '00000463', '00000464',
                             '00000465', '00000466', '00000467', '00000468', '00000469', '00000700', '00000701'])

# A function that will be called on each CAN capture session CSV, to gather all the data
def checkfile1(lFilename, hexvalue, list100, list201, list202, list251, list300, list301, list302, list303, list304,
               list305, list306, list307, list308, list400, list410, list420, list421, list422, list423, list430,
               list440, list450, list451, list460, list461, list462, list463, list464, list465, list466, list467,
               list468, list469, list700, list701, theIDCountList):
    global idCountList
    global idCountList_2
    global ranonce
    #open the CSV file
    with open(lFilename, mode='r') as csv_file:
        can_data = csv.DictReader(csv_file)

        # the "count" variable contains the number of times a given hex value appears in the given ID
        hexcount_dict = dict.fromkeys(
            ['onehundred_count', 'twoZeroOne_count', 'twoZeroTwo_count', 'twoFiveOne_count', 'threehundred_count',
             'threeZeroOne_count', 'threeZeroTwo_count', 'threeZeroThree_count', 'threeZeroFour_count',
             'threeZeroFive_count', 'threeZeroSix_count', 'threeZeroSeven_count', 'threeZeroEight_count',
             'fourhundred_count', 'fourTen_count', 'fourTwoZero_count', 'fourTwoOne_count', 'fourTwoTwo_count',
             'fourTwoThree_count', 'fourThreeZero_count', 'fourFourZero_count', 'fourFiveZero_count',
             'fourFiveOne_count', 'fourSixZero_count', 'fourSixOne_count', 'fourSixTwo_count', 'fourSixThree_count',
             'fourSixFour_count', 'fourSixFive_count', 'fourSixSix_count', 'fourSixSeven_count', 'fourSixEight_count',
             'fourSixNine_count', 'sevenhundred_count', 'sevenZeroOne_count'], 0)

        # This class contains the function used to execute the general counting of the hex values and number of times IDs appear in the capture sessions
        class theCounter:

            def __init__(self, count):
                self.count = count

            # Function used to tally IDs and hex values in those IDs
            def func_theCounter(x, idlong, idshort, hexcountvar):
                if row["Frame_ID"] == idlong or row["Frame_ID"] == idshort:
                    can_hex: str = (
                        f'\t{row["ByteA"]} {row["ByteB"]} {row["ByteC"]} {row["ByteD"]} {row["ByteE"]} {row["ByteF"]} {row["ByteG"]} {row["ByteH"]}')
                    hexcount_dict[hexcountvar] += (can_hex.count(hexlist[hexvalue]))
                    x.count += 1

        # Assign each ID an instance of the "theCounter" class
        p100, p201, p202, p251, p300, p301, p302, p303, p304, p305, p306, p307, p308, p400, p410, p420, p421, p422,\
        p423, p430, p440, p450, p451, p460, p461, p462, p463, p464, p465, p466, p467, p468, p469, p700, p701 = \
        theCounter(0), theCounter(0), theCounter(0), theCounter(0), theCounter(0), theCounter(0), theCounter(0), \
        theCounter(0), theCounter(0), theCounter(0), theCounter(0), theCounter(0), theCounter(0), theCounter(0), \
        theCounter(0), theCounter(0), theCounter(0), theCounter(0), theCounter(0), theCounter(0), theCounter(0), \
        theCounter(0), theCounter(0), theCounter(0), theCounter(0), theCounter(0), theCounter(0), theCounter(0), \
        theCounter(0), theCounter(0), theCounter(0), theCounter(0), theCounter(0), theCounter(0), theCounter(0)

        # Put each instance of the "theCounter" class into a list for easy iteration in loops
        plist = [p100, p201,  p202,  p251,  p300,  p301,  p302,  p303,  p304,  p305,  p306, p307,  p308,  p400,  p410,
                 p420,  p421,  p422,  p423,  p430,  p440,  p450, p451,  p460,  p461,  p462,  p463,  p464,  p465,  p466,
                 p467,  p468,  p469, p700,  p701]
        # A variable used to keep track of the number of rows scanned
        FileLine_count = 0

        # Call the function for every row in the capture sessions
        for row in can_data:

            #execute counter function on every ID
            for p in range(34):
                
                plist[p].func_theCounter(list(idzerosdict)[p], list(idnozerosdict)[p], list(hexcount_dict)[p])

            FileLine_count += 1
            print(FileLine_count)
            # exit for loop when the number of rows scanned are equal to the user input value
            if FileLine_count == maxline:
                break

        # list of ID appearances
        theIDCountList = [p100.count, p201.count, p202.count, p251.count, p300.count, p301.count, p302.count, p303.count,
                 p304.count, p305.count, p306.count, p307.count, p308.count, p400.count, p410.count, p420.count,
                 p421.count, p422.count, p423.count, p430.count, p440.count, p450.count, p451.count, p460.count,
                 p461.count, p462.count, p463.count, p464.count, p465.count, p466.count, p467.count, p468.count,
                 p469.count, p700.count, p701.count]
        # Create 2 lists containing the ID appearance counts for all 35 IDs in each capture session file
        if ranonce == 0:
            idCountList = theIDCountList.copy()
            ranonce += 1
        elif ranonce == 1:
            idCountList_2 = theIDCountList.copy()

        # This creats a series of comma seperated values for each ID that represents how many times each hex value is found
        list100.append(hexcount_dict['onehundred_count'])
        list201.append(hexcount_dict['twoZeroOne_count'])
        list202.append(hexcount_dict['twoZeroTwo_count'])
        list251.append(hexcount_dict['twoFiveOne_count'])
        list300.append(hexcount_dict['threehundred_count'])
        list301.append(hexcount_dict['threeZeroOne_count'])
        list302.append(hexcount_dict['threeZeroTwo_count'])
        list303.append(hexcount_dict['threeZeroThree_count'])
        list304.append(hexcount_dict['threeZeroFour_count'])
        list305.append(hexcount_dict['threeZeroFive_count'])
        list306.append(hexcount_dict['threeZeroSix_count'])
        list307.append(hexcount_dict['threeZeroSeven_count'])
        list308.append(hexcount_dict['threeZeroEight_count'])
        list400.append(hexcount_dict['fourhundred_count'])
        list410.append(hexcount_dict['fourTen_count'])
        list420.append(hexcount_dict['fourTwoZero_count'])
        list421.append(hexcount_dict['fourTwoOne_count'])
        list422.append(hexcount_dict['fourTwoTwo_count'])
        list423.append(hexcount_dict['fourTwoThree_count'])
        list430.append(hexcount_dict['fourThreeZero_count'])
        list440.append(hexcount_dict['fourFourZero_count'])
        list450.append(hexcount_dict['fourFiveZero_count'])
        list451.append(hexcount_dict['fourFiveOne_count'])
        list460.append(hexcount_dict['fourSixZero_count'])
        list461.append(hexcount_dict['fourSixOne_count'])
        list462.append(hexcount_dict['fourSixTwo_count'])
        list463.append(hexcount_dict['fourSixThree_count'])
        list464.append(hexcount_dict['fourSixFour_count'])
        list465.append(hexcount_dict['fourSixFive_count'])
        list466.append(hexcount_dict['fourSixSix_count'])
        list467.append(hexcount_dict['fourSixSeven_count'])
        list468.append(hexcount_dict['fourSixEight_count'])
        list469.append(hexcount_dict['fourSixNine_count'])
        list700.append(hexcount_dict['sevenhundred_count'])
        list701.append(hexcount_dict['sevenZeroOne_count'])

        # Create a list of all the hex count lists for easy iteration
        hexcountlists = [list100, list201, list202, list251, list300, list301, list302, list303, list304, list305, list306,
                         list307, list308, list400, list410, list420, list421, list422, list423, list430, list440, list450,
                         list451, list460, list461, list462, list463, list464, list465, list466, list467, list468, list469,
                         list700, list701]

        #prints number of times each hex values appears in a CSV list.
        if hexvalue == 255:
            for x in range(34):

                print(list(idnozerosdict)[x], "</br>", hexcountlists[x], "</br>", file=open("output.html", "a"))

            # A variable used to call list items
            p = 0

            for pcount in theIDCountList:
                print("</br>There are", pcount, "instances of the ID", list(idnozerosdict)[p], "in file", lFilename, file=open("output.html", "a"))
                # Increment list item call variable
                p += 1
            print("\n</br>", "\n</br>", "\n</br>", file=open("output.html", "a"))

# List variables used to store how many times each hex value is found in the related ID for the first data capture session
i = 0
onehundred_countlist = []
twoZeroOne_countlist = []
twoZeroTwo_countlist = []
twoFiveOne_countlist = []
threehundred_countlist = []
threeZeroOne_countlist = []
threeZeroTwo_countlist = []
threeZeroThree_countlist = []
threeZeroFour_countlist = []
threeZeroFive_countlist = []
threeZeroSix_countlist = []
threeZeroSeven_countlist = []
threeZeroEight_countlist = []
fourhundred_countlist = []
fourTen_countlist = []
fourTwoZero_countlist = []
fourTwoOne_countlist = []
fourTwoTwo_countlist = []
fourTwoThree_countlist = []
fourThreeZero_countlist = []
fourFourZero_countlist = []
fourFiveZero_countlist = []
fourFiveOne_countlist = []
fourSixZero_countlist = []
fourSixOne_countlist = []
fourSixTwo_countlist = []
fourSixThree_countlist = []
fourSixFour_countlist = []
fourSixFive_countlist = []
fourSixSix_countlist = []
fourSixSeven_countlist = []
fourSixEight_countlist = []
fourSixNine_countlist = []
sevenhundred_countlist = []
sevenZeroOne_countlist = []

# A list of the hex count lists
listofcountlists = [onehundred_countlist, twoZeroOne_countlist, twoZeroTwo_countlist, twoFiveOne_countlist, threehundred_countlist, threeZeroOne_countlist,
threeZeroTwo_countlist, threeZeroThree_countlist, threeZeroFour_countlist, threeZeroFive_countlist, threeZeroSix_countlist,
threeZeroSeven_countlist, threeZeroEight_countlist, fourhundred_countlist, fourTen_countlist, fourTwoZero_countlist,
fourTwoOne_countlist, fourTwoTwo_countlist, fourTwoThree_countlist, fourThreeZero_countlist, fourFourZero_countlist, fourFiveZero_countlist,
fourFiveOne_countlist, fourSixZero_countlist, fourSixOne_countlist, fourSixTwo_countlist, fourSixThree_countlist,
fourSixFour_countlist, fourSixFive_countlist, fourSixSix_countlist, fourSixSeven_countlist, fourSixEight_countlist,
fourSixNine_countlist, sevenhundred_countlist, sevenZeroOne_countlist]
idCountList = []
gFilename = 'Oil pressure-false.csv'

# Executes the "checkfile1" function the function is put in a while loop to be executed 255 times in order to search for all 255 hex values
while i < 256:
    checkfile1(gFilename, i, onehundred_countlist, twoZeroOne_countlist, twoZeroTwo_countlist, twoFiveOne_countlist,
               threehundred_countlist, threeZeroOne_countlist, threeZeroTwo_countlist, threeZeroThree_countlist,
               threeZeroFour_countlist, threeZeroFive_countlist, threeZeroSix_countlist, threeZeroSeven_countlist,
               threeZeroEight_countlist, fourhundred_countlist, fourTen_countlist, fourTwoZero_countlist,
               fourTwoOne_countlist, fourTwoTwo_countlist, fourTwoThree_countlist, fourThreeZero_countlist,
               fourFourZero_countlist, fourFiveZero_countlist, fourFiveOne_countlist, fourSixZero_countlist,
               fourSixOne_countlist, fourSixTwo_countlist, fourSixThree_countlist, fourSixFour_countlist,
               fourSixFive_countlist, fourSixSix_countlist, fourSixSeven_countlist, fourSixEight_countlist,
               fourSixNine_countlist, sevenhundred_countlist, sevenZeroOne_countlist, idCountList)
    i += 1

# List variables used to store how many times each hex value is found in the related ID for the first data capture session
i = 0
onehundred_countlist_2 = []
twoZeroOne_countlist_2 = []
twoZeroTwo_countlist_2 = []
twoFiveOne_countlist_2 = []
threehundred_countlist_2 = []
threeZeroOne_countlist_2 = []
threeZeroTwo_countlist_2 = []
threeZeroThree_countlist_2 = []
threeZeroFour_countlist_2 = []
threeZeroFive_countlist_2 = []
threeZeroSix_countlist_2 = []
threeZeroSeven_countlist_2 = []
threeZeroEight_countlist_2 = []
fourhundred_countlist_2 = []
fourTen_countlist_2 = []
fourTwoZero_countlist_2 = []
fourTwoOne_countlist_2 = []
fourTwoTwo_countlist_2 = []
fourTwoThree_countlist_2 = []
fourThreeZero_countlist_2 = []
fourFourZero_countlist_2 = []
fourFiveZero_countlist_2 = []
fourFiveOne_countlist_2 = []
fourSixZero_countlist_2 = []
fourSixOne_countlist_2 = []
fourSixTwo_countlist_2 = []
fourSixThree_countlist_2 = []
fourSixFour_countlist_2 = []
fourSixFive_countlist_2 = []
fourSixSix_countlist_2 = []
fourSixSeven_countlist_2 = []
fourSixEight_countlist_2 = []
fourSixNine_countlist_2 = []
sevenhundred_countlist_2 = []
sevenZeroOne_countlist_2 = []
idCountList_2 = []

# List of countlists to allow easy iteration in loop
listofcountlists_2 = [onehundred_countlist_2, twoZeroOne_countlist_2, twoZeroTwo_countlist_2, twoFiveOne_countlist_2, threehundred_countlist_2, threeZeroOne_countlist_2,
threeZeroTwo_countlist_2, threeZeroThree_countlist_2, threeZeroFour_countlist_2, threeZeroFive_countlist_2, threeZeroSix_countlist_2,
threeZeroSeven_countlist_2, threeZeroEight_countlist_2, fourhundred_countlist_2, fourTen_countlist_2, fourTwoZero_countlist_2,
fourTwoOne_countlist_2, fourTwoTwo_countlist_2, fourTwoThree_countlist_2, fourThreeZero_countlist_2, fourFourZero_countlist_2, fourFiveZero_countlist_2,
fourFiveOne_countlist_2, fourSixZero_countlist_2, fourSixOne_countlist_2, fourSixTwo_countlist_2, fourSixThree_countlist_2,
fourSixFour_countlist_2, fourSixFive_countlist_2, fourSixSix_countlist_2, fourSixSeven_countlist_2, fourSixEight_countlist_2,
fourSixNine_countlist_2, sevenhundred_countlist_2, sevenZeroOne_countlist_2]

# The file name of the second CSV file being analized
gFilename_2 = 'Oil pressure-true.csv'

# Executes the "checkfile1" function the function is put in a while loop to be executed 255 times in order to search for all 255 hex values
# in all 35 IDs
while i < 256:
    checkfile1(gFilename_2, i, onehundred_countlist_2, twoZeroOne_countlist_2, twoZeroTwo_countlist_2,
               twoFiveOne_countlist_2, threehundred_countlist_2, threeZeroOne_countlist_2, threeZeroTwo_countlist_2,
               threeZeroThree_countlist_2, threeZeroFour_countlist_2, threeZeroFive_countlist_2,
               threeZeroSix_countlist_2, threeZeroSeven_countlist_2, threeZeroEight_countlist_2,
               fourhundred_countlist_2, fourTen_countlist_2, fourTwoZero_countlist_2, fourTwoOne_countlist_2,
               fourTwoTwo_countlist_2, fourTwoThree_countlist_2, fourThreeZero_countlist_2, fourFourZero_countlist_2,
               fourFiveZero_countlist_2, fourFiveOne_countlist_2, fourSixZero_countlist_2, fourSixOne_countlist_2,
               fourSixTwo_countlist_2, fourSixThree_countlist_2, fourSixFour_countlist_2, fourSixFive_countlist_2,
               fourSixSix_countlist_2, fourSixSeven_countlist_2, fourSixEight_countlist_2, fourSixNine_countlist_2,
               sevenhundred_countlist_2, sevenZeroOne_countlist_2, idCountList_2)
    i += 1

# a function used to compare the number of times each hex value was found in a given ID and print that info in the output file
def func_compare(thepercent, countlist1, countlist2, theid, idcount1, idcount2):
    global i
    # If the hex value appears zero times in both files, then do nothing
    if countlist2 == 0 and countlist1 == 0:
        return
    # If only one of the values are equal to zero, then determine if the number of hex appearances is equal to the number of ID apperances
    if min(countlist2, countlist1) == 0:
        a_set = [countlist1, countlist2]
        print(theid, "id count:",idcount1, idcount2)
        print(hexlist[i], "hex value count:",countlist1, countlist2)
        b_set = [idcount1, idcount2]
        check = any(item in a_set for item in b_set)
        # if the number of hex appearances, is equal to the number of ID apperances, then highlight in red else print without red highlight
        if check is True:
            print("<font color='red'>hex value ", hexlist[i],"(","{0:08b}".format(int(hexlist[i], 16)),") in ID", theid,", has had an increase from zero appearances to ",
                  max(countlist1, countlist2), " appearances</font></br>", sep='', file=open("output2.html", "a"))
        else:
            print("hex value ", hexlist[i],"(","{0:08b}".format(int(hexlist[i], 16)),") in ID", theid,", has had an increase from zero appearances to ",
                  max(countlist1, countlist2), " appearances</br>", sep='', file=open("output2.html", "a"))
        return
    # Determine what the increase/decrease percentage is of the given hex value appearance
    if countlist2 >= countlist1:
        thepercent = countlist2 / countlist1
    if countlist1 >= countlist2:
        thepercent = countlist1 / countlist2
    if thepercent >= 1.50:
        print("hex value", hexlist[i], "in ID", theid, ", has an increase or decrease in appearances of greater than 50%</br>",file=open("output.html", "a"))

# These variables are used to store the quotient or the percentage change of a hex value between the 2 CSVs
i=0
onehundred_percent = 0
twoZeroOne_percent = 0
twoZeroTwo_percent = 0
twoFiveOne_percent = 0
threehundred_percent = 0
threeZeroOne_percent = 0
threeZeroTwo_percent = 0
threeZeroThree_percent = 0
threeZeroFour_percent = 0
threeZeroFive_percent = 0
threeZeroSix_percent = 0
threeZeroSeven_percent = 0
threeZeroEight_percent = 0
fourhundred_percent = 0
fourTen_percent = 0
fourTwoZero_percent = 0
fourTwoOne_percent = 0
fourTwoTwo_percent = 0
fourTwoThree_percent = 0
fourThreeZero_percent = 0
fourFourZero_percent = 0
fourFiveZero_percent = 0
fourFiveOne_percent = 0
fourSixZero_percent = 0
fourSixOne_percent = 0
fourSixTwo_percent = 0
fourSixThree_percent = 0
fourSixFour_percent = 0
fourSixFive_percent = 0
fourSixSix_percent = 0
fourSixSeven_percent = 0
fourSixEight_percent = 0
fourSixNine_percent = 0
sevenhundred_percent = 0
sevenZeroOne_percent = 0

# List of percent values to allow easy iteration in loop
listofpercents = [onehundred_percent, twoZeroOne_percent, twoZeroTwo_percent, twoFiveOne_percent, threehundred_percent, threeZeroOne_percent, threeZeroTwo_percent,
threeZeroThree_percent, threeZeroFour_percent, threeZeroFive_percent, threeZeroSix_percent, threeZeroSeven_percent, threeZeroEight_percent,
fourhundred_percent, fourTen_percent, fourTwoZero_percent, fourTwoOne_percent, fourTwoTwo_percent, fourTwoThree_percent, fourThreeZero_percent,
fourFourZero_percent, fourFiveZero_percent, fourFiveOne_percent, fourSixZero_percent, fourSixOne_percent, fourSixTwo_percent, fourSixThree_percent,
fourSixFour_percent, fourSixFive_percent, fourSixSix_percent, fourSixSeven_percent, fourSixEight_percent, fourSixNine_percent, sevenhundred_percent,
sevenZeroOne_percent]

# Brief discription of data output
print("<font size = '4' face='arial'>This output shows the number of times a hex value appears in a given ID if its apperance count was zero "
      "in either of the can capture sessions. The line will be highlighted in red if the number of "
      "hex value appearences, is equal to the number of appearences of its given ID. Meaning, the value went from appearing"
      "zero times, to appearing 100% of the time.</font></br><hr>", file=open("output2.html", "a"))

# Print HTML format open tags
print("<body style='padding: 20px;'><font size='5' face='arial'><b>", file=open("output2.html", "a"))

# Apply the compare function to all IDs(35) for all hex values ranging from 0 to 255(00-FF)
for x in range(34):
    for i in range(256):
        func_compare(list(listofpercents)[x], listofcountlists[x][i], listofcountlists_2[x][i], list(idnozerosdict)[x], idCountList[x], idCountList_2[x])
# Print HTML format closing tags
print("</font></b></body>", file=open("output2.html", "a"))