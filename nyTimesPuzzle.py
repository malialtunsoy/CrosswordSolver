from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class Connector:
    def __init__(self, PATH):
        self.cluesAcross = []
        self.cluesDown = []
        self.PATH = PATH
        self.cellNumberArray = []
        self.cellBlockArray = []
        self.cellAnswerArray = []

    def connectToPuzzle(self):
        separtor = "============================\n"
        print(separtor , "CONNECTING TO THE WEBSITE\n"+ separtor)
        driver = webdriver.Chrome(self.PATH)
        driver.get("https://www.nytimes.com/crosswords/game/mini")

        """
        Skip first web message
        """
        time.sleep(1)
        okButton  = driver.find_element_by_xpath("//*[@id=\"root\"]/div/div/div[4]/div/main/div[2]/div/div[2]/div[3]/div/article/div[2]/button")
        driver.execute_script("arguments[0].click();", okButton)
        

        """
        REVEAL ANSWERS
        """
        revealButton = driver.find_element_by_xpath("//*[@id=\"root\"]/div/div/div[4]/div/main/div[2]/div/div/ul/div[2]/li[2]/button")
        driver.execute_script("arguments[0].click();", revealButton)
        #revealButton.click()

        revealPuzzleButton = driver.find_element_by_xpath("//*[@id=\"root\"]/div/div/div[4]/div/main/div[2]/div/div[1]/ul/div[2]/li[2]/ul/li[3]/a")
        driver.execute_script("arguments[0].click();", revealPuzzleButton)
        #revealPuzzleButton.click()

        yesIAmSureButton  = driver.find_element_by_xpath("//*[@id=\"root\"]/div/div[2]/div[2]/article/div[2]/button[2]")
        driver.execute_script("arguments[0].click();", yesIAmSureButton)

        closePopUp  = driver.find_element_by_xpath("//*[@id=\"root\"]/div/div[2]/div[2]/span")
        driver.execute_script("arguments[0].click();", closePopUp)

        """
        Get clue and cell data
        """
        print(separtor , "RECEIVING CLUES\n"+ separtor)
        clue = driver.find_element_by_class_name("Layout-clueLists--10_Xl")
        childs = clue.find_elements_by_class_name("Clue-li--1JoPu")
        cells = driver.find_elements_by_tag_name("g")

        """
        Manage Clues
        """
        for i in range(0,5):
            clueNum = childs[i].find_elements_by_css_selector("*")[0].text
            clueText = childs[i].find_elements_by_css_selector("*")[1].text
            self.cluesAcross.append([clueNum, clueText])
        for i in range(5,10):
            clueNum = childs[i].find_elements_by_css_selector("*")[0].text
            clueText = childs[i].find_elements_by_css_selector("*")[1].text
            self.cluesDown.append([clueNum, clueText])

        """
        Print clues
        """
        print("***ACROSS CLUES***")
        for i in self.cluesAcross:
            print(i)
        print("\n***DOWN CLUES***")
        for i in self.cluesDown:
            print(i)

        """
        Manage Grid Cells
        """
        print(separtor , "RECEIVING CELL DATA\n"+ separtor)
        #print("G size: ", len(cells))

        tempNumber = []
        tempBlock = []
        tempAnswer = []

        for g in range(0,25):
            if g%5 == 0:
                tempNumber = []
                tempBlock = []
                tempAnswer = []
            #print(g+1, cells[g+4].text)
            cellMiniNumber = ""
            cellAnswer = ""

            cellText = cells[g+4].text
            for s in cellText:
                if s.isdigit():
                    cellMiniNumber = s
                if s.isupper():
                    cellAnswer = s

            className = cells[g+4].find_elements_by_css_selector("rect")[0].get_attribute("class")
            if "block" in className:
                className = "1"
            else:
                className = "0"

            if cellMiniNumber == '':
                cellMiniNumber = "-"
            if cellAnswer == '':
                cellAnswer = "-"
            
            tempNumber.append(cellMiniNumber)
            tempBlock.append(className)
            tempAnswer.append(cellAnswer)
            if g%5 == 4:
                self.cellNumberArray.append(tempNumber)
                self.cellBlockArray.append(tempBlock)
                self.cellAnswerArray.append(tempAnswer)

        """
        Print Cell Data
        """
        print("*** CELL INDEX NUMBERS ***")
        for r in self.cellNumberArray:
            print(r)
        print("\n*** BLOCK CELL MAP ***")
        for r in self.cellBlockArray:
            print(r)
        print("\n*** CELLS WITH SOLUTIONS ***")
        for r in self.cellAnswerArray:
            print(r)

        """
        Quit browser
        """
        print(separtor , "CLOSING THE BROWSER\n"+ separtor)
        driver.quit()


    def print_clues(self):
        """
        Print Clues
        """
        print("Across Clues")
        for clue in self.cluesAcross:
            print(clue)

        print("Down Clues")
        for clue in self.cluesDown:
            print(clue)

    def print_grid_cells(self):
        """
        Print Grid Cells
        """
        print("\nGrid Number")
        for row in self.cellNumberArray:
            print(row)
        print("Grid Blocks")
        for row in self.cellBlockArray:
            print(row)
        print("Grid Answer")
        for row in self.cellAnswerArray:
            print(row)


