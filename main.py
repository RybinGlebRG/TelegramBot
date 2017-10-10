import time
import telepot.telepot as tp
from telepot.telepot.loop import MessageLoop
#Fake token, change valid token
bot = tp.Bot('463574165:AAFlC-rq_t5gfvokF9s5-TZOFDT-JLXAktA')

import ai
AI=ai.AI()

def handle(msg):
    content_type, chat_type, chat_id = tp.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        answer=AI.answer(msg['text'])
        #answer="lol"
        bot.sendMessage(chat_id, answer)

MessageLoop(bot,handle).run_as_thread()
print ('Listening ...')

while(1):
    time.sleep(10)

