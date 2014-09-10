IL-Campaign-Scraper
===================

The goal of this project is to scrape campaign contributions as they arrive from the IL Board of Elections

## Current Status
### Fetching
At some point, this will need to go and fetch all old data, but 
presently, the goal is to monitor the RSS feed and collect all data from 
there.  The main feed for scraping is located at:

```
http://www.elections.il.gov/rss/SBEReportsFiledWire.aspx
```
This feed returns the most recently updated items in an XML object 
called <item>, like so:

```xml
<item>
    <title>Friends of Linda Little</title>
    <link>http://www.elections.il.gov/CampaignDisclosure/A1List.aspx?ID=541232&amp;FiledDocID=541232&amp;ContributionType=All%20Types&amp;Archived=False</link>
    <description>Friends of Linda Little A-1 ($1000+ Year Round) 
9/8/2014 3:38:53 PM - Filed electronically</description>
    <pubDate>Mon, 08 Sep 2014 15:38:53 -0500</pubDate>
    <guid>http://www.elections.il.gov/CampaignDisclosure/A1List.aspx?ID=541232&amp;FiledDocID=541232&amp;ContributionType=All%20Types&amp;Archived=False#541232</guid>
</item>
```
