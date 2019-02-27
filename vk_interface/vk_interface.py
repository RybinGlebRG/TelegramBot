import threading as th


class VK_Interface(th.Thread):

    def __init__(self, buffer, lock):
        th.Thread.__init__(self)
        self.buffer = buffer
        self.lock = lock

    def run(self):
        while True:
            self.main()

    def main(self):
        pass
