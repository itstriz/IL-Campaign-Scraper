from bs4 import BeautifulSoup
import sqlite3 as lite
import sys
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

def get_report_types(data):
    """ return a list of all report types from data chunk """
    report_types = []
    for item in data:
        report_type = split_link(item['link'])['report_type']
        if report_type not in report_types:
            report_types.append(report_type)

    return report_types

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

def scrape_report(report_type, url):
    if report_type == 'A1List':
        data = get_url_contents(url)
        soup = BeautifulSoup(data)
        org_name = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_lblName'}).text
        contrib_table = []
        table = soup.find('table', {'id': 'ctl00_ContentPlaceHolder1_tblA1List'})
        
        # Get Committee ID
        org_id_link = table.find('a')
        org_id = org_id_link['href']
        org_id = org_id[org_id.find('=')+1:]

        for row in table.find_all('tr'):
            row_data = []
            for tabledata in row.find_all('td'):
                td_category = str("".join(tabledata['headers']))
                td_category = str.replace(td_category, "ctl00_ContentPlaceHolder1_th", "")
                row_data.append((td_category, str(tabledata.text)))
            # filter out blank lists
            if row_data:
                contrib_table.append(row_data)
        
        results = {'org_name': org_name,
                   'org_id'  : org_id,
                   'contribs': contrib_table}
        return results
    if report_type == 'D2Semi':
        data = get_url_contents(url)
        return data

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
        param_item = split_param_item(param_item)
        param_list.append(param_item)
        
    return param_list

def split_param_item(param_item):
    """ Split up <param>=<value> into dict """
    param_item = str(param_item)

    # Strip out questions marks and ampersands
    param_item = param_item.replace("?", "")
    param_item = param_item.replace("&", "")

    temp_dict = param_item.split("=")
    
    return {temp_dict[0] : temp_dict[1]}

def create_db():
    # start sqlite
    con = None
    try:
        con = lite.connect('campaigns.db')
        cur = con.cursor()
        cur.execute('SELECT SQLITE_VERSION()')
    
        data =cur.fetchone()

        print "SQLITE version: %s" % data

    except lite.Error, e:
        print "Error: %s" % e.args[0]
        sys.exit(1)

    finally:
        if con:
            con.close()

# Declare main RSS URL
rss_url = 'http://www.elections.il.gov/rss/SBEReportsFiledWire.aspx'

# Get the raw feed and turn it into text
data = get_url_contents(rss_url)

# Split up the individual <item> XML data
data = get_items(data)

# Get report types
report_types = get_report_types(data)
print report_types

for item in data:
    test_item = split_link(item['link'])
    if str(test_item['report_type']) == 'D2Semi':
        foo = scrape_report(test_item['report_type'], test_item['link'])
        break
#test_item = split_link(data[5]['link'])
#foo = scrape_report(test_item['report_type'], test_item['link'])
print foo
#print test_item['link']

create_db()
