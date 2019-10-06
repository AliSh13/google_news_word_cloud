# Cкрипт выводит облако слов по темам на google news.
  
GoogleWordCloud(topic, rus = False) 

по умолчанию задан английский язык и регион, тему нужно выбирать самомстоятельно.


ch_l = GoogleWordCloud(topic = 'Champions League')

ch_l.show_word_cloud(smax_words=50, sw = set())

по умолчанию выводит максимум - 50 слов, в аргумент sw можно добавить множество "стоп-слов".
