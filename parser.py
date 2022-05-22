from urllib.request import urlopen
from bs4 import BeautifulSoup


def getLine(url, short_name):
    html = urlopen(url)
    bs = BeautifulSoup(html.read(), 'html.parser')
    for country_url in bs.find_all('a'):
        if country_url.get_text() == short_name:
            line = country_url.parent.parent
    return(line)


def getSomeLetter(url, short_name):
    same_letter_count = 0
    html = urlopen(url)
    bs = BeautifulSoup(html.read(), 'html.parser')
    table = bs.find('table', {'class':'wikitable'})
    for country_url in table.find_all('a')[1::2]:
        if short_name[0] == country_url.get_text()[0]:            
            same_letter_count += 1
    return(same_letter_count)


def getMainData(line_in_table, counter):

    country_dict = {"country": "", "full_country_name": "","same_letter_count": counter,"link_to_photo": ""}

    link_to_photo = line_in_table.find('a', {'class': 'image'}).attrs['href'].split(":")[1]
    link_to_photo = "https://ru.wikipedia.org/wiki/Список_государств#/media/Файл:" + link_to_photo
    short_name = line_in_table.find('a', {'class': None}).getText()
    full_country_name = line_in_table.find_all('td')[3].getText()
    
    country_dict["country"] = short_name
    country_dict["full_country_name"] = full_country_name.strip('\n')
    country_dict["link_to_photo"] = link_to_photo
    return(country_dict)


def main(url, short_name, list_of_dict):
    
    line_in_table = getLine(url, short_name)
    counter = getSomeLetter(url, short_name)
    dict_of_statistic = getMainData(line_in_table, counter)
    list_of_dict = list_of_dict.append(dict_of_statistic)
    return(dict_of_statistic, list_of_dict)


url = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE%D1%81%D1%83%D0%B4%D0%B0%D1%80%D1%81%D1%82%D0%B2'
list_of_dict = []


print("Введите короткое название страны на русском языке, соблюдая регистр и пунктуацию")
short_name = input(str())

main(url, short_name, list_of_dict)
print(list_of_dict)