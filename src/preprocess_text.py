# this is the class of fro cleanning and preprocess text for analysis of LDA
# By: Cindy Zhang Gao

import pandas as pd
from nltk.corpus import stopwords
import re
from nltk.tokenize import word_tokenize
import string
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class preprocess_text:

    """
    This class contains functions for cleanning the text, graphic and lda moedlling
    Params:
        
    """
    def __init__(self):
        pass


    def clean_text(titles:list):
        # Obtener las stopwords en español
        spanish_stopwords = stopwords.words('spanish')
        manual_stop_words=['unidad','unidades','x2','x3','x','color','negro','blanco','azul','ml','kg','lb','gr','mg','mm','und','bicicleta','shimano']
        spanish_stopwords=spanish_stopwords+manual_stop_words

        # Concatenar todos los títulos en una sola cadena de texto
        text = ' '.join(titles)

        # Convertir el texto a minúsculas
        text = text.lower()
        #eliminando numeros 
        text = re.sub(r'\d+', '', text)
        # Eliminar signos de puntuación
        text = text.translate(str.maketrans('', '', string.punctuation))


        # Tokenizar el texto en palabras
        words = word_tokenize(text)

        # Eliminar signos de puntuación y palabras vacías
        cleaned_words = [word for word in words if len(word) > 1 and word not in spanish_stopwords]

        # Unir las palabras limpias en una cadena de texto nuevamente
        cleaned_text = ' '.join(cleaned_words)

        return cleaned_text


    def generate_wordcloud(cleaned_text):
        # Crear el objeto WordCloud
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(cleaned_text)

        # Graficar la nube de palabras
        plt.figure(figsize=(8, 4))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')  # Desactivar ejes
        plt.title('Nube de palabras de los títulos')

        return plt.show()


    def format_topics_sentences(ldamodel=None, corpus=None, texts=None):
        # Init output
        sent_topics_df = pd.DataFrame()

        # Get main topic in each document
        for i, row_list in enumerate(ldamodel[corpus]):
            row = row_list[0] if ldamodel.per_word_topics else row_list            
            # print(row)
            row = sorted(row, key=lambda x: (x[1]), reverse=True)
            # Get the Dominant topic, Perc Contribution and Keywords for each document
            for j, (topic_num, prop_topic) in enumerate(row):
                if j == 0:  # => dominant topic
                    wp = ldamodel.show_topic(topic_num)
                    topic_keywords = ", ".join([word for word, prop in wp])
                    sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
                else:
                    break
        sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

        # Add original text to the end of the output
        contents = pd.Series(texts)
        sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
        return(sent_topics_df)


