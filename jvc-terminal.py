#!/usr/bin/python3
# coding: utf-8

from requests import get
import re
import bs4
import argparse
from prettytable import PrettyTable

# Ce programme permet de parser une page de forum issue du site jeuxvideo.com
# Indiquez en argument le lien de la page que vous voulez parser avec le drapeau '--url' ou '-u'
# Écrit par Antoine Paix
# Programme sous licence libre
# Dernière modification : 23/02/2020

# Arguments de la ligne de commande
parser = argparse.ArgumentParser(description="Affiche les différents topics des forums du site jeuxvideo.com")
requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument("-u", "--url", type=str, required=True, help="lien du forum à afficher")
args = parser.parse_args()

# url_jvc = 'http://www.jeuxvideo.com/forums/0-51-0-1-0-1-0-blabla-18-25-ans.htm'
url_jvc = args.url
request_text = get(url_jvc).text
page = bs4.BeautifulSoup(request_text, "html.parser")
topic_list = page.find('ul', class_='topic-list topic-list-admin')
topic_list = topic_list.findAll('li', {'data-id':re.compile('[0-9]{8}')})

# def remove_emoji(string):
#     emoji_pattern = re.compile("["
#                            u"\U0001F600-\U0001F64F"  # emoticons
#                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
#                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
#                            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
#                            u"\U00002702-\U000027B0"
#                            u"\U000024C2-\U0001F251"
#                            "]+", flags=re.UNICODE)
#     return emoji_pattern.sub(r'', string)

def TopicParser(topic):
    topic_title = topic.find('a', {'class':'lien-jv topic-title'}).get_text().strip() # nom du topic
    # topic_title = remove_emoji(topic_title)
    topic_link = "http://www.jeuxvideo.com" + topic.find('a', {'class':'lien-jv topic-title'}).get('href') # lien http du topic
    nb_messages = topic.find('span', {'class':'topic-count'}).get_text().strip() # nombre de messages sur le topic
    last_mes = topic.find('span', {'class':'topic-date'}).get_text().strip() # heure (ou date) du dernier message posté
    auteur = topic.find('span', {'class':'topic-author'}).get_text().strip() # auteur original du topic

    return topic_title, auteur, nb_messages, last_mes

# Using prettytable for printing datas
x = PrettyTable()
x.field_names = ["SUJET", "AUTEUR", "NB", "DERNIER MSG"]

for topic in topic_list:
    x.add_row([*TopicParser(topic)])


print(x)