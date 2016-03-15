from time import sleep
from random import uniform
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from clarifai.client import ClarifaiApi
from image_helper import ImageHelper
import inflect
import json


def check_exists_by_name(web_driver, classname):
    try:
        web_driver.find_element_by_class_name(classname)
    except NoSuchElementException:
        return False
    return True


def check_if_is_solved(web_driver):

    web_driver.switch_to.default_content()
    web_driver.switch_to.frame(driver.find_element_by_xpath("//iframe[contains(@src,'enquete')]"))
    driver.switch_to.frame(driver.find_element_by_xpath("//iframe[contains(@title,'widget')]"))

    try:
        check_box = driver.find_element_by_id("recaptcha-anchor")
        has_checked = check_box.get_attribute('aria-checked')
        if has_checked == 'true':
            return True
        else:
            return False
    except NoSuchElementException:
        return False


def wait_between(a, b):
    rand = uniform(a, b)
    sleep(rand)


def vote(web_driver):
    web_driver.switch_to.default_content()
    web_driver.switch_to.frame(driver.find_element_by_xpath("//iframe[contains(@src,'enquete')]"))
    btn_vote = driver.find_element_by_id("votar")
    btn_vote.click()


p = inflect.engine()
config = json.load(open('config.json'))['data']

url = config['target_url']
clarifai_client_language = config['clarifai_settings']['language']
clarifai_client_settings = config['clarifai_settings']['applications'][0]

while True:

    profile = webdriver.FirefoxProfile()
    profile.set_preference("intl.accept_languages", "en")
    driver = webdriver.Firefox(firefox_profile=profile)
    driver.get(url)

    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element_by_xpath("//iframe[contains(@src,'enquete')]"))

    option = driver.find_element_by_xpath("//input[contains(@value,'66')]")
    option.click()

    driver.switch_to.frame(driver.find_element_by_xpath("//iframe[contains(@title,'widget')]"))

    wait_between(0.2, 0.5)

    checkbox = driver.find_element_by_xpath("//*[@id='recaptcha-anchor']")
    checkbox.click()

    wait_between(1.0, 2.0)

    if check_if_is_solved(driver):
        print('\n\r reCaptcha is solved!')
    else:

        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element_by_xpath("//iframe[contains(@src,'enquete')]"))
        driver.switch_to.frame(driver.find_element_by_xpath("//iframe[contains(@title,'challenge')]"))

        if check_exists_by_name(driver, "rc-imageselect-desc-no-canonical"):

            text_tag = driver.find_element_by_class_name("rc-imageselect-desc-no-canonical")
            sentence_tag = text_tag.find_element_by_tag_name("strong")
            sentence_text = sentence_tag.text
            sentence = sentence_text.split()

            image_tag = driver.find_element_by_xpath("//img[contains(@class,'rc-image')]")
            image_url = image_tag.get_attribute('src')

            image_aux = ImageHelper(image_url)
            image_aux.generate_images()

            api = ClarifaiApi(app_id=clarifai_client_settings['id'],
                              app_secret=clarifai_client_settings['secret'],
                              language=clarifai_client_language)

            tiles = driver.find_element_by_id("rc-imageselect-target")
            table = tiles.find_element_by_tag_name("table")
            tds = table.find_elements_by_tag_name("td")

            if len(tds) == 9:  # prevent error when recaptcha put more than 9 pics
                for idx, td in enumerate(tds):
                    response = api.tag_images(image_aux.get_image(idx+1))
                    results = response['results'][0]['result']['tag']['classes']

                    plurals = []
                    for result in results:
                        plurals.append(p.plural(result))
                    results.extend(plurals)

                    for word in sentence:
                        if word in results:
                            td.find_element_by_class_name("rc-image-tile-target").click()
                            break

                driver.find_element_by_id("recaptcha-verify-button").click()

        wait_between(1.0, 1.5)

        if check_if_is_solved(driver):
            print('\n\r reCaptcha is solved! :) ')
            vote(driver)
        else:
            print('\n\r Maybe in next time :/ ')

        wait_between(1.0, 1.5)

        driver.close()
