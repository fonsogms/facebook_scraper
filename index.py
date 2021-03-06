###  here we setup everything regarding the chrome driver and the bot navigator
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
###
import time
## to download the images
import urllib.request
## for easier scraping
import bs4

username=input("Introduce your username:  ")
password=input("Introduce your password:  ")

## we set the chrome options to avoid notifications
chrome_options = webdriver.ChromeOptions()

prefs = {"profile.default_content_setting_values.notifications" : 2}

chrome_options.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
driver.get("https://facebook.com")
def check_Loaded(search,waiting):
    element=driver.find_elements_by_css_selector(search)
    i=0
    while True:
        element=driver.find_elements_by_css_selector(search)
        i=i+1

        if len(element)>0 or i>waiting:
            print("logged in!")
            break

def login():
    check_Loaded("#email",1000)
    email_input=driver.find_element_by_css_selector("#email")
    pass_input=driver.find_element_by_css_selector("#pass")
    login_button=driver.find_element_by_css_selector("#u_0_b")
    email_input.send_keys(username)
    pass_input.send_keys(password)
    time.sleep(2)
    login_button.click()
def get_to_photos_page():
    time.sleep(3)
    profile=driver.find_element_by_css_selector("._1k67._cy7")
    profile.click()
    time.sleep(2)
    tab_links=driver.find_elements_by_css_selector("._6-6")
    tab_links[3].click()
    time.sleep(3)
    driver.execute_script(f"window.scrollTo(0, 1000)") 
    time.sleep(3)

def scroll_down(previous_len,scroll_y):
    time.sleep(2)
    loaded_pics=driver.find_elements_by_css_selector(".uiMediaThumb")
    print(previous_len,len(loaded_pics))
    if len(loaded_pics)==previous_len:
        return loaded_pics
    else:
        driver.execute_script(f"window.scrollTo(0, {scroll_y+3000})") 
        scroll_down(len(loaded_pics),scroll_y+3000)



def download_picture(pic,index,errors):
        driver.get(pic["href"])
        time.sleep(0.5)
        check_Loaded(".spotlight",1000)
        html=driver.page_source
        soup=bs4.BeautifulSoup(html,'html.parser')
        image=soup.select(".spotlight")
        url=image[0]["src"]
        urllib.request.urlretrieve(url,f"./pictures/{index}.jpg")
   
def get_pictures_link():
    html=driver.page_source
    soup=bs4.BeautifulSoup(html,'html.parser')
    pictures=soup.select(".uiMediaThumb") 
    return pictures
    
    
login()

get_to_photos_page()

driver.execute_script(f"window.scrollTo(0, 1000)") 

scroll_down(0,0)
pictures=get_pictures_link()

    
index=0
errors=0
for pic in pictures:
    try:
        download_picture(pic,index,errors)
        index+=1

    except:
        errors+=1
        print("errors",errors)
        
