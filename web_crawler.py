""" WebCrawler: fetch images from various search engines and download them"""

from __future__ import print_function
from math import ceil
import sys
import os
import json
import images_downloader
from cffi.api import basestring
import random


class WebCrawler(object):
    """ Fetch images from various search engines and download them"""
    api_keys = []
    images_links = []
    keywords = ''

    def __init__(self, api_keys):
        self.api_keys = api_keys

    @staticmethod
    def error(msg):
        """Display an error message and exit"""
        print("Error: ", msg)
        exit()

    def collect_links_from_web(self, number_links_per_engine, remove_duplicated_links=False):
        # validate params:
        number_links = int(number_links_per_engine)
        if number_links <= 0:
            print("Warning: number_links_per_engine must be positive, value changed to default (100 links)")
            number_links = 100

        # call methods for fetching image links in the selected search engines:
        print("Start fetching...")
        extracted_links = []
        for engine, keys in self.api_keys.items():
            try:
                method = getattr(self, 'fetch_from_' + engine)
            except AttributeError:
                self.error('funciton fetch_from_' + engine + '() not defined')
            temporary_links = method(keys[0], keys[1], number_links)
            extracted_links += temporary_links
            print("\r >> ", len(temporary_links), " links extracted", end="\n")

        # remove duplicated links:
        if remove_duplicated_links:
            links_count = len(extracted_links)
            extracted_links = list(set(extracted_links))
            print(" >> ", links_count - len(extracted_links),
                " duplicated links removed, ", len(extracted_links), " kept")

        # store the links into the global list:
        self.images_links = extracted_links


    def fetch_from_flickr(self,api_key, api_secret, number_links=50):
        """ Fetch random images from Flikr """
        from flickrapi import FlickrAPI 
        
        random.seed()
        rand_page = random.randint(1,50)   #4000 pages 
    
        # calculate number of pages:
        if number_links < 30:
            items_per_page = number_links
        else:
            items_per_page = 30   # max 200 for flikr
        pages_nbr = int(ceil(number_links / items_per_page))
        links = []

        # get links from the random page:
        print("Carwling Flickr Search...")
        flickr = FlickrAPI(api_key, api_secret)
        response = flickr.photos_search(api_key=api_key,
                                        page=rand_page,
                                        per_page=items_per_page,
                                        media='photos',
                                        sort='relevance')
        images = [im for im in list(response.iter()) if im.tag == 'photo']
        for photo in images:
            photo_url = "https://farm{0}.staticflickr.com/{1}/{2}_{3}.jpg". format(
                photo.get('farm'), photo.get('server'), photo.get('id'), photo.get('secret'))
            links.append(photo_url)
        print(" >> ", len(links), " links extracted...", end="")

        # get next pages:
        for i in range(1, pages_nbr):
            response = flickr.photos_search(api_key=api_key,
                                            page=rand_page+1,
                                            per_page=items_per_page,
                                            media='photos',  
                                            sort='relevance')
            images = [im for im in list(response.iter()) if im.tag == 'photo']
            for photo in images:
                link = "https://farm{0}.staticflickr.com/{1}/{2}_{3}.jpg". format(
                    photo.get('farm'), photo.get('server'), photo.get('id'), photo.get('secret'))
                links.append(link)
            print("\r >> ", len(links), " links extracted...", end="")

        # store and reduce the number of images if too much:
        return links


    def save_urls(self, filename):
        """ Save links to disk """
        folder, _ = os.path.split(filename)
        if filename and not os.path.exists(folder):
            os.makedirs(folder)
        with open(filename, 'w') as links_file:
            for link in self.images_links:
                links_file.write(link + '\n')
        print("\nLinks saved to '", filename, "'")

    def load_urls(self, filename):
        """ Load links from a file"""
        if not os.path.isfile(filename):
            self.error("Failed to load URLs, file '" + filename + "' does not exist")
        with open(filename) as links_file:
            self.images_links= []
            for link in links_file:
                self.images_links.append(link)
        print("\nLinks loaded from ", filename)

    def download_images(self, target_folder='./data'):
        """ Download images and store them in the specified folder """
        print(" ")
        downloader = images_downloader.ImagesDownloader()
        if not target_folder:
            target_folder = './data'
        downloader.download(self.images_links, target_folder)