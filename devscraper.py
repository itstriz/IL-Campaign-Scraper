from bs4 import BeautifulSoup
import urllib2


def get_items(data):
    """ Get '<item>' data from text """
    soup = BeautifulSoup(data)
    data_items = []
    for data_item in soup.find_all('item'):
        item_dict = {   'title':            data_item.title.text,
                        'link':             data_item.link.text,
                        'description':      data_item.description.text,
                        'pub_date':         data_item.pubdate.text,
                        'guid':             data_item.guid.text
                    }
        data_items.append(item_dict)
    
    return data_items

def get_url_contents(url):
    """ Turn URL into plain text feed """
    response = urllib2.urlopen(url)
    html = response.read()

    return html


# Declare main RSS URL
rss_url = 'http://www.elections.il.gov/rss/SBEReportsFiledWire.aspx'

# Get the raw feed and turn it into text
data = get_url_contents(rss_url)

# Split up the individual <item> XML data
data = get_items(data)
