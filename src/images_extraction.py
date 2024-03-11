# this is the class of the  images extraction from MELI api per country and category id
# By: Cindy Zhang Gao


# libraries
import pandas as pd
import json
import requests
import urllib.request
class images_extraction:
    """
    This class contains all the methods to extract the images thumbnail from the items
    Params:
        category_id (str) : the category id of the table
    """
    def __init__(self, category_id):
        self.catgory_id = category_id.capitalize()

    def get_urls_names(self,category_id):
        """
        Gets the list of the links and the item id for the naming of the image

        Params:
        ----------
            category_id (string):
                the sttring of the category to extract the images

        
        Returns:
        ----------
            list_urls(list): urls with the image
            list_ids(list): list of the ids assigned of the url's
        """
        df_items=pd.read_csv(f'./data/df_items_{category_id}.csv')
        list_urls=df_items['thumbnail']
        list_ids=df_items['id']

        return list_urls,list_ids
    
    def open_save_img(self,url_str,item_id):

        """
        This function read the images from the thumbnail image 

        Params:
        ----------
            url_str (string):
                string of the url

            item_id (string):
                id of the item for the name of the image

        Returns:
        ----------
            no returns
        """

        
        with urllib.request.urlopen(url_str) as url:
            with open(f'Images/image_{item_id}.jpg', 'wb') as f:
                f.write(url.read())

        #img = Image.open(f'Images/image_{item_id}.jpg')

