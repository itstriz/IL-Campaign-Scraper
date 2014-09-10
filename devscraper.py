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

def split_link(link):
    """ Pull out various parts of link item """
    full_link = {}
    
    base_url = link.find('.gov/')
    bu_pos = base_url+5
    base_url = link[:bu_pos]
    
    uf_pos = link.find('/', bu_pos)
    url_folder = link[bu_pos:uf_pos]
        
    rt_pos = link.find('.', uf_pos)
    report_type = link[uf_pos+1:rt_pos]

    params_start = link.find('?', rt_pos)
    params = split_params(link[params_start:])

    full_link['link'] = link
    full_link['base_url'] = base_url
    full_link['url_folder'] = url_folder
    full_link['report_type'] = report_type
    full_link['params'] = params

    return full_link

def split_params(params):
    """ Split up the params string """
    num_params = params.count('=')
    
    param_list = []
    for p in range(1, num_params+1):
        if p == 1:
            start_pos = params.find('?')
            end_pos = params.find('&')
        else:
            start_pos = params.find('&', start_pos+1)
            end_pos = params.find('&', start_pos+1)
        if p == num_params:
            end_pos = len(params)

        param_item = params[start_pos:end_pos]
        param_list.append(param_item)
        
    return param_list

# Declare main RSS URL
rss_url = 'http://www.elections.il.gov/rss/SBEReportsFiledWire.aspx'

# Get the raw feed and turn it into text
data = get_url_contents(rss_url)

# Split up the individual <item> XML data
data = get_items(data)

link = data[2]['link']
print 'URL: ' + link
print split_link(link)
