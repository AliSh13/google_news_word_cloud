import requests
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS

class GoogleWordCloud():
    """Создает облако по статьям в новостной ленте google по выбранной теме. """

    def __init__(self, topic, rus = False):
        self.rus = rus
        self.topic = topic

    def get_url(self):
        '''Создает urlсогласно заданным пар-ам '''
        if self.rus is False:
            url = f'https://news.google.com/search?q={self.topic}&hl=en-US&gl=US&ceid=US:en'
        else:
            url = f'https://news.google.com/search?q={self.topic}&hl=ru-RU&gl=RU&ceid=RU:ru'
        return url

    def get_words(self):
        """ Парсит все статьи за месяц и разбивает на слова """
        r = requests.get(self.get_url()).text
        soup = BeautifulSoup(r, "lxml")
        articles = soup.find_all('div',
                                {'class': 'NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc'})
        words = []
        for article in articles:
            name = article.find('h3').text
            time = article.find('time').text
            #фильтр - исключает статьи за прошлый месяц
            if time != 'Last month':
                #разбиение на слова (исключая лишние символы) и сохранение в список
                for word in name.split():
                    if self.rus is False:
                        reg = re.compile("[^a-zA-Z0-9']")
                    else:
                        reg = re.compile("[^а-яА-Я0-9']")
                    words.append(reg.sub('', word.title()))

        return ' '.join(words)


    def show_word_cloud(self, max_words=50, sw = set()):
        """Генерирует изображение облака слов """
        stopwords = set(STOPWORDS) #задает стандартный набор "стоп-слов"
        if len(sw) > 0:
            stopwords = stopwords | sw
        #Генерирует облако слов
        wordcloud = WordCloud(
            background_color = 'Black',
            stopwords=stopwords,
            max_words=max_words
        ).generate(self.get_words())

        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()

rus = GoogleWordCloud(topic='Россия', rus = True)
stopw = {"от","на", "га", "что", "из", "рассказал", "россии","как", "про", "с", "за"}
rus.show_word_cloud(max_words=50, sw = stopw)
