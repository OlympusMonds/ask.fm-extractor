
from bs4 import BeautifulSoup
import urllib
import cPickle as pickle
import os
import argparse


def get_html(url):
    r = urllib.urlopen(url)
    return r.read()


def read_html(doc):
    soup = BeautifulSoup(doc, 'html.parser')
    return soup


def process_soup(sp):
    whole_answer_chunks = sp.find_all("div", class_="item streamItem streamItem-answer")

    whole_answer_list = []

    for ans in whole_answer_chunks:
        ansdict = {"question" : "",
                   "answer"   : ""}
        ansdict["question"] = ans.find("h1", class_="streamItemContent streamItemContent-question").get_text().strip()
        for anschunk in ans.find_all("p", class_="streamItemContent streamItemContent-answer"):
            ansdict["answer"] += "\n" + anschunk.get_text()
        whole_answer_list.append(ansdict)

    return whole_answer_list


def extract(account_name):
    picklefile = "sj.p"

    if os.path.isfile(picklefile):
        with open(picklefile, 'rb') as f:
            all_qa = pickle.load( f )
    else:
        all_qa = []
        doc = None
        pagenum = 1
        while doc != "":
            url = "https://ask.fm/{}/answers/more?page={}".format(account_name, pagenum)
            doc = get_html(url)
            sp = read_html(doc)
            all_qa.extend(process_soup(sp))
            pagenum += 1

        with open(picklefile, 'wb') as f:
            pickle.dump( all_qa, f )

    for qa in reversed(all_qa):
        try:
            print
            print qa["question"]
            print qa["answer"]
            print
            print "================="
        except:
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract all question/answers from someone's ask.fm account")
    parser.add_argument("account name", type=str,
                        help="The person's username.")
    args = vars(parser.parse_args())
    extract(args["account name"])
