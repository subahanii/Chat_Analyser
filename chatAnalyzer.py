"""
Author : Ghulam Mohiyuddin
What is this: This is a whatsapp group/indivisual chat analyser
Note: This is not a final, wait for more functionality
"""

import os
import re
import pandas as pd
import matplotlib.pyplot as plt

file_path = "C:\\Users\\MEEZAN MALEK\\Desktop\\WhatsApp Chat with Takvim.txt"
array_of_path = file_path.split("\\")

# Selecting the last element of array as title and removing last 4 characters ".txt"
title = (array_of_path[-1])[:  len(array_of_path[-1]) - 4]
print(title)

cht = open(file_path, encoding="utf8")
list_of_date_time_author_msg = []
total_msg = 0
total_msg_and_notification = 0
list_of_notification = []
total_valid_msg = 0


def startsWithDate(s):
    # ReGex finding date and time
    pattern = "^([0-2][0-9]|(3)[0-1])(\/)(([0-9])|((0)[0-9])|((1)[0-2]))(\/)(\d{2}|\d{4}), ([0-9][0-9]|[0-9]):([0-9][0-9])"
    result = re.match(pattern, s)
    if result:
        return True
    return False


def findColon(s):  # to know msg is valid or not
    n = len(s)
    c = 0
    for i in range(n):
        if s[i] == ":":
            c += 1
    return c  # return no. of colons in a msg, if 0 then this msg is not a valid msg.


while 1:
    current_line = cht.readline()
    if not current_line:
        break

    total_msg_and_notification += 1
    if startsWithDate(current_line):  # To check the msg starts with date or not.

        splitLine = current_line.split("-")
        dateTime = splitLine[0]

        date, time = dateTime.split(',')
        total_msg += 1

        if findColon(splitLine[1]) > 0:  # To know this line is genuine msg or notification.
            total_valid_msg += 1
            authorMsg = splitLine[1].split(":")

            author = authorMsg[0][:15] + ".."
            msg = authorMsg[1::]

            list_of_date_time_author_msg.append([date, time, author, msg])

        else:
            list_of_notification.append(splitLine[1])
            # collect all notification such as: someone added new member,someone join this group via file_path etc.

print("\n\nTotal msg =", total_msg, "\nTotal valid msg =", total_valid_msg, "\nTotal msg and notification =",
      total_msg_and_notification)

df = pd.DataFrame(list_of_date_time_author_msg, columns=["Date", "Time", "GroupMember", "Message"])

l = dict(df['GroupMember'].value_counts())
xval = []
yval = []
for x, y in l.items():
    xval.append(x)
    yval.append(y)


def showAll():
    plt.figure(figsize=(len(l) * 0.25, 10))
    plt.bar(xval, yval, width=0.8)

    plt.title("Group: " + title)
    plt.xlabel("Group Members")
    plt.ylabel("Number of messages")
    plt.xticks(xval, rotation=90)


showAll()
c3 = 0


def autolabel(x, y):
    global c3
    for i in range(len(x)):
        plt.text(x[i], y[i] + 5, str(y[i]), ha='center', rotation=90, color='red')
        c3 += y[i]


autolabel(xval, yval)
plt.text(len(l) - len(l) // 2, len(l), 'Total Active Members: ' + str(len(l)) + ", Total Message-" + str(c3),
         color='red')

plt.show()
# plt.savefig('test.png')
