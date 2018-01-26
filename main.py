import ui
import threading as th
import buffer
import logic


buffer=buffer.Buffer()
lock=th.Lock()

t1=ui.UI(buffer, lock)
t2=logic.Logic(buffer, lock)

t1.start()
t2.start()

t1.join()
t2.join()