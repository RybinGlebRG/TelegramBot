import random


class UtilityCalc:
    arguments = []
    values = []

    def __init__(self):
        for i in range(0, 59, 1):
            self.arguments.append(i * (1 / 60))
        self.arguments.pop()
        self.arguments.append(1)
        for i in range(0, 59, 1):
            self.values.append(random.random())

    def calcUtility(self, lst):
        for i in range(0,len(lst)):
            lst[i].utility=self.getUtility(lst[i].utility)

    def getUtility(self,utility):
        last=0
        next=0
        cur=0
        for i in range(1,len(self.arguments)-1):

            if utility==self.arguments[i]:
                last = i - 1
                next = i + 1
                cur = i
                break
            if utility>self.arguments[i] and utility<self.arguments[i+1]:
                last = i
                next = i + 1
                cur = -1
                break
            if utility<self.arguments[i] and utility>self.arguments[i-1]:
                last = i - 1
                next = i
                cur = -1
                break
            if utility==self.arguments[i-1]:
                cur=i-1
                break
            if utility==self.arguments[i+1]:
                cur=i+1
                break

        if cur!=-1:
            return self.values[cur]
        else:
            lval=self.values[last]
            nval=self.values[next]
            tmp=(utility-self.arguments[last])/(self.arguments[next]-self.arguments[last])
            tmp2=(nval-lval)*tmp
            return tmp2

    def chooseFittest(self,lst):
        max=0
        ind=-1
        for i in range(0, len(lst)):
            if lst[i].utility>=max:
                max=lst[i].utility
                ind=i
        return ind