# pythonDOMComparitor

Compare parts of HTML pages using python

This script is not necessarily secure. It runs wget in a subprocess when -get is specified on the command line.

# Usage

\# compare the body of 2 urls, both with the same query.
dom.py -url1 http://eg.com -url2 http://eg2.com -query="a=1" -find body

\# download the 2 given urls with path, store the output for testing.
dom.py -get -url1 http://eg.com -url2 http://dev.eg.com -path=/route

\# compare html stored in url1-output.html and url2-output.html
\# comopare the content of all div.content and all div.footer elements
\# (CSS selectors)
dom.py -find div.content -find div.footer

# parameters:

* -url1 {URL}
: Set the first url to load data from. If not specified, the script uses
: file://$PWD/url1-output.html.
* -url2 {URL}
: Set the first url to load data from. If not specified, the script uses
: file://$PWD/url2-output.html.
* -query {querystring}
: The given query is added to the URLs.
: (if there is already a query string, this wont work.)
: May be specified multiple times.
* -path {/common/path/at/end/of/url}
: The given path is added to the end of the URL string.
* -get
: Download the content of the specified URLs.
* -find "{css selector}"
: Find the given CSS selector in the HTML content. Compare each resulting element with diff, show the output.
: may be specified multiple times.

# Installation

You need the python module HtmlDom to make this work.

eg:
```
pip install HtmlDom
```

Otherwise, this is pretty trivial. It is a script.
