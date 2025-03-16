import requests
import re
from collections import Counter
import matplotlib.pyplot as plt


def map_function(text):
    words = re.findall(r'\b\w+\b', text.lower())
    return [(word, 1) for word in words]


def reduce_function(mapped_data):
    word_count = Counter()
    for word, count in mapped_data:
        word_count[word] += count
    return word_count


def visualize_top_words(word_count, top_n=10):

    top_words = word_count.most_common(top_n)
    words, counts = zip(*top_words)
    plt.figure(figsize=(10, 6))
    plt.bar(words, counts)
    plt.xlabel('Слова')
    plt.ylabel('Частота')
    plt.title(f'Топ-{top_n} слів з найвищою частотою')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

'''
тестова лінка
https://www.gutenberg.org/cache/epub/75629/pg75629-images.html
'''

if __name__ == '__main__':
    url = input("Введіть URL-адресу тексту: ")
    try:
        response = requests.get(url)
        response.raise_for_status()
        text = response.text
    except requests.RequestException as e:
        print(f"Помилка при завантаженні тексту: {e}")
        exit(1)

    mapped_data = map_function(text)
    word_count = reduce_function(mapped_data)

    visualize_top_words(word_count, top_n=10)