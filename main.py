import time
import telepot.telepot as tp
from telepot.telepot.loop import MessageLoop
#Fake token, change to valid one
bot = tp.Bot('463574165:AAGxdaxczz_aGDqWl6Rrn3BcglageG0_Gig')

import ai
AI = ai.AI()

def handle(msg):
    content_type, chat_type, chat_id = tp.glance(msg)
    #print(content_type, chat_type, chat_id)
    bot.sendMessage(chat_id,"LOL")
    if content_type == 'text':
        #answer=AI.answer(msg['text'])
        answer=msg['text']
        bot.sendMessage(chat_id, answer)

MessageLoop(bot,handle).run_as_thread()
#print ('Listening ...')

while(1):
    time.sleep(10)

