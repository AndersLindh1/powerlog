#!/usr/bin/env python3
# Anders Lindh
# 2022-01-28
# logscript to check for downtime
# check every minute (cron start the script)
# read last log entry
# if time since last entry > 1 minute make a log entry in another logfile containing down and uptime

import datetime
import os

def getTime():
	return datetime.datetime.now()

def convTimeToStr(time):
	return time.strftime("%Y-%m-%d %H:%M")

def convTimeToObj(time):
	return datetime.datetime.strptime(time, "%Y-%m-%d %H:%M")

def writeFile(text, file_name):
	with open(os.path.expanduser(file_name), 'w') as file:
		file.write(text + "\n")

def writeFileAdd(text, file_name):
	with open(os.path.expanduser(file_name), 'a') as file:
		file.write(text + "\n")

def checkExists():
	if not (os.path.exists(os.path.expanduser('~/Python/poweronlog/powerlog.txt'))):
		if not (os.path.exists(os.path.expanduser('~/Python/powerlog'))):
			if not (os.path.exists(os.path.expanduser('~/Python'))):
				os.mkdir(os.path.expanduser('~/Python'))
			os.mkdir(os.path.expanduser('~/Python/powerlog'))
		writeFile(convTimeToStr(getTime()), '~/Python/poweronlog/powerlog.txt')

def readTime():
	checkExists()
	with open(os.path.expanduser('~/Python/poweronlog/powerlog.txt'), 'r') as file:
		last = file.readlines()[-1]
	return last.rstrip()

def checkDiff():
	current = getTime()
	last = convTimeToObj(readTime())
	diff = (current - last)
	if diff.seconds >= 90:
		print("log power shortage")
		text = "Power lost from " + convTimeToStr(last) + " to " + convTimeToStr(current) + ". Total time down: " + str(int((diff.seconds//60))) + " minutes."
		writeFileAdd(text, '~/Python/poweronlog/powerofflog.txt')

checkDiff()
writeFile(convTimeToStr(getTime()), '~/Python/poweronlog/powerlog.txt')
