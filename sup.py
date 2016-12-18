MAIN_URL = "http://52.5.44.158/shop/all/"
TARGETS = [] #['Category', 'Item 1', 'Color', 'Size']
#Categories: jackets, shirts, tops-sweaters, sweatshirts, pants, shorts, hats, bags, accessories, shoes, skate
INFO = []
#[Name, Email, Tel, Address, ZIP, City, State, Country, Card Type, Card Number, MM, YYYY, CVV]
#Cards: master, visa, american_express

from bs4 import BeautifulSoup
from splinter import Browser
from time import sleep, time
import urllib.request as urllib2
from multiprocessing import Pool

def getShopItems(soup):
	return soup.find_all("div", class_="inner-article")

def itemName(soup, link):
	return soup.find_all("a", class_="name-link", href=link)[0].text

def itemColor(soup, link):
	return soup.find_all("a", class_="name-link", href=link)[1].text

def isAvailable(soup):
	return soup.find("div", class_="sold_out_tag") == None

def addToCart(browser, link, size):
	browser.visit(link)
	if(size != ""):
		browser.find_option_by_text(size).first.click()
	browser.find_by_name("commit").first.click()

def checkout(browser, info):
	browser.visit("https://www.supremenewyork.com/checkout")
	browser.fill("order[billing_name]", info[0])
	browser.fill("order[email]", info[1])
	browser.fill("order[tel]", info[2])
	browser.fill("order[billing_address]", info[3])
	browser.fill("order[billing_zip]", info[4])
	browser.fill("order[billing_city]", info[5])
	browser.select("order[billing_state]", info[6])
	browser.select("order[billing_country]", info[7])
	browser.find_by_tag("ins").first.click()
	browser.select("credit_card[type]", info[8])
	browser.fill("credit_card[cnb]", info[9])
	browser.select("credit_card[month]", info[10])
	browser.select("credit_card[year]", info[11])
	browser.fill("credit_card[vval]", info[12])
	browser.find_by_tag("ins").last.click()
	browser.find_by_name("commit").first.click()

def main():
	browser = Browser("firefox", user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/601.6.17 (KHTML, like Gecko) Version/9.1.1 Safari/601.6.17")
	for grail in TARGETS:
		soup = BeautifulSoup(urllib2.urlopen(MAIN_URL + grail[0].lower()).read(), "html.parser")
		sleep(.04)
		shopItems = getShopItems(soup)
		'''
		for item in shopItems:
			if(grail[1].capitalize() in item.text and grail[2].capitalize() in item.text):
				if(isAvailable(item)):
					addToCart(browser, "https://www.supremenewyork.com" + item.find('a').get("href"), grail[3].capitalize())
				break
		sleep(.02)
		print("")
	sleep(.02)
	print("[SupBot] Checking out...")
	checkout(browser, INFO)
	print("[SupBot] Checked out!")
		'''
		for item in shopItems:
			itemLink = item.find('a').get("href")
			grailName = itemName(soup, itemLink)
			grailColor = itemColor(soup, itemLink)
			if(grail[1] in grailName.lower() and grail[2] in grailColor.lower()):
				if(isAvailable(item)):
					print("[SupBot] {} in {} is available. Adding to cart...".format(grailName, grailColor))
					print("[SupBot] Store Link: https://www.supremenewyork.com" + itemLink)
					addToCart(browser, "https://www.supremenewyork.com" + itemLink, grail[3].capitalize())
					print("[SupBot] {} in {} has been added to cart.".format(grailName, grailColor))
				else:
					print("[SupBot] {} in {} is sold out.".format(grailName, grailColor))
				break
		sleep(.02)
		print("")
	sleep(.02)
	print("[SupBot] Checking out...")
	checkout(browser, INFO)
	print("[SupBot] Checked out!")

start_time = time()
main()
print("[SupBot] Finished in {} seconds!".format(time() - start_time))