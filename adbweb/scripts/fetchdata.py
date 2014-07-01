import requests
from bs4 import BeautifulSoup
import requests_cache
from collections import defaultdict
requests_cache.install_cache('demo_cache')

#This is a function to bring up card info
#it bring up page in first line and turns it into html text
#i think the soup makes it like that
#then it looks for the title 'h4' then it .contents looks in the array which is broken by , and gets 2nd one (0,1,2)
# we did the same for small
card_codename = {}
def get_card(card_id):
    page = requests.get("http://littleakiba.com/tcg/weiss-schwarz/card.php?card_id=" + card_id).text
    soup = BeautifulSoup(page)
#print(soup.prettify())
    #print card_id

    if len(soup.find('h4').contents) ==3:
        #print card_name = soup.find('h4').contents[2]
        card_name = soup.find('h4').contents[2]
    else:
        #print 'N/A'
        card_name = 'N/A'

    #print soup.find_all('small')[0].contents[0]
    card_code = soup.find_all('small')[0].contents[0].split(' ')[0]
    card_codename[card_code] = card_name

#this code is how to use the function get_card
#get_card("4194")

page = requests.get("http://littleakiba.com/tcg/weiss-schwarz/card.php?series_id=46").text
soup = BeautifulSoup(page)
for link in soup.find_all('a'):

    if 'card_id' in link["href"]:
        card_id = link["href"].split("=")[1]
        get_card(card_id)

card_data = defaultdict(int)

for line in file('carddata.txt'):
    card_code = line.split(',')[0]
    card_number = line.split(',')[1].strip()
    card_data[card_code] = int(card_number)
for line in file('bakemonogatari.txt'):
    card_code = line.split(':')[0]
    card_number = line.split(':')[1].strip()
    card_data[card_code] = card_data[card_code] + int(card_number)
print card_data
#print card_codename
decks = []
cards = {}
for line in file('cards.txt'):
    if line.strip() == "":
        decks.append(cards)
        cards = {}
    else:
        card_code = line.split(':')[0]
        card_number = line.split(':')[1].strip()
        card_name = line.split(':')[2].strip()
        cards_required = str(int(card_number)-int(card_data[card_code]))

        #print card_codename[card_code.upper().replace('E', '')]
        #card_info = cards_required + " x " + card_name
        cards[card_code] = {
            "name": card_name,
            "target": card_number,
            "owned": str(card_data[card_code]),
            "required": cards_required,
        }

deck = decks[2]
print "Cards Required:"
card_totalaim = 0
for card in deck.values():
    print card["required"] + " x " + card["name"]
    card_totalaim = card_totalaim + int(card['target'])

print "Cards Owned:"
card_total = 0
for card in deck.values():
    if card["owned"] != "0":
        print card["owned"] + " x " + card["name"]
    card_total = card_total + int(card["owned"])
percentage = card_total * 100 / card_totalaim
print str(card_total) + ' / ' + str(card_totalaim)
print 'Completion: ' + str(percentage) + '%'