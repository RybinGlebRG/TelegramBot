import ui
import threading as th
import buffer
import logic


shared=buffer.Buffer()
lock=th.Lock()

t1=ui.UI(shared,lock)
t2=logic.Logic(shared,lock)

t1.start()
t2.start()

t1.join()
t2.join()