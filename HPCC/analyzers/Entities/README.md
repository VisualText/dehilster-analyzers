# Entity Analyzer for Department of Justice Indictment Press Releases

This is an analyzer that extracts people from the Department of Justice press releases that contain the keyword "indictment".

The webpage is found at: [https://www.justice.gov/news](https://www.justice.gov/news?search_api_fulltext=%20indictment&start_date=&end_date=&sort_by=field_date)

There python script [DOJArticles.py](https://github.com/VisualText/dehilster-analyzers/blob/main/HPCC/analyzers/Entities/input/DOJArticles.py) grabs press releases from the DOJ's new webpages on and creates an XML file of each article with it's title, url, and text.