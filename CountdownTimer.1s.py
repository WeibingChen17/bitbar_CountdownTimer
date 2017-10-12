#!/usr/local/bin/python3
# <bitbar.title>Countdown Timer</bitbar.title>
# <bitbar.version>v0.1</bitbar.version>
# <bitbar.author>Weibing Chen</bitbar.author>
# <bitbar.author.github>weibingchen17</bitbar.author.github>
# <bitbar.desc>A countdown timer with present and custom time.</bitbar.desc>
# <bitbar.image>https://github.com/WeibingChen17/bitbar_CountdownTimer/blob/master/counterdownTimer.png</bitbar.image>
# <bitbar.dependencies>python3, osascript</bitbar.dependencies>
import os, sys
import datetime

def idle():
    # print has something wrong with unicode. Need fixed
    os.system('echo ⏲️')
    print("---")
    print(" 1 min | color=blue bash=" + os.path.realpath(__file__) +  " param1=1 terminal=false")
    print(" 5 min | color=green bash=" + os.path.realpath(__file__) +  " param1=5 terminal=false")
    print("10 min | color=blue bash=" + os.path.realpath(__file__) +  " param1=10 terminal=false")
    print("30 min | color=green bash=" + os.path.realpath(__file__) +  " param1=30 terminal=false")
    print("60 min | color=blue bash=" + os.path.realpath(__file__) +  " param1=60 terminal=false")
    print("Custom | color=red bash=" + os.path.realpath(__file__) +  " param1=set terminal=false")

def touch(a_file):
    with open(a_file, 'a'):
        os.utime(a_file, None)

def setATime(a_time):
    touch(lockFile)
    with open(setFile, 'w') as f:
        f.write(a_time)

def cancel():
    idle()
    if os.path.isfile(setFile):
        os.remove(setFile)

def alert():
    cancel()
    for _ in range(10):
        os.system('afplay /System/Library/Sounds/Tink.aiff')

lockFile = '/tmp/CountdownTimer.lock'
setFile = '/tmp/CountdownTimer.set'

if len(sys.argv) == 1:
    if not os.path.isfile(setFile):
        idle()
    else:
        with open(setFile, 'r') as f:
            setTime = int(f.read()) 
        timestamp = datetime.datetime.fromtimestamp(os.path.getmtime(lockFile))
        td = setTime - (datetime.datetime.now() - timestamp).total_seconds()
        if td <= 0: 
            alert()
        else:
            minute, second = divmod(td, 60)
            if minute < 60:
                print(str(int(minute)) + ':' + '{0:02d}'.format(int(second)))
            else:
                hour, minute = divmod(minute, 60)
                print(str(int(hour)) + ':' + '{0:02d}'.format(int(minute)) + ':' + '{0:02d}'.format(int(second)))
            print("---")
            print("Cancel | color=red bash=" + os.path.realpath(__file__) +  " param1=cancel terminal=false")
else:
    if sys.argv[1].isdigit():
        setATime(str(int(sys.argv[1]) * 60))
    else:
        if sys.argv[1] == 'cancel':
            cancel()
        elif sys.argv[1] == 'set':
            line = '''osascript -e 'Tell application "System Events" to display dialog "How many minutes to count down? or [hh:]mm:ss " default answer ""' -e 'text returned of result' 2>/dev/null '''
            a_time = os.popen(line).read().strip()
            if ':' not in a_time:
                if a_time.isdigit() and int(a_time) > 0:
                    setATime(a_time)
            else:
                try: 
                    hms = [int(i) for i in a_time.split(':')]
                    if len(hms) == 2 and 0 <= hms[0] < 60 and 0 <= hms[1] < 60:
                        setATime(str(hms[0] * 60 + hms[1]))
                    if len(hms) == 3 and 0 <= hms[1] < 60 and 0 <= hms[2] < 60:
                        setATime(str(hms[0] * 60 * 60 + hms[1] * 60  + hms[2]))
                except:
                    pass
