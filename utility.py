import action
import dbInteraction

class UtilityCalc:
    DB = dbInteraction.DBInteraction()
    arguments = []
    evo=None
    values = []
    actions = []

    def __init__(self,evolution):
        for i in range(0, 59, 1):
            self.arguments.append(i * (1 / 60))
        self.arguments.pop()
        self.arguments.append(1)
        self.evo=evolution

    def calcUtility(self, lst,function):
        for i in range(0,len(lst)):
            lst[i].utility=self.getUtility(lst[i].utility,function)

    def getUtility(self,utility,values):
        last=0
        next=0
        cur=0
        # Need to make it simpler !!!!!!!!!!!
        for i in range(1,len(self.arguments)-1):

            if utility==self.arguments[i]:
                last = i - 1
                next = i + 1
                cur = i
                break
            elif utility>self.arguments[i] and utility<self.arguments[i+1]:
                last = i
                next = i + 1
                cur = -1
                break
            elif utility<self.arguments[i] and utility>self.arguments[i-1]:
                last = i - 1
                next = i
                cur = -1
                break
            elif utility==self.arguments[i-1]:
                cur=i-1
                break
            elif utility==self.arguments[i+1]:
                cur=i+1
                break

        if cur!=-1:
            return values[cur]
        else:
            lval=values[last]
            nval=values[next]
            tmp=(utility-self.arguments[last])/(self.arguments[next]-self.arguments[last])
            tmp2=(nval-lval)*tmp
            return tmp2

    def addActions(self,chat_id,word,category):
        have=self.DB.getPossibleAnswers(chat_id,word[-1],category)
        max=0;
        for el in have:
            res=self.DB.getPossiblePlayerAnswers(chat_id,el,category)
            if len(res)>max:
                max=len(res)
            self.actions.append(action.Action(el[0]))
            self.actions[-1].utility=len(res)
        if max!=0:
            #Normalize values
            for i in range(0,len(self.actions)):
                self.actions[i].normalize(max)
        self.calcUtility(self.actions,self.evo.getFunction())


    def getFittest(self):
        max=0
        ind=-1
        for i in range(0, len(self.actions)):
            if self.actions[i].utility>=max:
                max=self.actions[i].utility
                ind=i

        if ind==-1:
            return None
        else:
            return self.actions[ind].element