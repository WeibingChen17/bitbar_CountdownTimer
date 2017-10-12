#!/usr/local/bin/python3
# <bitbar.title>Countdown Timer</bitbar.title>
# <bitbar.version>v0.1</bitbar.version>
# <bitbar.author>Weibing Chen</bitbar.author>
# <bitbar.author.github>weibingchen17</bitbar.author.github>
# <bitbar.desc>A countdown timer with present and custom time.</bitbar.desc>
# <bitbar.image>http://www.hosted-somewhere/pluginimage</bitbar.image>
# <bitbar.dependencies>python3, osascript</bitbar.dependencies>
import os, sys
import datetime

def idle():
    # I don't know why print does not work here
    os.system('echo ⏲️')
    print("---")
    print(" 1 min | color=red bash=" + os.path.realpath(__file__) +  " param1=1 terminal=false")
    print(" 5 min | color=green bash=" + os.path.realpath(__file__) +  " param1=5 terminal=false")
    print("10 min | color=red bash=" + os.path.realpath(__file__) +  " param1=10 terminal=false")
    print("30 min | color=green bash=" + os.path.realpath(__file__) +  " param1=30 terminal=false")
    print("60 min | color=red bash=" + os.path.realpath(__file__) +  " param1=60 terminal=false")
    print("Custom | color=blue bash=" + os.path.realpath(__file__) +  " param1=set terminal=false")

def touch(a_file):
    with open(a_file, 'a'):
        os.utime(a_file, None)

def setATime(a_time):
    touch('/tmp/CountdownTimer.lock')
    with open('/tmp/CountdownTimer.set', 'w') as f:
        f.write(a_time)

def trigger():
    idle()
    cancel()
    for _ in range(10):
        os.system('afplay /System/Library/Sounds/Tink.aiff')

def cancel():
    idle()
    if os.path.isfile('/tmp/CountdownTimer.set'):
        os.remove('/tmp/CountdownTimer.set')

if len(sys.argv) == 1:
    if not os.path.isfile('/tmp/CountdownTimer.set'):
        idle()
    else:
        with open('/tmp/CountdownTimer.set', 'r') as f:
            setTime = int(f.read())*60
        timestamp = datetime.datetime.fromtimestamp(os.path.getmtime('/tmp/CountdownTimer.lock'))
        td = setTime - (datetime.datetime.now() - timestamp).total_seconds()
        if td < 0: 
            trigger()
        minute, second = divmod(td, 60)
        print(str(int(minute)) + ':' + '{0:02d}'.format(int(second)))
        print("---")
        print("Cancel | color=green bash=" + os.path.realpath(__file__) +  " param1=cancel terminal=false")
else:
    if sys.argv[1].isdigit():
        setATime(sys.argv[1])
    else:
        if sys.argv[1] == 'set':
            line = '''osascript -e 'Tell application "System Events" to display dialog "How many minutes to count down? " default answer ""' -e 'text returned of result' 2>/dev/null '''
            a_time = os.popen(line).read().strip()
            print(a_time)
            print(a_time.isdigit())
            print(int(a_time))
            if a_time.isdigit() and int(a_time) > 0:
                setATime(a_time)
            else:
                idle()
        elif sys.argv[1] == 'cancel':
            cancel()
