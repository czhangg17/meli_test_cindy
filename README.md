# Data Science Challenge

Este repositorio contiente la solución de un challege técnico para Mercado Libre, el cual demuestra un proceso end-to-end de un modelo de machine learning. La principal solución de este proyecto es poder agrupar items de diferentes categrias y poderlos agrupar

## Estructura del respositorio

El notebook principal se llama `prueba_meli.ipynb` el cual contiene el desarrollo de todos los modelos.

El módulo ``src``  pues contiene todos los códigos y clases para extracción , modelamiento y descarga de los datos. 

* `data_extraction.py`: Contiene la clase que descarga automáticamente los productos del Marketplace para cualquier país deseado y categoria. 

* `images_extraction.py`: Contiene las clase que se utliza para descargar las imagenes en formato minuatura de cada item.
  
* `preprocess_text.py`: Contiene las clase que se utliza para limpiar los títulos y devolver los tokens

La carpeta `Scripts` contiene los notebooks de, extraccion análisis exploratorio ymodelamiento. 

* `main_data_extraction_dev.ipynb`: Tiene la extracción de los datos de la api

* `prueba_meli.ipynb`: Contiene el Análisis Exploratorio de algunas variables, y un modelo LDA para los títulos.

La carpeta `data` contiene los archivos descargados para Colombia
La carpeta `images` contiene llas imagenes descargadas de los items correspondientes a la data
La carpeta `results` contiene resultados del modelo LDA



