import math
import random
import time
from tkinter import *
import numpy as np
import pandas as pd
from openpyxl import Workbook
import matplotlib.pyplot as plt
import pathlib
import os

counter = 0

#action of center button
def centercd():
    global curtime
    centerbtn["state"] = DISABLED
    leftbtn["state"] = DISABLED
    rightbtn["state"] = ACTIVE
    curtime = time.time()

#action of right button
def rightcd():
    rightbtn["state"] = DISABLED
    centerbtn["state"] = DISABLED
    leftbtn["state"] = ACTIVE

#action of left button
def leftcd():
    leftbtn["state"] = DISABLED
    rightbtn["state"] = DISABLED
    centerbtn["state"] = ACTIVE
    global counter; global dist; global btnwidth; global btnheight
    global btny; global centerx; global centerwidth; global timelist
    global D; global W; global ID; global WD
    counter = counter+1
    curD = 2*dist+14
    timelist=np.append(timelist, time.time()-curtime)
    D=np.append(D, curD)
    W=np.append(W, btnwidth)
    WD=np.append(WD, btnwidth/curD)
    ID=np.append(ID, math.log(2*curD/btnwidth, 2))
    btnwidth = random.randint(10, 140)
    dist = random.randint(50, centerx-btnwidth)
    leftbtn.place(x=centerx-dist-btnwidth, y=btny, width=btnwidth, height=btnheight)
    rightbtn.place(x=centerx+dist+centerwidth, y=btny, width=btnwidth, height=btnheight)
    if counter >= 3:
        showplot.place(x=450, y=20, width=100, height=40);

def shplot():
    #save the data in excel sheet
    df = pd.DataFrame(zip(timelist, W, D, WD, ID), columns=['MT(s)','W','D', 'W/D', 'ID'])
    stpath = os.path.realpath(os.path.dirname(__file__)) + '\data.xlsx'
    with pd.ExcelWriter(stpath) as writer:  
        df.to_excel(writer, sheet_name='sheet1', index=False)
    
    fig1 = plt.figure("First Plot")
    plt.scatter(WD, ID)
    plt.title("Fitt's Experiment")
    plt.xlabel("W/D")
    plt.ylabel("ID")
    fig2 = plt.figure("Second Plot")
    plt.scatter(ID, timelist)
    plt.title("Fitt's Experiment")
    plt.xlabel("ID")
    plt.ylabel("MT (s)")
    m, b = np.polyfit(ID, timelist, 1)
    plt.plot(ID, m*ID+b)
    fig2.show()
    fig1.show()


root = Tk()
root.title("Fitt's Experiment")

outframe = Frame(root, width=1000, height=400, bg="#c4a886")
outframe.pack();

inframe = Frame(outframe, width=1000, height=200, bg="#b88d58")
inframe.pack(padx=10, pady=100)

centerwidth = 14
centerheight = 14
btnwidth = 50
btnheight = 200
centerx = 493
centery = 93
btny = 100-btnheight/2 
dist = 140

curtime = time.time()
timelist=np.array([])
D=np.array([])
W=np.array([])
WD=np.array([])
ID=np.array([])

leftbtn = Button(inframe, bg="#800000", relief="raised", activebackground="#800000", command=leftcd, state=DISABLED)
leftbtn.place(x=centerx-dist-btnwidth, y=btny, width=btnwidth, height=btnheight)

centerbtn = Button(inframe, bg="#800000", relief="raised", activebackground="#800000", command=centercd, state=ACTIVE)
centerbtn.place(x=centerx, y=centery, width=centerwidth, height=centerheight)

rightbtn = Button(inframe, bg="#800000", relief="raised", activebackground="#800000", command=rightcd, state=DISABLED)
rightbtn.place(x=centerx+dist+centerwidth, y=btny, width=btnwidth, height=btnheight)

showplot = Button(outframe, text="Show Plot", bg="#785244", activebackground="#785244", command=shplot)


root.resizable(0,0)
root.mainloop()