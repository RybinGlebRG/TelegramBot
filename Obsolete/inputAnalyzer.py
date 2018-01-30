from TelegramInterface.telepot import telepot as tp


class InputAnalyzer:
    answer=None
    chats=None

    def __init__(self,answer,chats):
        self.answer=answer
        self.chats=chats

    def on_callback_query(self,msg):
        query_id, from_id, query_data = tp.glance(msg, flavor='callback_query')
        i=self.getChatIndex(from_id)
        self.chats[i].on_callback_query(msg)


    def handle(self,msg):
        content_type, chat_type, chat_id = tp.glance(msg)
        print('Chat_id:', chat_id)
        if content_type == 'text':
            self.answer(msg['text'], chat_id)

    def getChatIndex(self,chat_id):
        for i in range(0,len(self.chats)):
            if self.chats[i].chat_id==chat_id:
                return i
        return -1
