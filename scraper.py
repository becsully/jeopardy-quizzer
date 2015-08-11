# -*- coding: utf-8 -*-

import csv
from bs4 import BeautifulSoup
import requests
from pprint import pprint


def til_em(string):
    answer = ""
    while True:
        for i in range(len(string)):
            if string[i:i+5] != "</em>":
                answer += string[i]
            else:
                break
        break
    return answer.encode('ascii','ignore')


def text_from_code(soup_object):
    print soup_object
    try:
        text = soup_object.string.encode('ascii', 'ignore')
    except AttributeError:
        try:
            raw_text = soup_object.find("td", {"class": "clue_text"}).strings
            text = ""
            for string in raw_text:
                text += string.encode('ascii','ignore')
        except AttributeError:
            text = "Sorry, there's been an error."
    print text
    return text


def de_html(soup_object):
    temp_clue = str(soup_object)
    clue = ""
    html_tag_closed = True
    for i in range(len(temp_clue)-2):
        if temp_clue[i] == "<":
            html_tag_closed = False
        elif temp_clue[i] == ">":
            html_tag_closed = True
        elif html_tag_closed:
            try:
                clue += temp_clue[i].encode('ascii', 'ignore')
            except UnicodeDecodeError:
                pass
        else:
            pass
    return clue.encode('ascii', 'ignore')


def scraper(url):
    print "Scraping clues from " + url
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html.parser')

    categories = {}
    raw_categories = soup.findAll("td", {"class": "category_name"})
    for i in range(2):
        for j in range(6):
            name = "%i%i" % (i, j)
            categories[name] = de_html(raw_categories[i*6+j])
    categories["FINAL JEOPARDY"] = de_html(raw_categories[12])

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
            answer = til_em(raw_answer2)
        except TypeError:
            answer = "(none)"

        try:
            value = (question.find("td", {"class": "clue_value"})).string.encode('ascii', 'ignore')
        except:
            value = "Either this was a Daily Double, or the clue was not reached."

        try:
            clue = de_html(question.find("td", {"class": "clue_text"}))
        except AttributeError:
            clue = "This question was not reached."

        if count == 60:
            category = categories["FINAL JEOPARDY"]
            value = "Final Jeopardy!"
            final_raw = soup.find("table", {"class": "final_round"})
            raw_answer = final_raw.find("div")["onmouseover"].split('correct_response')[1]
            answer = til_em(raw_answer)[3:]

        question_dict = {"Clue": clue, "Value": value, "Answer": answer, "Category": category}
        q_list.append(question_dict)
        count += 1

    print "done with scraping a page!"
    return q_list


def saver(q_list):
    fieldnames = ["Category","Value","Clue","Answer"]
    with open("answers.csv", "ab") as jeopardy_csv:
        writer = csv.DictWriter(jeopardy_csv, fieldnames=fieldnames)
        for clue in q_list:
            if clue["Clue"] == "This question was not reached.":
                pass
            else:
                writer.writerow(clue)
    jeopardy_csv.close()
    print "done with saving a set of questions!"


def blank_remover():
    count = 0
    with open("new_answers2.csv", "rb") as original:
        for line in original:
            if count < 100228:
                with open("new_answers3.csv", "ab") as replacement:
                    replacement.write(line)
                    replacement.close()
                count += 1
            else:
                if count % 2 == 0:
                    count += 1
                    pass
                else:
                    with open("new_answers3.csv", "ab") as replacement:
                        replacement.write(line)
                        replacement.close()
                        count += 1
        print "done"
    original.close()


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


def test():
    #url = "http://www.j-archive.com/showgame.php?game_id=3938"
    #url = "http://j-archive.com/showseason.php?season=26"
    #base_scraper(url)
    #pprint(scraper(url))
    blank_remover()


def main():
    for i in range(28,32):
        url = "http://j-archive.com/showseason.php?season=%i" % i
        print "Scraping Season #%i" % i
        base_scraper(url)
    print "done done done all scraping!"
    blank_remover()
    print "ALL DONE"


if __name__ == "__main__":
    test()