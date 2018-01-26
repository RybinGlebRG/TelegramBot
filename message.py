

class Message:
    # transmit/read
    type=None
    # command/text
    subtype=None
    chat_id=None
    text=None
    state=None

    def __init__(self,chat_id,text,type=None,subtype=None,state=None):
        self.chat_id=chat_id
        self.text=text
        self.type=type
        self.subtype=subtype
        self.state=state