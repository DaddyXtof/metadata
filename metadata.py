import json
import requests
import sys

startingURL = "http://169.254.169.254/latest/"
dic = {'latest': {}}


def parseURL(url, dic):
    resp = requests.get(url)
    if resp.status_code == 404:
        return
    for r in resp.text.split('\n'):
        if not r:
            continue
        if r == "dynamic" or r == "meta-data" or r == "user-data":
            r += '/'
        if r[-1] != '/':
            dic[r] = {}
            dic[r] = getData(url + r)
            if len(sys.argv) > 1 and sys.argv[1] == r:
                print(sys.argv[1] + ": ")
                print(dic[r])
        else:
            newURL = url + r
            newIndex = r[0:len(r) - 1]
            dic[newIndex] = {}
            parseURL(newURL, dic[newIndex])
    return dic


def getData(url):
    a = requests.get(url)
    try:
        val = json.loads(a.text)
    except ValueError:
        val = a.text
    return val


if __name__ == '__main__':
    if len(sys.argv) > 1:
        print("Searching for... " + sys.argv[1] + '\n')
    with open("metadata.txt", "w") as mFile:
        json.dump(parseURL(startingURL, dic), mFile, indent=4)
        print('Latest metadata saved to metadata.txt' + '\n')