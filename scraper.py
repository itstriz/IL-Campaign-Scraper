from bs4 import BeautifulSoup
import urllib2

def get_subitems(url):
    """ Take url and get all subitems """
    subitem_list = []
    start_pos = url.find('?')
    end_pos = url.find('=', start_pos)
    while end_pos <> -1:
        subitem_list.append(url[start_pos+1:end_pos])
        start_pos = url.find('&', end_pos)
        end_pos = url.find('=', end_pos+1)
    
    print subitem_list

def get_report_id(url):
    """ Take url address from RSS feed and return report ID"""
    start_pos = url.lower().find('?id=')
    end_pos = url.lower().find('&', start_pos)
    report_id = url[start_pos+4:end_pos]

    return report_id

def get_report_type(url):
    """ Take url address from RSS feed and return report name"""
    base_url = 'http://www.elections.il.gov/CampaignDisclosure/'
    ext_start_pos = url.find('.', len(base_url))
    ext_end_pos = url.find('?', ext_start_pos)
    ext_name = url[ext_start_pos:ext_end_pos]
    report_name = url[len(base_url):ext_start_pos]

    return report_name

def get_rss_links(data):
    """ Take RSS Feed URL and return a list of all links, other info """
    soup = BeautifulSoup(data)
    url_table = []
    for link in soup.find_all('link'):
        full_link = link.text
        report_name = get_report_type(full_link)
        report_info = {}
        report_info['url'] = full_link
        report_info['report_name'] = report_name
        
        report_id = get_report_id(full_link)
        report_info['id'] = report_id

        get_subitems(full_link)

        url_table.append(report_info)
    
    #print url_table
        
def get_url_contents(url):
    """ Pull contents out of an url """
    response = urllib2.urlopen(url)
    html = response.read()

    return html

""" Main function - update docstring as this changes """
url = 'http://www.elections.il.gov/rss/SBEReportsFiledWire.aspx'
url_contents = get_url_contents(url)

get_rss_links(url_contents)
