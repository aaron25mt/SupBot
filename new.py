from splinter import Browser
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

caps = DesiredCapabilities.FIREFOX
caps["marionette"] = True
caps["binary"] = "/Applications/Firefox.app/Contents/MacOS/firefox-bin"

with Browser('firefox', capabilities=caps) as browser:
	base_url = "http://www.supremenewyork.com/shop/all/"
	category = "shirts"
	
	browser.visit(base_url + category)