import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import csv_manager
from ticktacktoe.board import Board

def start_whatsapp():

    options = Options()

    options.add_argument("--user-data-dir=C:\\Users\\mihir\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)

    PATH='C:\\Users\\mihir\\chrome driver\chromedriver.exe'
    driver=webdriver.Chrome(PATH, options=options)
    driver.maximize_window()

    driver.get('https://web.whatsapp.com')

    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "zoWT4"))
        )
    except:
        print('failed')
        driver.quit()
        return False
    time.sleep(0.25)

    return driver

def redirect_user_by_search(username, driver):
    text_box=driver.find_element_by_class_name('_13NKt')
    text_box.clear()
    text_box.send_keys(username)
    text_box.send_keys(Keys.ENTER)

def redirect_user(username, driver):
    text_box=driver.find_element_by_class_name('_13NKt')
    text_box.send_keys(username)
    text_box.clear()
    try:
        driver.find_element_by_xpath(f"//*[@title='{username}']").click()
    except:
        print('EROR: clicking failed, pressed enter')
        text_box.send_keys(Keys.ENTER)
        
def send_message(mssg, driver):
    text_box=driver.find_elements_by_class_name('_13NKt')[1]
    text_box.clear()
    text_box.send_keys(str(mssg))
    text_box.send_keys(Keys.ENTER)
    return len(driver.find_elements_by_class_name('_22Msk'))

def newLine(driver):
    action= ActionChains(driver)
    action.key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()

class contact_manager:
    
    def __init__(self, li) -> None:
        self.contact=li
    
    def add_contact(self, c):
        self.contact=self.contact+[c]
        csv_manager.set_contact(self.contact)
        
    def print_contacts(self):
        for i, c in enumerate(self.contact):
            print(f'[{i}] {c}')
    
    def get_contact(self, num):
        if num<0 or num>len(self.contact):
            return False
        if num==len(self.contact):
            mssg=input('contact name-> ')
            redirect_user_by_search(mssg, driver=driver)
            return 's'
        return self.contact[num]

    def ask_contact(self):
        while True:
            self.print_contacts()
            num=input('enter contact number -> ')
            if num=='-add':
                mssg=input('contact name-> ')
                contacts.add_contact(mssg)
                continue
            try:
                num=int(num)
            except:
                print('please only input valid numbers')
                continue
            userName=self.get_contact(num)
            if userName=='s':
                return False
            if userName!=False:
                return userName

def read_message(driver):
    for i in range(1, 11):
        messages=driver.find_elements_by_class_name('i0jNr')
        try:
            lastMessage=messages[-i].find_element_by_xpath(".//span").text
            break
        except:
            continue

    return(lastMessage)
    
def message_reader(driver, t):
    lastMessage=read_message(driver)
    # print(f'last mssg-> {lastMessage}')
    for i in range(t*2):
        newMessage=read_message(driver)
        if lastMessage!=newMessage:
            return newMessage
        time.sleep(0.5)
    return False

def initialize(driver):
    text_box=driver.find_elements_by_class_name('_13NKt')[1]
    def writeMessage(mssg):
        text_box.send_keys(str(mssg))
    def enter():
        text_box.send_keys(Keys.ENTER)
    writeMessage('Hi I am asc\'s whatsap bot. what can I do-')
    newLine(driver)
    writeMessage('1) start a game of tick tac toe with you and my creator')
    newLine(driver)
    writeMessage('please put a number of the index to make me do that')
    enter()

class ticktactoe:
    def __init__(self, driver) -> None:
        self.board=Board()
        self.driver=driver
        self.move='X'

    def printBoard(self):
        text_box=driver.find_elements_by_class_name('_13NKt')[1]
        def writeMessage(mssg):
            text_box.send_keys(str(mssg))
        def enter():
            text_box.send_keys(Keys.ENTER)
        li=self.board.pBoard()
        for i in li:
            writeMessage(i)
            newLine(self.driver)
        enter()
    
    def checkMove(self, position):
        output=self.board.check_move(position)
        if output=='True':
            return True
        else:
            send_message(output, driver=self.driver)
            return False
    
    def checkForWin(self):
        outcome=self.board.check_for_win(self.move)
    
    def inputMove(self, position):
        # if self.checkMove(position)!='True':
        #     return False
        self.board.input_move(int(position), self.move)
        self.checkForWin()
        if self.move=='X':
            self.move='O'
        else:
            self.move='X'
        
        self.printBoard()
        return True
    
def playtic(driver):
    game=ticktactoe(driver)
    game.printBoard()
    while game.board.game_state=='C':
        move=message_reader(driver=driver, t=10)
        if move!=False:
            output=game.checkMove(move)
            if output==True:
                game.inputMove(move)
        
    if game.board.game_state=='X':
        send_message('player X wins!!', driver=driver)
    elif game.board.game_state=='O':
        send_message('player O wins!!', driver=driver)
    else:
        send_message('Draw!!', driver=driver)
    # game.board.reset_board()

    
driver=start_whatsapp()
contacts=contact_manager(csv_manager.get_contact())

while True:
    userName=contacts.ask_contact()
    if userName!=False:
        redirect_user(userName, driver=driver)
    leave=False
    while True:
        mssg=input(f'messge to {userName}->')
        if mssg=='S':
            break
        elif mssg=='lr':
            print(read_message(driver=driver))
        elif mssg=='r':
            print(f'new mssg-> {message_reader(driver=driver, t=10)}')
        elif mssg=='ini':
            initialize(driver=driver)
            for i in range(10):
                outcome=message_reader(driver=driver, t=20)
                if outcome!=False:
                    try:
                        outcome=int(outcome)
                    except:
                        continue
                    if outcome==1:
                        playtic(driver=driver)
                        break
        elif mssg=='esc':
            break
        elif mssg=='esc f':
            leave=True
            break

        else:
            send_message(mssg, driver)

    if leave:
        break
    
time.sleep(5)
driver.quit()

