import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup

TOKEN = '6892414329:AAE4sd8QC7Tbi8OUuLJwhRS_YpUOpKePkEs'
bot = telebot.TeleBot(TOKEN)
CHANNEL_ID = '-1002064240401' 

def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    div_container = soup.find('div', {'class': 'shop-container'})  
    if div_container is not None:
        img_tags = div_container.find_all('img')
        img_urls = [tag['src'] for tag in img_tags]
        return img_urls
    else:
        return []

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('African')
    itembtn2 = types.KeyboardButton('Acrylic')
    itembtn3 = types.KeyboardButton('charcoal')
    itembtn4 = types.KeyboardButton('Ethiopian')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    bot.send_message(message.chat.id, "click on a button:", reply_markup=markup)

def handle_button(message, url):
    img_urls = scrape_website(url)  
    for img_url in img_urls:
        if not img_url.startswith('http'):
            img_url = 'https://telsemarts.com/' + img_url  
        try:
            response = requests.get(img_url)
            response.raise_for_status()
        except (requests.HTTPError, requests.ConnectionError):
            print(f"Unable to access image at {img_url}")
            continue
        bot.send_photo(CHANNEL_ID, img_url)  

@bot.message_handler(func=lambda message: message.text == 'African')
def handle_button1(message):
    handle_button(message, 'https://telsemarts.com/product-category/african/')

@bot.message_handler(func=lambda message: message.text == 'Acrylic')
def handle_button2(message):
    handle_button(message, 'https://telsemarts.com/product-category/acrylic/')

@bot.message_handler(func=lambda message: message.text == 'charcoal')
def handle_button3(message):
    handle_button(message, 'https://telsemarts.com/product-category/charcoal/')

@bot.message_handler(func=lambda message: message.text == 'ethiopian')
def handle_button4(message):
    handle_button(message, 'https://telsemarts.com/product-category/ethiopian/')

bot.polling()

