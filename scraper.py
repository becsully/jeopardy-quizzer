# -*- coding: utf-8 -*-

import csv
from bs4 import BeautifulSoup
import requests
from pprint import pprint


def scraper(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html.parser')

    categories = {}
    raw_categories = soup.findAll("td", {"class": "category_name"})
    for i in range(2):
        for j in range(6):
            name = "%i%i" % (i, j)
            try:
                categories[name] = raw_categories[i*6+j].string.encode('ascii', 'ignore')
            except AttributeError:
                raw_category = raw_categories[i*6+j].strings
                categories[name] = ""
                for string in raw_category:
                    categories[name] += string.encode('ascii','ignore')
    categories["FINAL JEOPARDY"] = raw_categories[12].string.encode('ascii', 'ignore')

    q_list = []
    questions = soup.findAll("td", {"class": "clue"})
    count = 0

    for question in questions:

        if count < 30:
            x = "0"
        else:
            x = "1"

        cate_name = "%s%i" % (x, (count % 6))
        category = categories[cate_name]

        try:
            raw_answer = (question.find("div"))["onmouseover"]
            raw_answer2 = (raw_answer.split('response">')[1]).encode('ascii', 'ignore')
            answer = ""
            while True:
                for i in range(len(raw_answer2)):
                    if raw_answer2[i:i+5] != "</em>":
                        answer += raw_answer2[i]
                    else:
                        break
                break
        except TypeError:
            answer = "(none)"

        try:
            value = (question.find("td", {"class": "clue_value"})).string.encode('ascii', 'ignore')
        except:
            value = "Either this was a Daily Double, or the clue was not reached."

        try:
            clue = (question.find("td", {"class": "clue_text"})).string.encode('ascii', 'ignore')
            if clue == None:
                temp_clue = (question.find("div"))["onmouseout"].split("', '")[2]
                clue = ""
                html_tag_closed = True
                for i in range(len(temp_clue)-2):
                    if temp_clue[i] == "<":
                        html_tag_closed = False
                    elif temp_clue[i] == ">":
                        html_tag_closed = True
                    elif html_tag_closed:
                        clue += temp_clue[i]
                    else: pass
        except AttributeError:
            try:
                raw_clue = question.find("td", {"class": "clue_text"}).strings
                clue = ""
                for string in raw_clue:
                    clue += string.encode('ascii','ignore')
            except AttributeError:
                clue = "This question was not reached."

        if count == 60:
            category = categories["FINAL JEOPARDY"]
            value = "Final Jeopardy!"

        question_dict = {"Clue": clue, "Value": value, "Answer": answer, "Category": category}
        q_list.append(question_dict)
        count += 1

    print "done with scraping a page!"
    return q_list


def saver(q_list):
    fieldnames = ["Category","Value","Clue","Answer"]
    with open("answers.csv", "a") as jeopardy_csv:
        writer = csv.DictWriter(jeopardy_csv, fieldnames=fieldnames)
        for clue in q_list:
            writer.writerow(clue)
    jeopardy_csv.close()
    print "done with saving a set of questions!"


def base_scraper(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html.parser")
    links = []
    raw_links = soup.findAll("td", {"style": "width:140px"})
    for show in raw_links:
        show_link = show.find("a").get('href')
        links.append(show_link)
    for link in links:
        saver(scraper(link))
    print "done done done with everything!"


def test():
    url = "http://www.j-archive.com/showgame.php?game_id=4589"
    #url = "http://j-archive.com/showseason.php?season=30"
    #base_scraper(url)
    pprint(scraper(url))


if __name__ == "__main__":
    test()