import json
import re
import string
import nltk
import pymorphy2
from nltk.corpus import stopwords
from telethon.sync import TelegramClient
from datetime import timedelta
from datetime import datetime

# from DB import DB
from Advanced_DB_UA import DbAdvanced


class Parser:

    def __init__(self, name='???????', api_id=????????, api_hash='??????????????????????????????'):
        self.name = name
        self.api_id = api_id
        self.api_hash = api_hash

        self.spec_chars = string.punctuation + r'\n\x0«»\t—…[]\n*'
        self.stop_words = stopwords.words('russian')
        self.morph = pymorphy2.MorphAnalyzer()

        self.db_writer = DbAdvanced()
        self.last_date = self.db_writer.last_date()

        # self.searching_period = datetime.now() - timedelta(days=100)

        self.military_chats = ['https://t.me/wargonzo', 'https://t.me/milinfolive', 'https://t.me/voenkorKotenok',
                          'https://t.me/epoddubny', 'https://t.me/voenacher', 'https://t.me/nesaharru',
                          'https://t.me/milchronicles', 'https://t.me/diselin', 'https://t.me/rusvesnasu',
                          'https://t.me/topwar_official', 'https://t.me/swodki', 'https://t.me/uniannet',
                          'https://t.me/u_now']

        #self.db_writer.db_cleaning()

    def parse(self):
        with TelegramClient(self.name, self.api_id, self.api_hash) as client:
            for index in range(len(self.military_chats)):
                for message in client.iter_messages(self.military_chats[index]):
                    if message.date.timestamp() > self.last_date:

                        text = message.text

                        if text is None:
                            continue

                        if type(text) != float:
                            text = "".join([ch for ch in text if ch not in self.spec_chars])
                            text = re.sub('\n', '     ', text)
                            tokens = nltk.word_tokenize(text)
                            filtered_text = [word.lower() for word in tokens if word.lower() not in self.stop_words]
                            final_text = []

                            for word in filtered_text:
                                if word.isalpha() and len(word) > 2:
                                    p = self.morph.parse(word)[0]
                                    final_text.append(p.normal_form)
                                else:
                                    continue

                            adv_text = json.dumps(final_text)

                            new_line = [message.id, self.military_chats[index], message.chat.title,
                                        message.date.timestamp(), message.text, adv_text]

                            self.db_writer.insert_into_db(new_line)
                    else:
                        break

# if __name__ == '__main__':
#     test = Parser()
#     test.parse()
