import time
import telepot.telepot as tp
from telepot.telepot.loop import MessageLoop
bot = tp.Bot('463574165:AAHCrL8DnLIJs85koM6zKsVCOsF0Gxjl2yc')
#response = bot.getUpdates()


def handle(msg):
    content_type, chat_type, chat_id = tp.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        bot.sendMessage(chat_id, msg['text'])

MessageLoop(bot,handle).run_as_thread()
print ('Listening ...')

while(1):
    time.sleep(10)

