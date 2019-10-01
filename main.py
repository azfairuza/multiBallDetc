import cv2
import numpy as np
import math
import csv

def printImage2JPG(image, folderName, frameNumber=1, Interval = 1):
    """a function to print an OpenCV image into a JPEG file at a directory

    :param image : OpenCV variable that contain image matrix
    :type image : img
    :param folderName : Folder directory of the printed image (JPEG image)
    :type folderName : str
    :param frameNumber : Current frame if the source is video. Default is 1.
    :type frameNumber : int
    :param Interval : Interval of printing image to JPEG if the source is
        video. Default is 1.
    :type Interval : int
    :return : none

    """


    # get filename so that it combined with the current frame number
    # and having jpeg extension
    filename = folderName +  "image ke-" + str(frameNumber) + '.jpeg'

    # checking if the frame number is at the interval.
    # If true then print the image
    if frameNumber % Interval == 0:
        cv2.imwrite(filename, image)
    return

def TrackingObject(oldPos, newPos, radList):
    """a function to track object identity that has been detected

    This function calculate and track the object identity by comparing
    list of position (x,y) in a previous frame and current frame. An
    object is said to be same from previous and current frame if it has
    shortest distance. The Object that has been given identity is excluded
    from calculation of shortest distance, therefore it will not get
    multiple identity. This function only works if the number of the objects
    is conserve. This function also sort the current object position and radius
    based on the identity

    :param oldPos: List of objects position in the previous frame
    :type oldPos : list
    :param newPos: list of objects position in the current frame
    :type newPos: list
    :param radList: list of objects radius in the current frame
    :type : list
    :return: list of sorted object position based on their identity
    :rtype: list
    """


    # checking whether oldPos has value or not. if oldPos
    # hasn't get any value, it must be the first frame.
    # So, there's no previous position list.
    if not oldPos :

        # it returns as it be
        return newPos, radList

    # if there is previous position list
    else:
        # a is just iterator variable
        a = 0

        # get the list size of oldPos
        sizeOldPos = len(oldPos)

        #for every object position in newPos (list of current position)
        for i in newPos :

            #for every object in oldPos that has not given identity
            for j in range(a,sizeOldPos) :

                # Remember that every position consist of (x,y)
                # So position[0] equal to x and position[1] equal to y
                xRange = int(i[0] - oldPos[j][0])
                yRange = int(i[1] - oldPos[j][1])

                # get the range distance by using phytagorean theorem
                Range = math.sqrt(math.pow(xRange,2) + math.pow(yRange, 2))

                # get the minimum distance of the object between previous
                # and the current frame
                if j == a:
                    minRange = Range
                    location = j
                else:
                    if minRange > Range:
                        minRange = Range
                        location = j

            # swap the element of newPos so it has same identity order as oldPos
            newPos[a], newPos[location] = newPos[location], newPos[a]

            # also for the radius
            radList[a], radList[location] = radList[location], radList[a]

            #increase the iterator
            a += 1

    #return sorted newPos and radList
    return newPos, radList

def clean():
    """ a function to clean a list

    :return: an empty list
    :rtype: list
    """


    A = []
    return A

def writingID(sortedPos, image):
    """ a function to write object ID at an image

    :param sortedPos: list of sorted object position
    :type sortedPos: list
    :param image: Image where to draw or write the ID
    """

    # Just an iterator variable
    a = 0;

    #  For every position in sortedPos list
    for i in sortedPos:
        # increase the iterator value by 1
        a += 1

        # draw a black filled circle with radius equal to 20 px
        cv2.circle(image, (i[0],i[1]), 20, (0, 0, 0), -1)

        # write the ID number at the center of object
        cv2.putText(image,str(a),(i[0]-10,i[1]+10), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255))

def writePosToCSV(csvFile, frameNumber, posList) :
    """ a function to write every position of object to a CSV file

    :param csvFile: file name and directory of CSV file
    :type csvFile: str
    :param frameNumber: current frame number of the position
    :type frameNumber: int
    :param posList: list of object position at the current frame number
    :type posList: list
    :return: None
    """

    # initiation for row container list
    row = []

    # adding frame Number to the first element
    row.append(frameNumber)

    # for every position in the position list
    for pos in posList:

        #for every component in the position
        for component in pos:

            # adding that component in to next element
            row.append(component)

    # open the csv file with append mode
    with open(csvFile, 'a') as writeFile:
        writer = csv.writer(writeFile)

        # insert the row list to next row in csv file
        writer.writerow(row)

    # close the csv file
    writeFile.close()

def InitPosToCSV(csvFile, ballNumber):
    """ a function to initiate writing position object into CSV file

    :param csvFile: file name and directory of CSV file
    :type csvFile: str
    :param ballNumber: total number of the object
    :type ballNumber: int
    :return: none
    """


    # Open the CSV file with write mode
    with open(csvFile, 'w') as writeFile:

        # Insert Frame in first column
        writeFile.write("Frame,")

        # For every object
        for i in range(ballNumber):

            # Write X + number Object in next column
            writeFile.write("X" + str(i+1) + ",")

            # Write Y + number Object in next column
            writeFile.write("Y" + str(i+1) + ",")

        # Change to the next row for further writing
        writeFile.write("\n")

    # Close the csv File
    writeFile.close()

def InitRadToCSV(csvFile, ballNumber):
    """ a function initiate writing radius object into csv file

    :param csvFile: file name and directory of the csv file
    :type csvFile: str
    :param ballNumber: total number of the object
    :type ballNumber: int
    :return: None
    """

    # Open the csv file with write mode
    with open(csvFile, 'w') as writeFile:

        # write Frame in the first column
        writeFile.write("Frame,")

        # for every object
        for i in range(ballNumber):

            # write redBall + object number in next column
            writeFile.write("radBall" + str(i+1) + ",")

        # change line for further writing
        writeFile.write("\n")

    # close the file
    writeFile.close()

def InitRangeToCSV(csvFile, ballNumber):
    """ a function to initiate writing distance between object to CSV file


    :param csvFile: file name and directory of csv file
    :type csvFile: str
    :param ballNumber: the total number of the object
    :type ballNumber: int
    :return: None
    """

    # initiate iterator variable
    a = 1

    # open the csv File in write mode
    with open(csvFile, 'w') as writeFile:

        # write Frame into first column
        writeFile.write("Frame,")

        # for every object
        for i in range(ballNumber):

            # also for every object but without itself
            # and without object that has been counted
            for j in range(a, ballNumber):

                #write range + combination of two object into next column
                writeFile.write("Range" + str(i+1) + str(j+1) + ",")

            # adding the iterator
            a += 1

        # Change line for further writing
        writeFile.write("\n")

    # Close the csv file
    writeFile.close()

def writeRadToCSV(csvFile, frameNumber, radList):
    """ a function to write object radius into csv file

    :param csvFile: file name and directory of the csv file
    :type csvFile: str
    :param frameNumber: current frame number of the object
    :type frameNumber: int
    :param radList: list of object radius
    :type: list
    :return: None
    """


    # Initiate for row container list
    row = []

    # Adding current frame Number to the row list
    row.append(frameNumber)

    #for every object radius in radList
    for rad in radList:

        # add the radius to the row list
        row.append(rad)

    # open the csv file in append mode
    with open(csvFile, 'a') as writeFile:
        writer = csv.writer(writeFile)

        # insert row list into next row on csv file
        writer.writerow(row)

    # close the csv file
    writeFile.close()

def writeRangeToCSV(csvFile, frameNumber, rangeBallList):
    """ a function to write range distance between objects into csv File

    :param csvFile: file name and directory of the csv file
    :type csvFile: str
    :param frameNumber: current frame number of the object
    :type frameNumber: int
    :param rangeBallList: list of range distance between every objects
    :type rangeBallList: list
    :return: None
    """


    # initiate row container list
    row = []

    # insert the current frame number to row list
    row.append(frameNumber)

    # for every range distance in rangeBallList
    for dist in rangeBallList:

        # insert the distance to row list
        row.append(dist)

    # open the csv file with append mode
    with open(csvFile, 'a') as writeFile:
        writer = csv.writer(writeFile)

        # insert row list into the next row of csv file
        writer.writerow(row)

    # close the file
    writeFile.close()

def calcRangeBall(sortedPos, ballNumber):
    """ a function to calculate range distance between objects

    :param sortedPos: list of sorted object position list
    :type sortedPos: list
    :param ballNumber: the total number of the object
    :type ballNumber: int
    :return: list of range distance between objects
    :rtype: list
    """

    # initiate a container list for range distance value
    rangeBallList = []

    # iterator variable
    a = 1

    # for every object position in sortedPos list
    for posA in sortedPos:

        # for every object position in sortedPos list
        # except itself and others which have been calculated
        for B in range(a, ballNumber):

            # calculate x distance
            xRange = int(posA[0] - sortedPos[B][0])

            # calculate y distance
            yRange = int(posA[1] - sortedPos[B][1])

            # calculate the range distance using phytagorean theorem
            Range = math.sqrt(math.pow(xRange, 2) + math.pow(yRange, 2))

            # insert the range distance value to rangeBallList
            rangeBallList.append(Range)

        # increase the iterator value by one
        a += 1

    # return the rangeBallList which contain calculated range distance
    return rangeBallList


#Settings path file and file name (Change the Green one)

pathFile = 'D:\\Project\\OpenCV Erlina\\'                   # Directory of the program file
openFile = pathFile +'video1.mp4'                           # Name of the input video, put video next to program file
csvPosFile = pathFile + 'dataPosBola.csv'                   # name of the csv file that contain object position
                                                            # over time
csvRadFile = pathFile + 'dataRadBola.csv'                   # name of the csv file that contain object radius over time
csvRangeBallFile = pathFile + 'dataRangeBola.csv'           # name of the csv file that contain object range distance
                                                            # over time
folderNameRaw = pathFile + 'output\\raw\\'                  # folder directory for saving raw image screenshot
folderNameHSV = pathFile + 'output\\hsv\\'                  # folder directory for saving HSV image screenshot
folderNameFiltered = pathFile + 'output\\filtered\\'        # folder directory for saving filtered image screenshot
folderNameResult = pathFile + 'output\\result\\'            # folder directory for saving result image screenshot
videoResultFile = pathFile + 'output\\video\\result.avi'    # folder directory for saving video result

#Settings System (change the value if system make false detection)
minBallRadius = 60      # minimum radius object that can be detected
maxBallRadius = 65      # maximum radius object that can be detected
minDistance = 125       # minimum distance between object that allowed
ballNumber = 2          # number object that need to be detected
Interval = 30           # use to capture screenshot per some frame
frameWidth = 1280       # frame width of the image
frameHeigth = 720       # frame height of the image
fps = 30                # frame per seconds of the video

# Setting flag (change based on fiture that wanted to use)
# Remember : more fitures make system slower
printRaw = True            # if True then system will print raw image per interval
printHSV = True            # if True then system will print HSV image per interval
printFiltered = True       # if True then system will print filtered image per interval
printResult = True         # if True then system will print result image per interval
renderVideoResult = True   # if True then system will render result video
getPositionBall = True      # if True then system will generate CSV file contained object position per frame
getRadiusBall = True        # if True then system will generate CSV file contained object radius per frame
getRangeBall = True         # if True then system will generate CSV file contained distance between objects per frame

#Settings for HSV treshold (change to detect object color)
h_Min = 0           # minimum hue, related to basic color
h_Max = 255         # maximum hue, related to basic color
s_Min = 0           # minimum saturated, related to shade
s_Max = 255         # maximum saturated, related to shade
v_Min = 10          # minimum value, related to brightness
v_Max = 255         # maximum value, related to brightness

# lower treshold is combined from minimum arguments
lowerTreshold = (h_Min, s_Min, v_Min)

# upper treshold is combined from maximum arguments
upperTreshold = (h_Max, s_Max, v_Max)

#Settings for boundary color (change to make boundary color better)
red = 0             # red value in RGB
green = 255         # green value in RGB
blue = 0            # blue value in RGB

# bounColor is RGB color format contain 3 variable above
boundColor = (blue, green, red)

#open the video file
capture = cv2.VideoCapture(openFile)

#checking render flag, if True then render
if renderVideoResult == True :
    render = cv2.VideoWriter(videoResultFile,                               # Video result name and director
                             cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),    # MJPG format is supported for AVI ext
                             fps, (frameWidth, frameHeigth))                # Properties of video

frameNumber = 0         # Initialize frame umber variable
oldPos = []             # Initialize old object position list
newPos = []             # Initialize new object position list
radList = []            # Initialize object radius list
rangeBallList = []      # Initalize range distance between objects list

# as long as video being opened
while(capture.isOpened()):

    # variable that count number object detected
    ballCount = 0

    # reading the video file, image send to frame, ret contain boolean True or False
    ret, frame = capture.read()

    # if there isn't any frame ret equal to False
    if ret == False:

        # break the while loop
        break

    # resize image so it will have same size
    frame = cv2.resize(frame, (frameWidth,frameHeigth))

    # add the frame number value by 1
    frameNumber += 1

    # check if print raw flag equal to True
    if printRaw == True:

        # printing raw image
        printImage2JPG(frame, folderNameRaw, frameNumber, Interval)

    # convert color space from RGB to HSV
    HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # check if print HSV flah equal to True
    if printHSV == True:

        # printing HSV image
        printImage2JPG(HSV, folderNameHSV, frameNumber, Interval)

    # filter image based on color treshold
    filtered = cv2.inRange(HSV,lowerTreshold,upperTreshold)

    # check if print Filtered flag equal to True
    if printFiltered == True:

        # Printing filtered image
        printImage2JPG(filtered, folderNameFiltered, frameNumber, Interval)

    # find contours in filtered image
    contours, hierrarchy = cv2.findContours(filtered, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # for every contour detected
    for cnt in contours:

        # find minimum enclosing circle
        (x,y) , radius = cv2.minEnclosingCircle(cnt)

        # get the center value
        center = (int(x), int(y))

        # get the radius value
        radius = int(radius)

        # if radius is inside of radius treshold
        if radius < maxBallRadius and radius > minBallRadius :

            # draw circle surrounding the object
            cv2.circle(frame, center, radius, boundColor, 2)

            # insert center position to newPos list
            newPos.append([int(x),int(y)])

            # insert object radius to radList list
            radList.append(radius)

            # increase the ballCount by 1
            ballCount += 1

        # if contour radius above the radius treshold
        elif radius >= 65 :

            # find a bounding rectangle
            x, y, w, h = cv2.boundingRect(cnt)      # (x,y) equal to bottom-left point, w = width, h = height

            # get Region of Interest (ROI) image within the bounding rectangle
            roiFrame = frame[y:y+h,x:x+w]

            # convert the color space of ROI image from RGB to Grayscale
            roiGray = cv2.cvtColor(roiFrame, cv2.COLOR_BGR2GRAY)

            # apply median blur to Grayscale ROI image
            roiGray = cv2.medianBlur(roiGray, 5)

            # find circle shape in Grayscale ROI image using hough transform
            circles = cv2.HoughCircles(roiGray, cv2.HOUGH_GRADIENT, 1,
                                       minDistance, None, 50, 30,
                                       minBallRadius, maxBallRadius)

            # if there is circle found
            if circles is not None :

                # change the type value to UINT16 and round it up
                circles = np.uint16(np.around(circles))

                # for every circle detected
                for i in circles[0,:] :

                    # draw circle surrounding the object
                    cv2.circle(roiFrame,(i[0],i[1]),i[2],boundColor, 2)

                    # insert center position to newPos list
                    newPos.append([i[0]+x, i[1]+y])

                    # insert object radius to radList list
                    radList.append(i[2])

                    # increase ballCount value by 1
                    ballCount += 1

    # if object detected is same with the number object that should be detected
    if ballCount == ballNumber:

        # track the object so it get sorted Position and Radius based by the identity
        oldPos, radList = TrackingObject(oldPos, newPos, radList)

        # calculate the range distance between objects
        rangeBallList = calcRangeBall(oldPos, ballNumber)

        # write ID object to result image
        writingID(oldPos, frame)

        # check get position objec flag
        if getPositionBall == True:

            # check frame Number
            if frameNumber == 1:

                # initialize CSV file if it is first frame
                InitPosToCSV(csvPosFile, ballNumber)

            # save object position to csv file
            writePosToCSV(csvPosFile, frameNumber, oldPos)

        # check get object radius flag
        if getRadiusBall == True:

            # check frame Number
            if frameNumber == 1:

                # initialize CSV file if it is first frame
                InitRadToCSV(csvRadFile, ballNumber)

            # save object radius to csv file
            writeRadToCSV(csvRadFile, frameNumber, radList)

        # check get range distance between object flag
        if getRangeBall == True:

            # check frame number
            if frameNumber == 1:

                # initialize CSV file if it is first time
                InitRangeToCSV(csvRangeBallFile, ballNumber)

            # save object range distance to csv file
            writeRangeToCSV(csvRangeBallFile, frameNumber, rangeBallList)

    # clean the newPos list
    newPos = clean()

    # clean the radList list
    radList = clean()

    # clean the rangeBallList
    rangeBallList = clean()

    # check print result value
    if printResult == True:

        # if True then printing the result image
        printImage2JPG(frame, folderNameResult, frameNumber, Interval)

    # check render result video flag
    if renderVideoResult == True:

        # write the video
        render.write(frame)

    # show the image in windows frame
    cv2.imshow('frame', frame)

    # if 'q' keyword pressed and image has been showed
    if cv2.waitKey(1) & 0xFF == ord('q'):

        # break the while loop
        break

# release capture
capture.release()

# check render result video flag
if renderVideoResult == True:

    # release render
    render.release()

# destroy all created windows frame
cv2.destroyAllWindows()