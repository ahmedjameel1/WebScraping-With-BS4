# Web Scrapping
import requests
from bs4 import BeautifulSoup
import csv
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

colorama_init()


date = input('Enter A Date in the Next format => MM/DD/YYYY: ')
page = requests.get(
    f'https://www.yallakora.com/match-center/%D9%85%D8%B1%D9%83%D8%B2-%D8%A7%D9%84%D9%85%D8%A8%D8%A7%D8%B1%D9%8A%D8%A7%D8%AA?date={date}')


def main(page):

    src = page.content
    soup = BeautifulSoup(src, "lxml")
    matches_details = []

    # get championships
    championships = soup.find_all("div", {'class': "matchCard"})

    def get_championship_info(championships):

        championship_title = championships.contents[1].find("h2").text.strip()
        all_matches = championships.contents[3].find_all("li")

        for i in range(len(all_matches)):

            # get teams
            teamA = all_matches[i].find('div', {'class': "teamA"}).text.strip()
            teamB = all_matches[i].find('div', {'class': "teamB"}).text.strip()

            # result
            match_result = all_matches[i].find(
                'div', {'class': "MResult"}).find_all('span', {'class': "score"})
            score = f'{match_result[0].text.strip()} - {match_result[1].text.strip()}'

            # time
            match_time = all_matches[i].find(
                'span', {'class': "time"}).text.strip()

            # add to the matches_details list
            matches_details.append({'نوع البطولة': championship_title, 'الفريق الاول': teamA, 'الفريق الثاني': teamB,
                                    'النتيجة': score, 'الوقت': match_time})

    for i in range(len(championships)):
        get_match_info(championships[i])

    keys = matches_details[0].keys()

    with open('documents/match_details.csv', 'w', encoding='utf-8') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(matches_details)
        print(f"{Fore.GREEN}Success!{Style.RESET_ALL}")


main(page)
