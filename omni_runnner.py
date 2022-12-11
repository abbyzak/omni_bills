#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import pyautogui
import time

def text_list(file_name):
    my_file = open(file_name, "r")
    content = my_file.read()
    content_list = content.split("\n")
    my_file.close()
    return list(set(content_list))[1:]
def lister(data):
    refree = []
    for i in range(len(data)):
        if data[i] != '':
            refree.append(data[i][1:15])
    return refree



ing = lister(text_list('bills.txt'))




def doit(ref):
    time.sleep(6)
    for i in range(len(ref)):
        pyautogui.typewrite(ref[i])  # useful for entering text, newline is Enter
        pyautogui.press('tab')
        pyautogui.typewrite('03122520220')  # useful for entering text, newline is Enter
        pyautogui.press('tab')


def runit(filename):
    doit(lister(text_list(filename)))




