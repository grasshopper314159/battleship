# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 00:20:19 2015

@author: Nate
"""

# import *.* from zellegraphics.py
from zellegraphics import *
from random import *
from time import sleep
from math import floor

# These are constants to specify the size of the windown and number /
#and number of squares on the board, etc.

cellsize = 35
cellspacing = 5
labelbuffer = 40
winhordim = 1000
winverdim = 600

#each board is 10 x 10 cells
counthorcells = 10
countvercells = 10

#there are two boards with one blank row between them
totalhor = 21
totalver = 10
#xshift is how many cells to the right the print function has to shift to print on the right-hand grid
xshift = 11



#These are used to calculate various statistics, e.g. on average, how many "shots" 
# does the computer need to completely sink all the ships if it's playing itself.

runs = 1   #number of games computer will play. Set to 1` for playing against a person
runtotal = 0 #total number of shots taken in "runs" # of games
averuns = 0 #average number of shots needed to win game
attempts = 0 # how many shots are taken in one run, not currently used in player vs computer game
runcount = 0 # number of games played, compared to runs for looping

#Time to pause between drawing shots
shortpause = .009
longpause = .25


    ###################################### arrayInit(x)################
#This functions initializes arrays used to track ship placement
#Calls:
#Called By: 
def arrayInit():
    # I don't really get this syntax...cut and paste from stackexchange
	# but it makes a 10 by 10 array of zeros in this case
    name = [[0 for x in range(counthorcells)] for x in range(countvercells)]
    return name

	#checks for hit and also records hit
def checkforhit(x,y,cmapu):
    if cmapu[y][x] == 1:
        hit = True
		#when there's a hit, the location turns to zero
        cmapu[y][x] = 0
    else:
        hit = False
    return hit


  ##########################   check_click###############
#This functions (used to input a player ship)  looks to see 
#   if a cell has already been clicked, 
#Calls: 
#Called By:  structured clicking

def check_click(x,y,mapr,clickcount):
    if x == -99:
        return false
    if mapr[y][x] == 1:
        return False
 #   if clickcount == 0 or 1:
#        return True
    else:
        return True
        
        
  ##########################   drawboard   ######################
#This functions alternates colors between runs
#Calls: paintcolor
#Called By:  main

def drawboard(winhordim, winverdim, cellsize, counthorcells, countvercells,win):
    #win = GraphWin("BattleShip", winhordim, winverdim)
    for v in range(countvercells):
        for h in range(counthorcells):
            #if v == 0:
            #    Text(Point(5+20*h, 25),string(h))
            upperleftx = labelbuffer+cellspacing+cellsize*h
            upperlefty = labelbuffer+cellspacing+cellsize*v
            lowerrightx = labelbuffer+cellsize+cellsize*h
            lowerrighty = labelbuffer+cellsize+cellsize*v
            r = Rectangle(Point(upperleftx,upperlefty), Point(lowerrightx,lowerrighty))
            r.setFill(paintcolor('backg', runcount))
            r.draw(win)
            #this applies the labels
			#v = 0 is the top row
            if v == 0:
			#h = 10 is the empty row between the boards
                if h == 10:
                    pass
                #this applies the column numberes for the right hand board (h-10)
                elif h>10:
                    Text(Point(labelbuffer+cellsize*h+cellspacing+15, 25),h-10).draw(win)
                #this applies the column numberes for the left hand board (h+1)
                else:
                    Text(Point(labelbuffer+cellsize*h+cellspacing+15, 25),h+1).draw(win)    
            #this prints the row lables: a through J
            if h == 0:
                Text(Point(20, labelbuffer+cellsize*v+cellspacing+15), chr(65+v)).draw(win)
    #this draws the strip between the two boards
    for v in range(countvercells):
        upperleftx = labelbuffer+cellspacing+cellsize*10
        upperlefty = labelbuffer+cellspacing+cellsize*v
        lowerrightx = labelbuffer+cellsize+cellsize*10
        lowerrighty = labelbuffer+cellsize+cellsize*v
        r = Rectangle(Point(upperleftx,upperlefty), Point(lowerrightx,lowerrighty))
        r.setFill('black')
        r.draw(win)

        
  ##########################   drawship  ######################
#This functions handles the actual drawing
#Calls: 
#Called By:  placeship


def drawship(x,y,direction,size,win, runcount):
#direction  = 1 means horizontal going to the right, 2 means vertical going down 
#runcount was used to alternate colors between runs, but not used for plyr v cmptr.

    if direction == 1:
        for i in range(size):            
            upperleftx = labelbuffer+cellspacing+cellsize*(x+i)
            upperlefty = labelbuffer+cellspacing+cellsize*y
            lowerrightx = labelbuffer+cellsize+cellsize*(x+i)
            lowerrighty = labelbuffer+cellsize+cellsize*y
            r = Rectangle(Point(upperleftx,upperlefty), Point(lowerrightx,lowerrighty))
            r.setFill(paintcolor('ship', runcount))
            r.draw(win)
            #not necessary because of map ship?  cmapu[y][x] = 1
            #Text(Point(labelbuffer+cellsize*x+cellspacing+15, y),direction).draw(win)
    
    if direction == 2:
        for i in range(size):
            upperleftx = labelbuffer+cellspacing+cellsize*x
            upperlefty = labelbuffer+cellspacing+cellsize*(y+i)
            lowerrightx = labelbuffer+cellsize+cellsize*x
            lowerrighty = labelbuffer+cellsize+cellsize*(y+i)
            r = Rectangle(Point(upperleftx,upperlefty), Point(lowerrightx,lowerrighty))
            r.setFill(paintcolor('ship', runcount))
            r.draw(win)        
 #direction  = 3 means horizontal going to the left, 4 means vertical going up,           
    if direction == 3:
        for i in range(size):            
            upperleftx = labelbuffer+cellspacing+cellsize*(x-i)
            upperlefty = labelbuffer+cellspacing+cellsize*y
            lowerrightx = labelbuffer+cellsize+cellsize*(x-i)
            lowerrighty = labelbuffer+cellsize+cellsize*y
            r = Rectangle(Point(upperleftx,upperlefty), Point(lowerrightx,lowerrighty))
            r.setFill(paintcolor('ship', runcount))
            r.draw(win)    

    if direction == 4:
        for i in range(size):
            upperleftx = labelbuffer+cellspacing+cellsize*x
            upperlefty = labelbuffer+cellspacing+cellsize*(y-i)
            lowerrightx = labelbuffer+cellsize+cellsize*x
            lowerrighty = labelbuffer+cellsize+cellsize*(y-i)
            r = Rectangle(Point(upperleftx,upperlefty), Point(lowerrightx,lowerrighty))
            r.setFill(paintcolor('ship', runcount))
            r.draw(win)  


  ##########################   get_click###############
#This functions gets the coor. of a click and converts them to cells
#Calls: 
#Called By:  structured clicking

def get_click(win):
        mouse = win.getMouse()
        #x = floor((mouse.getX()-labelbuffer+cellspacing)/cellsize)
        #y = floor((mouse.getY()-labelbuffer+cellspacing)/cellsize)
        x = floor((mouse.getX()-labelbuffer-2)/cellsize)
        y = floor((mouse.getY()-labelbuffer)/cellsize)
        #Debug
		#print("getclick x: ", x, "getclick y", y)
        return x,y
        
          
  ##########################   getrandomxy  ######################
#This function gives random starting coordinates and a vector
#for placing the computer ships
#Calls: 
#Called By:  placeship
def getrandomxy(counthorcells, countvercells, cellsize, cellspacing):
    x = randrange(0,counthorcells)
    y = randrange(0,countvercells)
    direction = randrange(1,3)
    #direction=2
    return x, y, direction



#this replaces random shot when the computer has scored a hit
#it will try one square to the right, then left, then up, then down    

def hunt(cmapu,cmapr, pmapu, pmapr, cshotmap,x,y, attempts, win, runcount):
    #1 right 2 down 3 left 4 up
    direction = 1
    while direction == 1:
        streak = 0
        while x+1<counthorcells and cshotmap[y][x+1] == 0:
            sleep(longpause)
            streak += 1
            attempts += 1
            user_shot(cmapu,cmapr, win)            
            cshotmap[y][x+1] = 1
            hit = checkforhit(x+1,y,pmapu)
            paintShot(x+1,y,hit,win,pmapr,runcount)
            if hit == False:
                x -= streak-1
                direction = 3
            else:
                x += 1
        direction = 3
     #1 right 2 down 3 left 4 up           
    while direction == 3:
        streak = 0
        while x-1 >= 0 and cshotmap[y][x-1] == 0:
            streak += 1
            sleep(longpause)
            attempts += 1
            cshotmap[y][x-1] = 1
            user_shot(cmapu,cmapr, win)  
            hit = checkforhit(x-1,y,pmapu)
            paintShot(x-1,y,hit,win,pmapr,runcount)
            
            if hit == False:
                direction = 4
            else:
                x -= 1
        direction = 4
     #1 right 2 down 3 left 4 up      
    while direction == 4:
        streak = 0
        while y-1 >= 0 and cshotmap[y-1][x] == 0:
            sleep(longpause)
            streak += 1
            attempts += 1
            cshotmap[y-1][x] = 1
            user_shot(cmapu,cmapr, win)
            
            hit = checkforhit(x,y-1,pmapu)
            paintShot(x,y-1,hit,win,pmapr,runcount)
            
            if hit == False:
                y += streak-1
                direction = 2
            else:
                y -= 1
        direction = 2
     #1 right 2 down 3 left 4 up            
    while direction == 2:
        while y+1 < countvercells and cshotmap[y+1][x] == 0:
            sleep(longpause)
            attempts += 1
            cshotmap[y+1][x] = 1
            user_shot(cmapu,cmapr, win)
            hit = checkforhit(x,y+1,pmapu)
            paintShot(x,y+1,hit,win,pmapr,runcount)
            
            if hit == False:
                direction = 5
            else:
                y += 1
        direction = 5
        
        
        ###################################### mapship(x)################
#This functions updates the map and places the ships on it
#Calls:
#Called By: placeship
def mapship(x,y,direction,size, cmapu):
    if direction == 1:
        for i in range(size): 
            cmapu [y][x+i] = 1
                
    if direction == 2:
        for i in range(size):
            cmapu [y+i] [x] = 1

    if direction == 3:
        for i in range(size): 
            cmapu [y][x-i] = 1    
      
    if direction == 4:
        for i in range(size):
            cmapu [y-i] [x] = 1



  ##########################   paint_click###############
#This functions paints a click based on cell location
#Calls: 
#Called By:  structured clicking

def paint_click(x,y,win):
        upperleftx = labelbuffer+cellspacing+cellsize*(x)
        upperlefty = labelbuffer+cellspacing+cellsize*y
        lowerrightx = labelbuffer+cellsize+cellsize*(x)
        lowerrighty = labelbuffer+cellsize+cellsize*y
        r = Rectangle(Point(upperleftx,upperlefty), Point(lowerrightx,lowerrighty))
        r.setFill(paintcolor('ship',0))
        r.draw(win)
        

  ########################## paintcolor(key,runcount)######################
#This functions alternates colors between runs
#Calls:
#Called By:  paintshot, drawboard, drawship 

def paintcolor(key,runcount):
    #debug print
    #print("runcount =", runcount)
    if runcount % 2 == 0:
        colordict = {
                        'backg' : 'blue',
                        'ship' : 'yellow',
                        'miss' : 'grey',
                        'hit' : 'red'}
    else:
         colordict = {
                        'backg' : 'blue',
                        'ship' : 'green',
                        'miss' : 'grey',
                        'hit' : 'red'}
    return colordict[key]


  ##########################paintShot(x,y,hit,win,cmapr, runcount)######################
#This functions draws shots, different colors depending on hit or miss
#Calls: paintcolor
#Called By:  main
def paintShot(x,y,hit,win,cmapr, runcount):
        upperleftx = labelbuffer+cellspacing+cellsize*(x)
        upperlefty = labelbuffer+cellspacing+cellsize*y
        lowerrightx = labelbuffer+cellsize+cellsize*(x)
        lowerrighty = labelbuffer+cellsize+cellsize*y
        r = Rectangle(Point(upperleftx,upperlefty), Point(lowerrightx,lowerrighty))
        if x>9:
            if cmapr[y][x-xshift] == 1:  #avoid painting over old hits
                hit = True
        else:
            if cmapr[y][x] == 1:  #avoid painting over old hits
                hit = True        
        if hit == False:
            r.setFill(paintcolor('miss', runcount))
        else:
            r.setFill(paintcolor('hit', runcount))
        r.draw(win)
        sleep(shortpause)

def cpaintShot(x,y,hit,win,cmapr, runcount):
        upperleftx = labelbuffer+cellspacing+cellsize*(x)
        upperlefty = labelbuffer+cellspacing+cellsize*y
        lowerrightx = labelbuffer+cellsize+cellsize*(x)
        lowerrighty = labelbuffer+cellsize+cellsize*y
        r = Rectangle(Point(upperleftx,upperlefty), Point(lowerrightx,lowerrighty))
        if x>9:
            if cmapr[y][x-xshift] == 1:  #avoid painting over old hits
                hit = True
        else:
            if cmapr[y][x] == 1:  #avoid painting over old hits
                hit = True        
        if hit == False:
            r.setFill(paintcolor('miss', runcount))
        else:
            r.setFill(paintcolor('hit', runcount))
        r.draw(win)
        sleep(shortpause)
  ##########################   placeship  ######################
#This function will place a ship of size "size" on the board and
#record it
#Calls: getrandomxy, testxy, drawship, mapship
#Called By:  placeships

def placeship(size,win, cmapu, runcount):
    didit = False
    #loops and continutes to get random coordinates until testxy verifies they 
	#don't put a ship off the board or onto another ship
    while didit == False:
        x,y,direction = getrandomxy(counthorcells, countvercells, cellsize, cellspacing)
               
        if testxy(x,y,direction,size, cmapu):
            didit = True
    #drawship(rightshift(x),y,direction,size,win, runcount)
    mapship(x,y,direction,size,cmapu)
    #return x,y

 
###################################### placeships###########
#This functions places many ships and records them
#onto the computers map of record
#Calls: placeship(s1,win, cmapu, runcount)
#Called By:main

def placeships(comp_ship_list,win, cmapu, cmapr,runcount):
    for n in comp_ship_list:    
        placeship(n,win, cmapu, runcount)

    #copies map into cmaor- which will stay unmodified 
    for v in range(countvercells):
        for h in range(counthorcells):
            cmapr[v][h]=cmapu[v][h]
    return cmapr 

######################### This will replace randomShot eventually *********
def probability_shot():
    pass
    
########################## randomShot(cmapu)######################
#This functions takes a random shot and records if its a hit
#Calls:
#Called By:  main()
def randomShot(cmapu,cshotmap):
    hit = False
    x = randrange(counthorcells)
    y = randrange(countvercells)
#this makes sure we haven't fired somewhere we've fired before    
    while cshotmap[y][x] != 0: 
        x = randrange(counthorcells)
        y = randrange(countvercells)
    hit = checkforhit(x,y,cmapu)
	#updates computer shot record
    cshotmap[y][x] = 1
    return x, y, hit

###################### to print on the right-hand grid #############
def rightshift(x):
    x += xshift
    return x
    
#used by function that gets player input to 
#place ships
def store_click(x,y,mapr):
    mapr[y][x] = 1
    return mapr


######### This is to put one ship on the board.
# Two clicks next to each other will place a ship, 
#since that is enough to determine the starting 
#point and direction
#it will try once and then return true if it could place a ship and 
#false if not. It needs to called repeatedly if player input is bad.

#Called by user_ship_input

def structured_clicking(size, pmapr, pmapu, win):
    clickcount = 0
    x1 = 0
    y1 = 0
    direction = 0
    while clickcount < 2:
        x,y = get_click(win)
		#checks to see if there is already a ship placed there (pmapr)
        if pmapr[y][x] == 0:
		#this checks the updated map (pmapu) to see of the player is clicking 
		# on a square just clicked on (in order to unclick it)
            if check_click(x,y,pmapu,clickcount):
                paint_click(x,y,win)
                store_click(x,y,pmapu)
                clickcount += 1
                #debug:
				# print("clickcount ", clickcount)
                if clickcount == 1:
				#debug:
                    #print("clickcount ", clickcount)
					#records the first click in x1. y1
                    x1 = x
                    y1 = y
            else:
			#the player can click on a square unclick it if he or she 
			#changes his or her mind
                unclick(x,y,pmapu,win)
                clickcount -= 1
    ##debug:
	#print("x: ",x, "y:", y, "x1: ", x1, "y1: ", y1)
	#Determine the orientation the player want the ship laid out
    if x == (x1+1) and y == y1:
        direction = 1
    if x == (x1-1)and y == y1:
        direction = 3
    if y == (y1+1)and x == x1:
        direction = 2
    if y == (y1-1)and x == x1:
        direction = 4
    #debug:
	#print("direction", direction)
    #print("^^^^^^^^^^^^^^^^^^^^^calling test xy")
	#testxy verifies that desired location is ok
    if testxy(x1, y1, direction,size, pmapr) and direction != 0: #  "Direction != 0" necessary?
        #debug:
		#print("passed testxy passed")
        drawship(x1,y1,direction,size,win, 0)
        mapship(x1,y1,direction,size, pmapu)
		#copies the ship to the map of record
        update_map(pmapu,pmapr)
		#clears pmapu for next ship input
        pmapu = arrayInit()
        #Debug 
		#print('returning true')
        return True
    else:
        unclick(x,y,pmapu,win)
        unclick(x1,y1,pmapu,win)
        clickcount -= 2
        #pmapr [y] [x] =  0
        #pmapr [y1] [x1] =  0
        #Debug 
		#print("returning false")
        return False
        #structured_clicking(size, pmapr,pmapu, win)
        
    
  ########################## sumCalc(array)######################
#This adds up all the numbers in an array
#Calls:
#Called By:  main() 
    
def sumCalc(array):
    summ = 0
    for v in range(countvercells):
        for h in range(counthorcells):
            summ += array[v][h]
    return summ



  ##########################   testxy  ######################
#This functions tests to see if the random coor or player coor
#that represents the start of a ship 
#will put a ship out of bounds or overlap another ship 
#Calls: 
#Called By:  placeship
def testxy(x, z, direction,size, cmapu):
    print("called testxy")
    dimcheck = False
    check = 0
    #debug prints
    #print("x and z:",x,z)
    print("Direction:",direction)
    #print("Size:",size)
    
    #check if it goes off the map
    #directions: 1 right, 2 down, 3 left, 4 up
    if direction == 1:
        
        if x+size-1<counthorcells:
            dimcheck = True
    if direction == 2:
        print("z: ",z,"size:",size,"x",x)  
        if z+size-1 < countvercells:
            dimcheck = True
    if direction == 3:
        if x-size+1 > -1:
            dimcheck = True
    if direction == 4:
        if z-size+1 > -1:
            dimcheck = True
    if dimcheck  ==  False:
        #debug print
        print("xy dimcheck is False")
        return False
    #debug print
    print(dimcheck)
	
	
    #Checks to see if the new ship will overlap an existing ship
    if direction == 1:
        for i in range(size): 
            #debug print
            #print("i:",i,"z:",z,"x+i:",x+i)
            check = check+cmapu[z][x+i]
                
    if direction == 2:
        for i in range(size):
            #debug print
			#print("z: ",z,"i:",i,"x",x)  
            check = check+cmapu[z+i] [x]
            
    if direction == 3:
        for i in range(size): 
            #debug print
            #print("i:",i,"z:",z,"x+i:",x+i)
            check = check+cmapu[z][x-i]     
            
    if direction == 4:
        for i in range(size):
              
            check = check+cmapu [z-i] [x]
    #debug print       
    #print("xy check intersection check ",check)
    if check == 0:
        #debug print
        print("Final check: True")        
        return True
    #debug print
	#print("Final check: False")      
    return False
    #return TrueCS

   ##########################   unclick###############
#This functions reverts a cell to the background color and changes
        # the corresponding map location to 0
#Calls: 
#Called By:  structured clicking
        
def unclick(x,y,pmapr,win):
        upperleftx = labelbuffer+cellspacing+cellsize*(x)
        upperlefty = labelbuffer+cellspacing+cellsize*y
        lowerrightx = labelbuffer+cellsize+cellsize*(x)
        lowerrighty = labelbuffer+cellsize+cellsize*y
        r = Rectangle(Point(upperleftx,upperlefty), Point(lowerrightx,lowerrighty))
        r.setFill(paintcolor('backg',0))
        r.draw(win)
        pmapr[y][x] = 0

  
#records a hit on the computers map
def updatehit(x,y,cmapu):
    cmapu[y][x] = 0
                

#Used to copy a ship from cmapu to cmapr (from first map to the second map)
def update_map(map1, map2):
    for y in range(countvercells):
        for x in range(counthorcells):
            if map1[y][x] == 1:
                map2[y][x] = map1[y][x]

#this places all the users ships: listr is a list will all the ship sizes
def user_ship_input(listr, pmapr, pmapu, win):
    
    for n in listr:
	#structured_clicking handles the input of one ship and returns true after it has placed one
	#this while loop just keeps calling it until it is successful
        while structured_clicking(n, pmapr,pmapu,win) == False:
            pass

#gets shot, evaluates if its a hit, and draws it			
def user_shot(cmapu,cmapr, win):
    x,y = get_click(win)
    hit = checkforhit(x-xshift,y,cmapu)
    paintShot(x,y,hit,win,cmapr,0)
    return hit

###############################################################

##########                     MAIN
###############################################################

def main():
	#pmapr is player's map record: it will store where the player's ships 
	#were placed by putting a one whereever a ship is
    pmapr = arrayInit()
	#pmapu will record hits by changing 1 s to zeros. when pmapu is zero
	#all the players ships are sunk
    pmapu = arrayInit()
	    
    #cmapu - computer map updated- will be the updating map which tracks where ships are hit
    cmapu = arrayInit()
    #cmapr - computer map record- will be the map of the original placement
    cmapr = arrayInit()
    #map to record shots taken by computer
    cshotmap = arrayInit()
    #This will be the total number of shots fired over all games
	# if the computer is repeatedly calling itself
    runtotal = 0

	
    #from zelle's graphics module, creates a window for our game
    win = GraphWin("BattleShip", winhordim, winverdim)

    # this will be the window where the action happens
    drawboard(winhordim, winverdim, cellsize, totalhor, totalver, win)
	
	#   This is the number and size of ships the computer places 
    comp_ship_list = [4,4,5] 
    #This places the computer ships
    cmapr = placeships(comp_ship_list, win, cmapu, cmapr, runcount)
	
	
	#instructions
    start_text = Text(Point(winverdim-30, winhordim/2+10), "Click twice to place each of your three ships.")
    start_text.setSize(20)
    start_text.setStyle('bold')
    start_text.setFill("blue")
    start_text.draw(win)
	
    #This is the number and size of ships the user places
    listofuserships = [4,4,5]
	#this gets the players input on ship location
    user_ship_input(listofuserships, pmapr, pmapu, win)
	#instructions
    start_text = Text(Point(winverdim-10, winhordim/2+40), "Click on the right board to begin.")
    start_text.setSize(20)
    start_text.setStyle('bold')
    start_text.setFill("blue")
    start_text.draw(win)
	
	#waits for user to click before starting
    get_click(win)
    
    #When the sum of the array is zero, al ships are hit
    csumArray = sumCalc(cmapu)
    psumArray = sumCalc(pmapu)
    #Debugging
    #print("1SumCalc: ", sumCalc(cmapu))
    #Attempts is the number of shots fired for one game
    attempts = 0 #is this necessary? check later
    # THis loop runs until the ships are sunk
    while csumArray != 0 and psumArray != 0:  #while nobody has lost, it loops.
        user_shot(cmapu,cmapr, win) #Gets the users shot
        sleep(longpause)
        #the computer generates a random shot and records if it's a hit
        x,y,hit = randomShot(pmapu, cshotmap)
# THe color of the square changes if the computer shot there        
        cpaintShot(x,y,hit,win,pmapr, 0)
        #Update sumarray to see if all ships have been sunk
        csumArray = sumCalc(cmapu)
        psumArray = sumCalc(pmapu)
        if hit == True and psumArray and csumArray != 0:
			#once the computer records a hit, it next shots 
			#are calculated using the hunt function.  
            hunt(cmapu, cmapr, pmapu, pmapr, cshotmap,x,y, attempts,win, 0)
        
        
        attempts += 1
        sleep(shortpause)
    #Determines who won:
    if csumArray == 0:
        congrats = Text(Point(winverdim-10, winhordim/2), "Player wins.")
        congrats.setSize(30)
        congrats.setStyle('bold')
        congrats.setFill("red")
        congrats.draw(win)
        print("PLayer wins.")
    else:
        print("Computer wins.")
        
        congrats = Text(Point(winverdim-10, winhordim/2), "Computer wins.")
        congrats.setSize(30)
        congrats.setStyle('bold')
        congrats.setFill("red")
        congrats.draw(win)
    win.getMouse()
    win.close()





main()