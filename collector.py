from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import os

mdr = 'aternosfiles/' #Main directory, all files will be stored in
currdir = '' #DO NOT CHANGE
currfile = '' #DO NOT CHANGE
sleeptime = 10  # Change this according to your inernet speed. 2-3 for fast, 5-7 for slow, 9-10 for very slow (1 mb/s)
mail = 'yourmail@gmail.com'
password = 'yourpassword'


driver = webdriver.Chrome()  #Open chrome browser. Change this if you want a different browser
driver.get('https://aternos.org/server')

driver.find_element_by_partial_link_text('Sign in with Google').click() 
driver.find_element_by_name('identifier').send_keys(mail) #it types your mail
driver.find_element_by_id('identifierNext').click() 
time.sleep(sleeptime)
driver.find_element_by_name('password').send_keys(yourpassword)#it types your password
driver.find_element_by_id('passwordNext').click()
time.sleep(sleeptime)
driver.get('https://aternos.org/files/')
time.sleep(sleeptime)

mainfiles=driver.find_elements_by_class_name('filename')
def getfiles(files):
    global currdir
    for file in files:
        filename = file[1]
        filelink = file[0]
        print('file: ' + filename)
        currfile = filename
        try:
            driver.get('view-source:'+filelink)
            time.sleep(sleeptime)#3)
            filesrclines = driver.find_elements_by_class_name('line-content')
            filesrchtml = ''
            for ltr in filesrclines:
                    filesrchtml += ltr.text+'\n'
            soup = BeautifulSoup(filesrchtml, 'html.parser')
            try:
                yml = soup.find("div", {"id": "editor"}).get_text()
            except AttributeError:
                yml = ""
                print("file: "+filename+" dir: "+mdr+currdir+"Was not able to be copied")
            except:
                yml = ""
                print("file: "+filename+" dir: "+mdr+currdir+"Was not able to be copied")
            with open(mdr+currdir+currfile, 'w') as dcm:
                dcm.write(yml)
                dcm.close()
            print("file done: "+filename)
        except:
            print( "Error occured for file: " + filename+", dir: "+mdr+currdir)
    
def getfolders(foldername, link, maindir):
    #currdir += foldername +'/'
    global currdir
    try:
        os.makedirs(mdr+currdir)
    except FileExistsError:
        print("got fileexistserror for: "+mdr+currdir)
    driver.get(link)
    time.sleep(sleeptime)
    dirall = driver.find_elements_by_class_name('file')
    dirfiles = []
    dirfolders = []
    for dr in dirall:
        if dr.find_element_by_tag_name('i').get_attribute('class') == 'fas fa-file-alt' and dr.find_element_by_tag_name('a'):
            dirfiles.append([dr.find_element_by_tag_name('a').get_attribute('href'), dr.find_element_by_tag_name('a').text])  #format: link, filename
        elif dr.find_element_by_tag_name('i').get_attribute('class') == 'fas fa-folder' and dr.find_element_by_tag_name('a'):
            dirfolders.append([dr.find_element_by_tag_name('a').get_attribute('href'), dr.find_element_by_tag_name('a').text])
        else:
            print("unknown file or folder in dir: "+currdir)
            print("The file is probably not downloadable")
    getfiles(dirfiles)
    for folder in dirfolders:
        currdir += folder[1] +'/'
        print("Downloading folder: "+currdir)
        getfolders(folder[1], folder[0], currdir)
        currdir = maindir

folderlinks = []
for x in mainfiles:
    if x.get_attribute('href'):
        folderlinks.append([x.get_attribute('href'), x.text])
folderlinks = folderlinks[5:]
for folderlink in folderlinks:
    currdir = folderlink[1]+'/'
    print("PLugin: " + currdir)
    getfolders(folderlink[1], folderlink[0], currdir)
