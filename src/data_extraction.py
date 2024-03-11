# this is the class of the data extraction from MELI api per country and category id
# By: Cindy Zhang Gao


# libraries
import pandas as pd
import json
import requests
import urllib.request

class data_extraction:
    """
    This class contains all the methods to extract the data from the api
    Params:
        country_name (str) : the country with captalize letter
    """
    def __init__(self, country_name):
        self.country_name = country_name.capitalize()
        

    def return_site_id(self,country):
        """
        Return the id of the country of all meli country catalogues

        Params:
        --------
            country (string):
                The name of the country  interest
        Returns:
            site_dictionary id (str):
                the name id of the sitee
        """
        sites_url = "https://api.mercadolibre.com/sites"
        response = requests.get(url = sites_url)
        sites_list = response.json()

        site_dictionary = next((site for site in sites_list if site["name"] == country), None)
        if site_dictionary is None:
            raise print(f'The country {country} is not available. See available countries at https://api.mercadolibre.com/sites') # exception
        else:
            return site_dictionary['id']
        

    def return_cat_id(self,country_id):
        """
        Return the catalogue of item categories

        Params:
        --------
            country_id (string):
                The name of the site_id given by the country
        Returns:
        --------
            df_cats (pd.DataFrame)
                The dataframe with the category catalogues
        """
        try:
            cats = requests.get(f'https://api.mercadolibre.com/sites/{country_id}/categories')
            df_cats=pd.DataFrame(cats.json())
        except Exception as e:
            print(e)


        return df_cats

    def get_items_api(self,country_id,category_id,offset):
        """
        Retrieves a fraction of the listed products.

        Params
        --------
            country_id (string): 
                The ID of the country of interest.
                
            category_id (string):
                The ID of the category of interest.

            offset (integer):
                Starting point of the request.

        Returns
        ---------
            df_products (pandas.DataFrame):
                A DataFrame containing all the single-valued information for each product.
        """
        url = f'https://api.mercadolibre.com/sites/{country_id}/search?category={category_id}&offset={offset}'
        urls_request=requests.get(url).json()

        df_products=urls_request['results']

        return df_products
    

    def attributes_to_df(self,df_products,col_name):
        """
        Converts specific column with json structure to new columns

        Params:
        ----------
            df_products (pd.DataFrame):
                data frame with the resquest by the api of the products

            col_name (string):
                column name of the data frame needed to be transformed

        Returns:
        ----------
            df_joined (pd.DataFrame) data frame unida con las nuevas columnas extraidos
        """
        
        df_normalize=pd.json_normalize(df_products[col_name])
        df_normalize.rename(columns={'id':str('id_'+col_name)},inplace=True)
        df_joined=pd.concat([df_products,df_normalize],axis=1)
        df_joined.drop(col_name, axis=1, inplace=True)

        return df_joined
    
    def get_save_data(self,country_name,category_id):
        """
        Converts specific column with json structure to new columns

        Params:
        ----------
            df_products (pd.DataFrame):
                data frame with the resquest by the api of the products

            col_name (string):
                column name of the data frame needed to be transformed

        Returns:
        ----------
            df_joined (pd.DataFrame) data frame unida con las nuevas columnas extraidos
        """

        site_id=self.return_site_id(country=country_name)
        n_items=requests.get(f'https://api.mercadolibre.com/categories/{category_id}').json().get("total_items_in_this_category")
        # creamos el vector de offsets
        offset_vec = range(0, (1000 // 50) * 50 + 1, 50)
        df_products=[pd.DataFrame(self.get_items_api(country_id=site_id,category_id=category_id,offset=offset)) for offset in offset_vec]
        df_items = pd.concat(df_products, ignore_index=True)
        #extrayendo unos jsons que tienen internamente
        single_columns=['shipping','seller','attributes','installments','differential_pricing']
        #recorremos sobre las columnas que queremos que se extraigan los dictionary
        for col in single_columns:
            df_items=self.attributes_to_df(df_products=df_items,col_name=col)
        
        df_items.to_csv(f'./data/df_items_{category_id}.csv')

        return df_items
    

