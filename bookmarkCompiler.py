import sys
import os
import subprocess
import urllib.parse as urlparse
from bs4 import BeautifulSoup
import urllib3
from yattag import Doc

#accept command line input with sys module - file path

def main():
    path = sys.argv[1]
    fileList = os.listdir(path)
    str = path+"{0}"
    fileList = [str.format(f) for f in fileList]
    linkList = list(set(combineLinks(fileList)))
    linkList = checkLinks(linkList)
    finalList = constructMaster(linkList)
    final = open('bookmarx.html', 'w')
    final.write(constructDoc(finalList))
    final.close()


def combineLinks(fileList):
    linkList = []
    for fName in fileList:
        f = open(fName, "r", encoding="utf8")
        f.close
        soup = BeautifulSoup(f, 'html.parser')
        for link in soup.find_all('a'):
            linkList.append(link.get('href'))
    return linkList

def checkLinks(linkList):
    http = urllib3.PoolManager(timeout=7.0)
    for l in linkList:
        try:
            req = http.request('GET', l, retries=urllib3.Retry(redirect=2, raise_on_redirect=False))
            if(req.status != 200):
                linkList.remove(l)
                print("removed with STATUS CODE {}  {}".format(req.status, l))
            else:
                print("added {}".format(l))
        except:
            print("Could not connect {} ... removed".format(l))
            linkList.remove(l)
    return linkList

def constructMaster(linkList):
    listOfLists = []
    subList = []
    domains = []
    for l in linkList:
        domains.append(urlparse.urlsplit(l)[1])
    domains = sorted(list(set(domains)))
    n = 0
    for d in domains:
        print("{}  {}".format(n, d))
        n += 1

    for d in domains:
        for l in sorted(linkList):
            if d in l:
                subList.append(l)
        listOfLists.append(subList)
        subList = []
    if len(listOfLists) == len(domains):
        master = zip(domains, listOfLists)
    else:
        print(len(listOfLists)-len(domains))
        return []
    return master


    #for l in sorted(linkList):
    #   for x in range(len(domains)):
    #        if domains[x] in l:
    #            subList.append(l)
    #            print("{}   {}".format(domains[x], l))
    #    listOfLists.append((domains[x], subList))
    #    subList = []
    #print(listOfLists)
    #if len(listOfLists) == len(domains):
    #    master = zip(domains, listOfLists)
    #else:
    #    print(len(listOfLists)-len(domains))
    #    return []
   # return master

def constructDoc(masterList):
    doc, tag, text = Doc().tagtext()

    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        with tag('body'):
            for data in masterList:
                #with tag('div', klass=data[0]):
                with tag('h3'):
                    text(data[0])
                doc.stag('br')
                for i in data[1]:
                    with tag('a', href=i):
                        text(i)
                    doc.stag('br')
                            #str = '<a href = "{}"/>'.format(i)
                            #line('li', str)
    return doc.getvalue()
                                
if __name__=="__main__":
    main()
