#!env/bin/python3
import subprocess
import argparse
from htmldom import htmldom
import difflib
import urllib.parse
import os

# force latin1 encoding.
class LatinHtmlDom(htmldom.HtmlDom):
    def getEncoding(self, response):
        return "iso-8859-1";

def MyURL(uri, path="", query=""):
    theURI = urllib.parse.quote(urllib.parse.urljoin(uri, path), safe=':/.')
    if (query == None):
        query = ""
    if isinstance(query, list):
        query = [urllib.parse.quote(arg, safe='=/:.') for arg in query]
    else:
        query = [urllib.parse.quote(query, safe='=/:.&')]
    if (len(query) > 0):
        theURI += "?" + "&".join(query)
    o = urllib.parse.urlparse(theURI)
    return o.geturl()

def getFiles(url1, url2):
    oldcmd = ["wget", "-O", "url1-output.html", url1];
    newcmd = ["wget", "-O", "url2-output.html", url2];
    subprocess.call(oldcmd);
    subprocess.call(newcmd);

def FindNodes(document, find):
    if document:
        return document.find(find)
    else:
        raise Exception("no document loaded")

def rstripList(list): return [x.rstrip("\n") for x in list]

def DOMDiff(url1, url2, findDOM):
    print("site1: {}".format(url1));
    print("site2: {}".format(url2));

    site1Document = LatinHtmlDom(url1)
    site1Document.createDom()
    site2Document = LatinHtmlDom(url2)
    site2Document.createDom()

    myRes = ""
    for domQuery in findDOM:
        print("finddom: " + domQuery + " at " + url1)
        print("finddom: " + domQuery + " at " + url2)

        site1Text = []
        site2Text = []
        for node in  FindNodes(site1Document, domQuery):
            site1Text.append(node.html())
        for node in  FindNodes(site2Document, domQuery):
            site2Text.append(node.html())

        count = len(site1Text)
        if (count < len(site2Text)):
            count = len(site2Text)
        for i in range(count):
            if not i in site1Text:
                site1Text.append("")
            if not i in site2Text:
                site2Text.append("")
                res = list(diff(site1Text[i], site2Text[i], url1, url2))
                if (len(res) == 0):
                    print("{sel} {i}: no differences".format(
                        sel=domQuery,
                        i=i
                    ))
                else:
                    print("{sel} {i}: diff:\n{diff}".format(
                        sel=domQuery,
                        i=i,
                        diff="\n".join(rstripList(res))
                    ))
        print("done comparing {query}:\n{url1}\n{url2}".format(
            query=domQuery,
            url1=url1,
            url2=url2
        ))

def diff(old, new, oldStr="old", newStr="new"):
    return difflib.unified_diff(
        old.split("\n"),
        new.split("\n"),
        fromfile=oldStr,
        tofile=newStr
    )

def _cli():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument(
        '-get',
        required=False,
        action='store_true',
        help='download the content, stored in ./url1-output.html, ./url2-output.html'
    )
    parser.add_argument(
        '-url1',
        type=str,
        required=False,
        help='url1 URL',
        default="file://"+os.path.join(os.getcwd(), 'url1-output.html')
    )
    parser.add_argument(
        '-url2',
        type=str,
        required=False,
        help='url2 URL',
        default="file://"+os.path.join(os.getcwd(), 'url2-output.html')
    )
    parser.add_argument(
        '-path',
        type=str,
        required=False,
        help='common path string'
    )
    parser.add_argument(
        '-query',
        type=str,
        required=False,
        help='query string'
    )
    parser.add_argument(
        '-find',
        type=str,
        required=False,
        help='DOM query string',
        action='append'
    )

    return parser.parse_args()

def main():
    args = _cli()
    print(repr(args.find))
    url1 = MyURL(args.url1, args.path, args.query)
    url2 = MyURL(args.url2, args.path, args.query)

    if args.find == None:
        args.find = ['body']

    if (args.get):
        getFiles(url1, url2)
    else:
        DOMDiff(url1, url2, args.find);

if __name__ == "__main__": main()
