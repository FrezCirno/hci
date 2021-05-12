import win32api
import sys
import os


def play_music():
    win32api.ShellExecute(0, 'open', '8071.mp3', '', 'assets', 1)


def open_file():
    win32api.ShellExecute(0, 'open', 'notepad.exe', '', '', 1)


def search(keyword):
    win32api.ShellExecute(0, 'open', f'www.bing.com/search?q={keyword}', '', '', 1)


def open_browser():
    win32api.ShellExecute(0, 'open', 'firefox.exe', '', '', 1)


def open_wechat():
    win32api.ShellExecute(0, 'open', "C:\Program Files (x86)\Tencent\WeChat\WeChat.exe", '', '', 1)
