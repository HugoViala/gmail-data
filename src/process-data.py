import json
import operator

DATA_PATH = "../data/mails-data.json"


def print_sorted_senders(data):
    senders = {}
    for message in data:
        if "sender" in message:
            sender = message["sender"]
            if sender.find("hugo.viala") == -1:
                if sender in senders:
                    senders[sender] = senders[sender] + 1
                else:
                    senders[sender] = 1
    sorted_senders = sorted(senders.items(), key=operator.itemgetter(1))
    for (sender,count) in sorted_senders:
        print sender.encode('utf-8') + " : " + str(count).encode('utf-8')

days = ["Mon,", "Tue,", "Wed,", "Thu,", "Fri,", "Sat,", "Sun,", "Thursday,"]
        
def truncDateWithoutHours(date):
    splitted = date.split()
    joined = ""
    if splitted[0] in days:
        if len(splitted[1]) == 1:
            splitted[1] = "0" + splitted[1]
        joined = " ".join(splitted[1:4])
    else:
        if len(splitted[0]) == 1:
            splitted[0] = "0" + splitted[0]
        joined = " ".join(splitted[0:3])

    return joined

def truncDateWithoutHoursAndDay(date):
    splitted = date.split()
    joined = ""
    if splitted[0] in days:
        return " ".join(splitted[2:4])
    else:
        return " ".join(splitted[1:3])

def process_dates(data):
    f = open("../data/mails-dates-data.txt", "w")
    send = open("../data/mails-date-sent-data.txt", "w")
    received = open("../data/mails-date-received-data.txt", "w")
    datesSend = {}
    datesReceived = {}

    for message in data:
        sendMail = False
        if "sender" in message:
            if message["sender"].find("hugo.viala") != -1:
                sendMail = True
        if "date" in message:
            date = truncDateWithoutHoursAndDay(message["date"])
            if sendMail:
                if date in datesSend:
                    datesSend[date] = datesSend[date] + 1
                else:
                    datesSend[date] = 1
            else:
                if date in datesReceived:
                    datesReceived[date] = datesReceived[date] + 1
                else:
                    datesReceived[date] = 1
                


    months = ["Jan ", "Feb ", "Mar ", "Apr ", "May ", "Jun ", "Jul ", "Aug ", "Sep ", "Oct ", "Nov ", "Dec "]
    years = ["2010", "2011", "2012", "2013", "2014", "2015"]

    for y in years:
        for m in months:
            if (m + y in datesSend) or (m + y in datesReceived) :
                f.write(m + y + "\n")
                
                if m + y in datesSend:
                    send.write(str(datesSend[m + y]) + "\n")
                else:
                    send.write("0\n")

                if m + y in datesReceived:
                    received.write(str(datesReceived[m+y]) + "\n")
                else:
                    received.write("0\n")
    
    f.close()
    send.close()
    received.close()

        
def main():
    f = open(DATA_PATH, 'r')
    data = json.loads(f.read())
    f.close()
    process_dates(data)



if __name__ == "__main__":
    main()
