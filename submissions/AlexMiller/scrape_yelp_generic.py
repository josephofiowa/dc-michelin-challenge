from selenium import webdriver
import json
import pdb
from optparse import OptionParser
import pandas as pd

parser = OptionParser()
parser.add_option("-o", "--output", dest="output", default="D:\\Documents\\Data\\Yelp\\NYC",
                        help="Output path. Default is wd",metavar="FOLDER")
(options, args) = parser.parse_args()


def input_text(browser, inputs, useID):
    # Fills a list of text boxes
    #
    # inputs: [{"input_id": "someId", "input_str": "some string"}, ... ]

    # This will cause Selenium to wait until the element is found.
    if useID:
        browser.find_element_by_xpath('//*[@id="{}"]'.format(inputs[0]["input_id"]))
        # browser.find_element_by_id(inputs[0]["input_id"]) 
    
        # Selenium is very slow at traversing the DOM. 
        # To quickly input text in many boxes, we inject a 
        # javacript function into the iframe. The collection
        # of textbox ids and strings is serialized 
        # as a Javascript object literal using the json module.
        inputs= json.dumps(inputs)
        js = "var inputs = {};".format(inputs)
        js += """
        console.log(inputs)
        for (var k = 0; k < inputs.length; k++) {
            var inputStr = inputs[k]["input_str"];
            var input = document.getElementById(inputs[k]["input_id"]);
            input.value = inputStr;
        }
        return true;"""
        browser.execute_script(js)
    else:
        #use name
        browser.find_element_by_xpath('//*[@name="{}"]'.format(inputs[0]["input_id"]))
        # browser.find_element_by_id(inputs[0]["input_id"]) 
    
        # Selenium is very slow at traversing the DOM. 
        # To quickly input text in many boxes, we inject a 
        # javacript function into the iframe. The collection
        # of textbox ids and strings is serialized 
        # as a Javascript object literal using the json module.
        inputs= json.dumps(inputs)
        js = "var inputs = {};".format(inputs)
        js += """
        console.log(inputs)
        for (var k = 0; k < inputs.length; k++) {
            var inputStr = inputs[k]["input_str"];
            var input = document.getElementsByName(inputs[k]["input_id"]);
            input[0].value = inputStr;
        }
        return true;"""
        browser.execute_script(js)
browser = webdriver.Chrome("C://chromedriver//chromedriver") # Create a session of Chrome
browser.implicitly_wait(30) # Configure the WebDriver to wait up to 30 seconds for each page to load

browser.get("https://www.yelp.com/") # Load page
location = {} # Set up our location input
location["input_id"] = "find_loc"
location["input_str"] = "New York, NY"
input_text(browser, [location], False) # Input the text using name search
browser.find_element_by_xpath('//*[@id="header-search-submit"]').click() # Hit search button to get us in the right locale
name = {} # Set up our name input
name["input_id"] = "find_desc"
name["input_str"] = "Chef's Table at Brooklyn Fare"
input_text(browser, [name], False) # Input the text using name
browser.find_element_by_xpath('//*[@id="header-search-submit"]').click() # Hit search button to find the restaurant
firstSpan = browser.find_elements_by_xpath("//*[contains(text(), '1.         ')]") #Find the first link
pdb.set_trace()
