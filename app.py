import pandas as pd
import time
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

turnAroundTimes = {}
responseTimes = {}


class Process:
    def __init__(self, pid, arrivalTime, burstTime, waitingTime):
        self.pid = pid
        self.arrivalTime = arrivalTime
        self.burstTime = burstTime
        self.waitingTime = waitingTime

    def getPID(self):
        return self.pid

    def getArrivalTime(self):
        return self.arrivalTime

    def decreaseTime(self, num):
        self.burstTime = self.burstTime - num

    def getBurstTime(self):
        return self.burstTime

    def clrBurst(self):
        self.burstTime = 0

    def clrWait(self):
        self.waitingTime = 0

    def increaseWaitTime(self, n):
        self.waitingTime = self.waitingTime + n

    def getWaitTime(self):
        return self.waitingTime


class Queue:
    def __init__(self):
        self.processes = []
        self.end = 0
        self.start = 0

    def enqueue(self, process):
        self.processes.append(process)
        self.end = self.end + 1
        process.clrWait()

    def dequeue(self):
        if (self.end == 0 and self.start == 0):
            return None
        rProcess = self.processes[self.start]
        self.start = self.start + 1
        if (self.start == self.end):
            self.start = 0
            self.end = 0
            self.processes = []
        return rProcess

    def increaseWait(self, n, process):
        for i in range(self.start, self.end):
            p = self.processes[i]
            if process.getPID() != p.getPID():
                p.increaseWaitTime(n)

    def size(self):
        return self.end - self.start

    def getShortest(self):
        short = self.processes[0]
        newQueue = []
        for i in range(self.start, self.end):
            if self.processes[i].getBurstTime() < short.getBurstTime():
                short = self.processes[i]
        for p in self.processes:
            if p.getPID() != short.getPID():
                newQueue.append(p)
        self.start = 0
        self.end = len(newQueue)
        self.processes = newQueue
        return short

    def getWaitTimeList(self, n):
        resProcess = []
        newQueue = []
        for i in range(self.start, self.end):
            if (self.processes[i].getWaitTime() >= n):
                resProcess.append(self.processes[i])
            else:
                newQueue.append(self.processes[i])
        self.start = 0
        self.end = len(newQueue)
        self.processes = newQueue
        return resProcess

    def printQueue(self):
        for i in range(self.start, self.end):
            print("|" + str(self.processes[i].getPID()) + "| ", end="")
        print()


q0 = Queue()
q1 = Queue()
q2 = Queue()
print("Enter name of the input file: ")
fileName = input()
df = pd.read_csv(fileName, delim_whitespace=True)
if(len(df)>10):
    print("This execution doesn't support more than 10 processess if you want more than 10 processes kindly update color array and add more colors than 10 and delete this check")
    exit(0)
processList = []
length = []
curr = 0
waitingTimes = {}


def increaseWaitWhole(n, p):
    for key, value in waitingTimes.items():
        if (key != p.getPID()):
            waitingTimes[key] += n


def round_robin(quantum, q):
    global curr
    length.append(curr)
    proc = q.dequeue()
    proc.clrWait()
    processList.append((proc.getPID()))
    q.increaseWait(quantum, proc)
    startTime = time.time_ns() // 1000000
    while (time.time_ns() // 1000000 - startTime <= quantum):
        doNothing = 0
    if (proc.getBurstTime() - quantum < 0):
        curr += proc.getBurstTime()
        proc.clrBurst()
        increaseWaitWhole(proc.getBurstTime(), proc)
        turnAroundTimes[proc.getPID()] = curr - proc.getArrivalTime()
    else:
        proc.decreaseTime(quantum)
        increaseWaitWhole(quantum, proc)
        curr += quantum
    if proc.getPID() not in responseTimes.keys():
        responseTimes[proc.getPID()] = curr
    length.append(curr)
    processList.append((proc.getPID()))
    return proc


def srtf(q):
    global curr
    p = q.getShortest()
    length.append(curr)
    startTime = time.time_ns() // 1000000
    processList.append((p.getPID()))
    while (time.time_ns() // 1000000 - startTime <= 500):
        doNothing = 0
    q.increaseWait(p.getBurstTime(), p)
    curr += p.getBurstTime()
    length.append(curr)
    processList.append((p.getPID()))
    increaseWaitWhole(p.getBurstTime(), p)
    turnAroundTimes[p.getPID()] = curr - p.getArrivalTime()


def printQueue():
    print("********************************************")
    print("Queue 0:", end="")
    q0.printQueue()
    print("Queue 1:", end="")
    q1.printQueue()
    print("Queue 2:", end="")
    q2.printQueue()


printQueue()


def updateWaitingScheme():
    waitIncList = q1.getWaitTimeList(200)
    for p in waitIncList:
        q0.enqueue(p)
    waitIncList = q2.getWaitTimeList(300)
    for p in waitIncList:
        q1.enqueue(p)


def addDataToQueue():
    global df
    for i in range(len(df)):
        pro = Process(int(df["pid"].iloc[0]), int(df["arrival_time"].iloc[0]), int(df["burst_time"].iloc[0]), 0)
        if (pro.getArrivalTime() <= curr):
            df = df.iloc[1:]
            waitingTimes[pro.getPID()] = 0
            q0.enqueue(pro)


while q0.size() != 0 or q1.size() != 0 or q2.size() != 0 or len(df) != 0:
    startCurr = curr
    addDataToQueue()
    while (q0.size() != 0):
        printQueue()
        p = round_robin(50, q0)
        addDataToQueue()
        if (p.getBurstTime() != 0):
            q1.enqueue(p)
        updateWaitingScheme()
        printQueue()
    while q1.size() != 0 and q0.size() == 0:
        p = round_robin(100, q1)
        addDataToQueue()
        if (p.getBurstTime() != 0):
            q2.enqueue(p)
        updateWaitingScheme()
        printQueue()

    while q2.size() != 0 and q1.size() == 0 and q0.size() == 0:
        srtf(q2)
        addDataToQueue()
        updateWaitingScheme()
        printQueue()
    if (startCurr == curr):
        curr += 1

print("********************************************")
print("Waiting Time of All Processes")
print("********************************************")
for key, value in waitingTimes.items():
    print("PID", key, "waiting time was", value)

print()
print("********************************************")
print("Turn Around Time of All Processes")
print("********************************************")
for key, value in turnAroundTimes.items():
    print("PID", key, "turn around time was", value)

print()
print("********************************************")

avgResTime = 0.0
for key, value in responseTimes.items():
    avgResTime = avgResTime + value
avgResTime = avgResTime / len(responseTimes)
print("Average Response time: ", avgResTime)

avgTurnAroundTime = 0.0
for key, value in turnAroundTimes.items():
    avgTurnAroundTime = avgTurnAroundTime + value
avgTurnAroundTime = avgTurnAroundTime / len(responseTimes)
print("Average Turn Around time: ", avgTurnAroundTime)
print("********************************************")

procDfList = [dict(Task="PID: " + str(processList[0]), Start='0', Finish=length[0])]

for i in range(1, len(processList)):
    procDfList.append(dict(Task="PID: " + str(processList[i]), Start=length[i - 1], Finish=length[i]))

df = pd.DataFrame(procDfList)
col = mcolors.TABLEAU_COLORS
#Update color pallete here
color = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
plt.hlines(1, length[0], length[1], colors=color[processList[0]%10], lw=30)
plt.text((length[0] + length[1])/ 2, 1.01, str(processList[0]), ha='center')


for i in range(2, len(length),2):
    plt.hlines(1, length[i], length[i+1], label=str(processList[i]), colors=color[processList[i]%10], lw=30)
    plt.text((length[i] + length[i+1]) / 2, 1.01, str(processList[i]), ha='center')

plt.tight_layout()
plt.show()
