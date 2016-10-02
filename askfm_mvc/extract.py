
from bs4 import BeautifulSoup
from urllib import request
import pickle
import os
import argparse


def get_html(url):
    r = request.urlopen(url)
    return r.read()


def read_html(doc):
    soup = BeautifulSoup(doc, 'html.parser')
    return soup


def get_image_as_str(url):
    r = request.urlopen(url)
    return r.read()


def process_soup(sp, newline):
    whole_answer_chunks = sp.find_all("div", class_="item streamItem streamItem-answer")

    whole_answer_list = []

    for ans in whole_answer_chunks:
        qanda = {"id"       : -1,
                 "question" : "",
                 "answer"   : "",
                 "asker"    : "Anon",
                 "date"     : "",
                 "url"      : "",
                 "likes"    : 0,
                 "media"    : None,}

        question = ans.find("div", class_="streamItemContent streamItemContent-question")
        qanda["question"] = question.find("h2").get_text().strip()
        asker = question.find("a", class_="questionersName")
        if asker:
            qanda["asker"] = asker.get_text().strip()

        for anschunk in ans.find_all("p", class_="streamItemContent streamItemContent-answer"):
            qanda["answer"] += newline + anschunk.get_text()

        meta = ans.find("a", class_="streamItemsAge")
        qanda["date"] = meta["title"]
        qanda["url"] = meta["href"]
        qanda["id"] = int(qanda["url"].split("/")[-1])
        qanda["likes"] = int(ans.find("a", class_="counter").get_text())

        media = ans.find("div", class_="streamItem-visualItem")
        if media:
            qanda["media"] = get_image_as_str(media.find("a")["data-url"])

        whole_answer_list.append(qanda)

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
        if pagenum == 2:
            break
        if len(all_qa) == 0:
            print("  Problem with data:\n{}".format(doc))
            break
    
    output = []
    for qa in reversed(all_qa):
        try:
            output.append(newline)
            output.append("{asker} asks: {question}".format(**qa))
            output.append(newline)
            output.append(qa["answer"])
            output.append(newline)
            output.append(qa["date"] + "  likes: " + str(qa["likes"]))
            output.append(newline)
            output.append(qa["url"])
            output.append(newline)
            if qa["media"]:
                with open("{}.jpg".format(qa["id"]), "wb") as f:
                    f.write(qa["media"])
            #done
        except KeyError:
            output.append(newline + "ERROR OCCURRED" + newline)

    print("returning lots of output")
    return newline.join(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract all question/answers from someone's ask.fm account")
    parser.add_argument("account name", type=str,
                        help="The person's username.")
    args = vars(parser.parse_args())
    print(extract(args["account name"]))
