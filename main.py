
api_keys = {'flickr': ('24c5ab910f81210e9d70652814f367da', 'd52bd1a9550316d2')}
images_nbr = 40                     # number of images to fetch
download_folder = "./data"          # folder in which the images will be stored

'''
from web_crawler import WebCrawler
crawler = WebCrawler(api_keys)

# 1. Crawl the web and collect URLs:
crawler.collect_links_from_web(images_nbr, remove_duplicated_links=True)

# 2. Save URLs to download them later (optional):
crawler.save_urls(download_folder + "/links.txt")

#  (alernative to the previous line) Load URLs from a file instead of the web:
#crawler.load_urls(download_folder + "/links.txt")

# 3. Download the images:
crawler.download_images(target_folder=download_folder)

'''
#-------------------------------------------------------------

from web_crawler_keyword import WebCrawler
crawler = WebCrawler(api_keys)

keywords = ["animals", "birds", "people","celebration","flowers","children","park","Family","Community","sea","friends","party"]

# 1. Crawl the web and collect URLs:
crawler.collect_links_from_web(keywords, images_nbr, remove_duplicated_links=True)

# 2. Save URLs to download them later (optional):
crawler.save_urls(download_folder + "/links.txt")

#  (alernative to the previous line) Load URLs from a file instead of the web:
#crawler.load_urls(download_folder + "/links.txt")

# 3. Download the images:
crawler.download_images(target_folder=download_folder)
