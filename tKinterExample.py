from tkinter import *
from tkinter import messagebox
#python game with MinMax AI
#made by Arturs Stipnieks (turbo7021)
class snakeWalnut(): # the snake filled walnut tree by turbo7021 
    def __init__(self): # initialize tree
        self.valueList = []     # when building, the current level being built
        self.oldValues = []     # the whole tree 
        self.isMaxLevel = False # when building, whether the level built is max or min
        self.minValue = 0       # lowest value in current level being built, to check if the tree is finished
        self.nodeCount = -1     # when building, current element number
        self.possibleNext = [0] # possible next turns
        self.humanStart = True  # whether man or computer begins
        self.addValue(self.count(), [0, 0, 0], None, 0) # makes root node

        self.turnOneValue = 2   # CHANGE THIS FOR FIRST TURN VALUE
        self.turnTwoValue = 3   # CHANGE THIS FOR SECOND TURN VALUE

    def treeAdd1H(self, value, data): # adds tree element where human puts small value
        if (data[1] + self.turnOneValue) <= 10:
            valueData = [data[0] + self.turnOneValue, data[1] + self.turnOneValue, data[2]]
            self.treeAdd(value, valueData, self.count(), self.turnOneValue)
        else:
            return


    def treeAdd2H(self, value, data): # adds tree element where human puts big value
        if (data[1] + self.turnTwoValue) <= 10:
            valueData = [data[0] + self.turnTwoValue, data[1] + self.turnTwoValue, data[2]]
            self.treeAdd(value, valueData, self.count(), self.turnTwoValue)
        else:
            return


    def treeAdd1C(self, value, data): # adds tree element where computer puts small value
        if (data[1] + self.turnOneValue) <= 10:
            valueData = [data[0], data[1] + self.turnOneValue, data[2] + self.turnOneValue]
            self.treeAdd(value, valueData, self.count(), self.turnOneValue)
        else:
            return


    def treeAdd2C(self, value, data): # adds tree element where computer puts big value
        if (data[1] + self.turnTwoValue) <= 10:
            valueData = [data[0], data[1] + self.turnTwoValue, data[2] + self.turnTwoValue]
            self.treeAdd(value, valueData, self.count(), self.turnTwoValue)
        else:
            return


    def treeAdd(self, value, data, count, addValue): # add the element
        self.addValue(count, data, value, addValue)

        
    def addValue(self, value, data, parent, addValue): # add new element
        self.valueList.append([value, data, 0, parent, [], self.isMaxLevel, addValue])
        self.checkMin(data[1])
        self.addChild(parent, value)

    def addData(self): # add a new level to the tree
        level = self.isMaxLevel
        items = self.printValues()
        self.minValue = 10
        if self.isMaxLevel:
            for item in items:
                self.treeAdd1H(item[0], item[1])
                self.treeAdd2H(item[0], item[1])
        else:
            for item in items:
                self.treeAdd1C(item[0], item[1])
                self.treeAdd2C(item[0], item[1])

    def printValues(self): # nodes of previous level which need following nodes
        self.oldValues.append(self.valueList)
        self.isMaxLevel = not self.isMaxLevel
        values = []
        for item in self.valueList:
            values.append(item)
        self.valueList = []
        return values

    def checkMin(self, data): # checks if the value is the lovest value in the level
        if data < self.minValue:
            self.minValue = data

    def buildLoop(self): # tree building level by level
        while (self.minValue < 9):
            self.addData()

    def printAllValues(self): # return the tree for debugging purpouses
        print(self.oldValues)
        print(self.valueList)

    def addChild(self, parent, value): # add child to a node
        
        for item in reversed(self.oldValues):
            for nodeItem in item:
                if nodeItem[0] == parent:
                    nodeItem[4].append(value)

    def updateValue(self): # add the MinMax values 
        self.oldValues.append(self.valueList)
        for item in reversed(self.oldValues):
            for nodeItem in item:
                if nodeItem[4] == []:
                    if nodeItem[1][0] > nodeItem[1][2]:
                        nodeItem[2] = 1
                    if nodeItem[1][0] < nodeItem[1][2]:
                        nodeItem[2] = -1

        for item in reversed(self.oldValues):
            for nodeItem in item:
                if not nodeItem[4] == []:
                    nodeItem[2] = (self.getRate(nodeItem[0], nodeItem[5]))
        self.printAllValues()

    def getRate(self, parent, level): # calculates the value of the node
        values = self.getChildrenData(parent)
        if level:
            return min(values)
        else:
            return max(values)

    def getChildrenData(self, value): # returns the children values of a node
        values = []
        for item in reversed(self.oldValues):
            for nodeItem in item:
                if nodeItem[3] == value:
                    values.append(nodeItem[2])
        if values != []:
            return values
        else:
            for item in reversed(self.oldValues):
                for nodeItem in item:
                    if nodeItem[0] == value:
                        values.append(nodeItem[2])
            return values

    def getChildrenValue(self, value): # returns the childrens children of a node
        values = []
        for item in reversed(self.oldValues):
            for nodeItem in item:
                if nodeItem[3] == value:
                    values.append(nodeItem[4])
        return values

    def computerDecide(self): # computer turn
        turns = []
        print("possible nodes ", self.possibleNext)
        if len(self.possibleNext) == 1:
            for item in self.oldValues:
                for nodeItem in item:
                    if nodeItem[0] == self.possibleNext[0]:
                        return nodeItem[6]
        else:
            for item in self.oldValues:
                for nodeItem in item:
                    if nodeItem[0] == self.possibleNext[0] or nodeItem[0] == self.possibleNext[1]:
                        turns.append(nodeItem)
            print(turns)
            if self.isLarger(turns[0][2], turns[1][2]):
                return turns[0][6]
            elif self.isSmaller(turns[0][2], turns[1][2]):
                return turns[1][6]
            else:
                if turns[0][4] == [] and turns[1][4] == []:
                    return turns[0][6]
                elif self.childrenTrace(turns[0][4], turns[1][4]):
                    return turns[0][6]
                else:
                    return turns[1][6]

    def childrenTrace(self, turns1, turns2): # returns best next turn
        turns = []
        nodes = []
        turns.append(turns1)
        turns.append(turns2)
        for item in turns:
            for nodeItem in item:
                nodes.append([nodeItem, self.getChildrenData(nodeItem)[0]])
        value = [-1, -2]
        if (nodes[0][0] == nodes[2][0] and [1][0] == nodes[3][0]) or (nodes[0][0] == nodes[3][0] and [1][0] == nodes[2][0]):
            if self.isLarger(self.childrenTrace(self.getChildrenValue(nodes[0][0], nodes[1][0])), self.childrenTrace(self.getChildrenValue(nodes[2][0], nodes[3][0]))):
                return True
        for item in nodes:
            if self.isSmaller(item[1], value[1]):
                value = item
        print(value)
        i = 0
        for item in nodes:
            if nodes[i][0] != value[0]:
                i+=1
        if i<=1:
            return True
    def isLarger(self, value1, value2): # highest value in context of starting player
        if value1 == value2:
            return False
        if not self.humanStart:
            if value1>value2:
                return True
            else:
                return False
        else:
            if value1>value2:
                return False
            else:
                return True
    def isSmaller(self, value1, value2):# lowest value in context of starting player
        if value1 == value2:
            return False
        if not self.humanStart:
            if value1<value2:
                return True
            else:
                return False
        else:
            if value1<value2:
                return False
            else:
                return True
        
    def setPossibleNext(self, value): # refresh the possible following turns
        print("setting next")
        nextNode = 0
        if value == 2:
            nextNode = self.possibleNext[0]
        else:
            nextNode = self.possibleNext[1]
        for item in self.oldValues:
            for nodeItem in item:
                if nodeItem[0] == nextNode:
                    self.possibleNext = nodeItem[4]
                    print("decided possible ", str(nodeItem))
                    print("decided possible next now", self.possibleNext)
    def count(self): # node counter
        self.nodeCount += 1
        return self.nodeCount

    def countTest(self): # return the number of previous ndoe
        return self.nodeCount

    def resetPlayer(self): # restarts game and human starts
        self.possibleNext = [1, 2]
        self.humanStart = True
        
    def resetComputer(self): # restarts game and computer starts
        self.possibleNext = [1, 2]
        self.humanStart = False


class score: # object that holds score of a match
    def __init__(self):  # initialize result object
        self.human = 0
        self.computer = 0
        self.total = 0

    def hAdd(self, value): # increase human score
        self.human += value
        self.total += value

    def cAdd(self, value): # increase computer score
        self.computer += value
        self.total += value

    def resultH(self): # returns human score
        return self.human

    def resultC(self): # returns computer score
        return self.computer

    def resultT(self): # returns total score
        return self.total

    def reset(self): # resets score
        self.human = 0
        self.computer = 0
        self.total = 0
# this is where the non snakeWalnut code begins




def choosePlayer(): # dialog to choose the player
    resultobj.reset()
    updateScore()
    if messagebox.askyesno("Begin game", "Does human begin?"):
        sLbl.configure(text="<<<")
        nodeTreeObj.resetPlayer()
        btn2.config(state=NORMAL)
        btn3.config(state=NORMAL)
    else:
        nodeTreeObj.resetComputer()
        btn2.config(state=DISABLED)
        btn3.config(state=DISABLED)
        datorsTurn()



def finish(): # game finished
    winnerMessage = ""
    if resultobj.resultH() > resultobj.resultC():
        winnerMessage = "Human wins"
    elif resultobj.resultC() > resultobj.resultH():
        winnerMessage = "Computer wins"
    else:
        winnerMessage = "Draw"
    winnerMessage += ", play again?"
    print("========", winnerMessage, "========")
    if messagebox.askyesno("Game finished", winnerMessage):
        updateScoreFinal()
        resultobj.reset()
        choosePlayer()
    else:
        on_closing()


def humanTurn(value): # human adds the chosen amount
    resultobj.hAdd(value)
    nodeTreeObj.setPossibleNext(value)
    print("====human added ", value, " ====")
    if updateScore():
        return
    datorsTurn()


def datorsAdd(): # computer adds the chosen amount
    value = nodeTreeObj.computerDecide()
    resultobj.cAdd(value)
    nodeTreeObj.setPossibleNext(value)
    print("====computer added ", value, " ====")

def datorsTurn(): # stops human game, does computer turn
    sLbl.configure(text=">>>")
    btn2.config(state=DISABLED)
    btn3.config(state=DISABLED)
    datorsAdd()
    if updateScore():
        return
    if resultobj.resultT() + 2 <= 10: btn2.config(state=NORMAL)
    if resultobj.resultT() + 3 <= 10: btn3.config(state=NORMAL)
    sLbl.configure(text="<<<")


def updateScore(): # refreshes the gui score, checks if game is finished
    updateScoreFinal()
    if resultobj.resultT() + 2 > 10:
        finish()
        return True
    else:
        return False

def updateScoreFinal(): # refreshes the gui score
    cLb2.configure(text=str(resultobj.resultH()))
    dLb2.configure(text=str(resultobj.resultC()))
    totalScore.configure(text=str(resultobj.resultT()))

def on_closing(): # game finished
    resultobj.reset()
    updateScore()
    messagebox.showinfo(title="Exit",
                        message="Thank you for playing.")
    window.quit()
    window.destroy()

resultobj = score()

nodeTreeObj = snakeWalnut() 
nodeTreeObj.buildLoop() 
nodeTreeObj.updateValue()

window = Tk()
window.title("Game")
window.geometry('200x200')
cLbl = Label(window, text="Human")
cLbl.grid(column=0, row=0)
sLbl = Label(window, text="")
sLbl.grid(column=1, row=0, rowspan=2)
dLbl = Label(window, text="Computer")
dLbl.grid(column=2, row=0)
btn2 = Button(window, text="+2", command=lambda: humanTurn(2))
btn2.grid(column=0, row=2)
btn3 = Button(window, text="+3", command=lambda: humanTurn(3))
btn3.grid(column=2, row=2)
cLb2 = Label(window, text="0")
cLb2.grid(column=0, row=1)
dLb2 = Label(window, text="0")
dLb2.grid(column=2, row=1)
totalScore = Label(window, text="0")
totalScore.grid(column=1, row=2)
window.protocol("WM_DELETE_WINDOW", on_closing)
choosePlayer()
window.mainloop()
