import os
import time
try:
    import foo
except :
    print "Trying to Install required module: requests\n"
    # os.system('python -m pip install requests')
    os.system('ping google.com')
    # print "###################"
    # time.sleep(20)
    # print "###################"
    # os.system('nmap')

install_requires=[
   'Flask==0.12.2',
   'Flask-WTF==0.14.2',
   'passlib==1.7.1'
]
