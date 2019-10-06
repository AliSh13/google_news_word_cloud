import requests
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS

def get_words():
    """ Парсит все статьи за месяц и разбивает на слова """
    url = 'https://news.google.com/search?q=Russia&hl=en-US&gl=US&ceid=US%3Aen'
    r = requests.get(url).text
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
                reg = re.compile("[^a-zA-Z0-9']")
                words.append(reg.sub('', word.title()))

    return words


def show_wordcloud(data):
    """Генерирует изображение облака слов """
    stopwords = set(STOPWORDS) #задает стандартный набор "стоп-слов"
    #Генерирует облако слов
    wordcloud = WordCloud(
        background_color='Black',
        stopwords=stopwords,
        max_words=50
    ).generate(data)

    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

show_wordcloud(' '.join(get_words()))
