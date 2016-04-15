
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


def process_soup(sp, newline):
    whole_answer_chunks = sp.find_all("div", class_="item streamItem streamItem-answer")

    whole_answer_list = []

    for ans in whole_answer_chunks:
        ansdict = {"question" : "",
                   "answer"   : ""}
        ansdict["question"] = ans.find("h1", class_="streamItemContent streamItemContent-question").get_text().strip()
        for anschunk in ans.find_all("p", class_="streamItemContent streamItemContent-answer"):
            ansdict["answer"] += newline + anschunk.get_text()
        whole_answer_list.append(ansdict)

    return whole_answer_list


def extract(account_name, newline = "\n", cache_raw=False):
    all_qa = []
    
    if cache_raw:
        picklefile = "{}.p".format(account_name)

        if os.path.isfile(picklefile):
            with open(picklefile, 'rb') as f:
                all_qa = pickle.load( f )
    
    doc = None
    pagenum = 0
    while doc != "":
        url = "https://ask.fm/{}/answers/more?page={}".format(account_name, pagenum)
        doc = get_html(url)
        sp = read_html(doc)
        all_qa.extend(process_soup(sp, newline))
        pagenum += 1
        print("  Finished page num {}".format(pagenum))
        if len(all_qa) == 0:
            print("  Problem with data:\n{}".format(doc))
            break
    
    if cache_raw:
        with open(picklefile, 'wb') as f:
            pickle.dump( all_qa, f )
    
    output = []
    for qa in reversed(all_qa):
        try:
            output.append(newline)
            output.append("=================")
            output.append(qa["question"])
            output.append("----")
            output.append(qa["answer"])
            output.append(newline)
        except KeyError:
            output.append(newline + "ERROR OCCURRED" + newline)

    print("returning lots of output")
    return newline.join(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract all question/answers from someone's ask.fm account")
    parser.add_argument("account name", type=str,
                        help="The person's username.")
    args = vars(parser.parse_args())
    print extract(args["account name"])
