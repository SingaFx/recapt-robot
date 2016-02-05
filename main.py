import re, csv
from time import sleep, time
from random import uniform, randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException    

def write_stat(loops, time):
	with open('stat.csv', 'a', newline='') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
		spamwriter.writerow([loops, time])  	 
	
def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True 
	
def wait_between(a,b):
	rand=uniform(a, b) 
	sleep(rand)

def get_captcha_frames(source): 	 
	r = re.compile('(?<=\<iframe).*?\sname="(I[\d_]+)"')
	return r.findall(source) 
	
# main procedure to randomly check and submit picture solution	
def solve_images(driver):
	wait_between(0.2, 0.5)	
	WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID ,"rc-imageselect-target"))) 		
	rand1 =	randint(1,9)
	# ******** check if there are clicked tiles ********
	if check_exists_by_xpath('//div[@id="rc-imageselect-target"]/div[@class="rc-imageselect-tileselected"]'): 
	    # there are checked tiles 
		rand2=''
	else:            
	    # there are NO checked tiles 		
		rand2 = randint(1,9) 
		while rand2==rand1: # we get rand2 different from rand1
			rand2 = randint(1,9)		
	wait_between(0.3, 0.8)		 
	# ********* clicking on a tile(s) ********** 
	tile1 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH ,   '//div[@id="rc-imageselect-target"]/div[{}]'.format(rand1)) )  
        )
	tile1.click()	
	# second tile click
	if (rand2):  
		driver.find_element_by_xpath('//div[@id="rc-imageselect-target"]/div[{}]'.format(rand2)).click()
 	# ********** clicking submit buttion **********
	driver.find_element_by_id("recaptcha-verify-button").click()
	
start = time()	 
url='http://blogs.ne10.uol.com.br/jamildo/2016/01/25/enquete-pedro-eurico-deve-continuar-a-ocupar-o-cargo-de-secretario-de-justica/'
driver = webdriver.Firefox()
driver.get(url)
mainWin = driver.current_window_handle
frameName1 = get_captcha_frames(driver.page_source)[0]
# *****  move to the main captcha frame *****
driver.switch_to_frame(frameName1)
wait_between(0.2, 0.5) 
# **** locate and click checkBox on main captcha frame ******
CheckBox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID ,"recaptcha-anchor"))) 
CheckBox.click() 
# *********  back to main window  *************
driver.switch_to.window(mainWin)    
wait_between(1.0, 1.5) 
# ********** fetch second iframe name **********
frameName2 = get_captcha_frames(driver.page_source)[-1] 

for i in range(1,100): 
	# check if checkbox is checked (reCaptcha solved)	
	WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID , frameName1)))   
	if check_exists_by_xpath('//span[@aria-checked="true"]'):
		timespan=round(time()-start) 
		print ('\n\r reCaptcha is solved at loop {0} for {1} seconds !'.format(i, timespan))
		import winsound
		winsound.Beep(400,1500)
		write_stat(i, timespan) # saving results into stat file
		break 		
	# move to the 2nd frame thru main window	
	driver.switch_to.window(mainWin)   
	WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID , frameName2)))  	
	# main procedure - picture puzzle check
	solve_images(driver)	
	# back to the main window
	driver.switch_to.window(mainWin)  	