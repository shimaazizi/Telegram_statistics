from typing import Union
from pathlib import Path
import json
from src.data import DATA_DIR

import json
from collections import Counter
from hazm import word_tokenize, Normalizer
from wordcloud import WordCloud
import arabic_reshaper
from bidi.algorithm import get_display


class ChatStatistics:
    def __init__(self, chat_json: Union[str, Path]):

        #load chat data
        with open(chat_json) as f :
            self.chat_data = json.load(f)

        self.normalizer = Normalizer()

        #load stopwords
        stop_words = open(DATA_DIR / 'stopwords.txt').readlines()
        stop_words = list(map(str.strip, stop_words))
        self.stop_words = list(map(self.normalizer.normalize, stop_words))

    def generate_word_cloud(self, output_dir: Union[str, Path]):
        text_content = ''

        for msg in self.chat_data['messages']:
            if type(msg['text']) is str:
                tokens = word_tokenize(msg['text'])
                tokens = list(filter(lambda item: item not in self.stop_words, tokens))
                text_content += f" {' '.join(tokens)}"

        #normalize, reshape for final word cloud        
        text_content = self.normalizer.normalize(text_content)
        text_content = arabic_reshaper.reshape(text_content)
        text_content = get_display(text_content)

        wordcloud = WordCloud(
            width=1200, height=1200,
            font_path=str(DATA_DIR/ 'BHoma.ttf'),
            background_color='white'
        ).generate(text_content)

        wordcloud.to_file(str(Path(output_dir) / 'wordcloud.png'))


if __name__ == "__main__":
    chat_stats = ChatStatistics(chat_json=DATA_DIR / 'online.json')
    chat_stats.generate_word_cloud(output_dir=DATA_DIR)
    print('Done!')
