from time import sleep
from random import uniform
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from clarifai.client import ClarifaiApi
from image_aux import ImageAux


def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def wait_between(a, b):
    rand = uniform(a, b)
    sleep(rand)

url = "http://blogs.ne10.uol.com.br/jamildo/2016/01/25/enquete-pedro-eurico-deve-continuar-a-" \
      "ocupar-o-cargo-de-secretario-de-justica/"


while True:
    driver = webdriver.Firefox()
    driver.get(url)

    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element_by_xpath("//iframe[contains(@src,'enquete')]"))
    driver.switch_to.frame(driver.find_element_by_xpath("//iframe[contains(@title,'widget')]"))

    wait_between(0.2, 0.5)

    checkbox = driver.find_element_by_xpath("//*[@id='recaptcha-anchor']")
    checkbox.click()

    wait_between(1.0, 1.5)

    if check_exists_by_xpath('//span[@aria-checked="true"]'):
        print('\n\r reCaptcha is solved!')
    else:
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element_by_xpath("//iframe[contains(@src,'enquete')]"))
        driver.switch_to.frame(driver.find_element_by_xpath("//iframe[contains(@title,'challenge')]"))

        text_tag = driver.find_element_by_xpath("//div[contains(@class,'rc-imageselect-desc-no-canonical')]")
        sentence_tag = text_tag.find_element_by_tag_name("strong")
        sentence_text = sentence_tag.text
        sentence = sentence_text.split()

        image_tag = driver.find_element_by_xpath("//img[contains(@class,'rc-image')]")
        image_url = image_tag.get_attribute('src')

        image_aux = ImageAux(image_url)
        image_aux.generate_images()

        api = ClarifaiApi('TXB6MB-evkMHppAyFrgw_qas3-_YKPGvels7bTP1', 'F32nfZQ3QEKnPi6vdKUj8k_bViz29L6thxNuv9P2')

        tiles = driver.find_element_by_id("rc-imageselect-target")
        table = tiles.find_element_by_tag_name("table")
        tds = table.find_elements_by_tag_name("td")

        for idx, td in enumerate(tds):
            response = api.tag_images(image_aux.get_image(idx+1))
            results = response['results'][0]['result']['tag']['classes']
            for word in sentence:
                if word in results:
                    td.find_element_by_class_name("rc-image-tile-target").click()
                    break

        driver.find_element_by_id("recaptcha-verify-button").click()

        wait_between(1.0, 1.5)

        if check_exists_by_xpath('//span[@aria-checked="true"]'):
            print('\n\r reCaptcha is solved! :) ')
        else:
            print('\n\r Maybe in next time :/ ')

        driver.close()
