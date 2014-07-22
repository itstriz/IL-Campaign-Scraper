from bs4 import BeautifulSoup
import urllib2

def get_report_type(url):
    base_url = 'http://www.elections.il.gov/CampaignDisclosure/'
    ext_start_pos = url.find('.', len(base_url))
    ext_end_pos = url.find('?', ext_start_pos)
    ext_name = url[ext_start_pos:ext_end_pos]
    report_name = url[len(base_url):ext_start_pos]

    return report_name

def get_rss_links(data):
    soup = BeautifulSoup(data)
    url_table = []
    for link in soup.find_all('link'):
        full_link = link.text
        report_name = get_report_type(full_link)

        url_table.append({'url': full_link, 'report_name': report_name})
    
    print url_table
        

def get_url_contents(url):
    response = urllib2.urlopen(url)
    html = response.read()

    return html

url = 'http://www.elections.il.gov/rss/SBEReportsFiledWire.aspx'
url_contents = get_url_contents(url)

get_rss_links(url_contents)