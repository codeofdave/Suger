from flask import Flask, render_template, redirect, request, url_for
from fabric import *
import time,os
app = Flask(__name__)
data = {'hosts': '192.168.78.134-192.168.78.135,192.168.1.1',
        'ips':['192.168.78.134','192.168.78.135','192.168.1.1'],
        'output':'',
        'cmd':'pwd',
        'passwd1':'fc2:IaaS@OS-CLOUD9!',
        'passwd2':'root:IaaS@OS-CLOUD8!',}

def log(msg):
    fp = open('./static/cmd.log','a')
    fp.write(msg)
    fp.close()

def getlog():
    try:
        fp = open('./static/cmd.log', 'r')
        log=fp.read()
        fp.close()
        return log
    except:
        print('get log error')


def execmd():
    if len(data['output']) > 10240:
        log(data['output'])
        data['output'] = ''


    c = Connection(host=data['ips'][0],user='root',connect_kwargs={'password':'Huawei@123'})
    result = c.run(data['cmd'])
    msg = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+\
          " Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
    data['output'] = msg.format(result)+'\n'+data['output']




def trans2ip(hosts):
    iplist=[]
    try:
        for ips in hosts.split(','):
            if not '-' in ips:
                iplist.append(ips)
            else:
                ipstart = ips.split('-')[0]
                ipend = ips.split('-')[1]
                prefix = ''
                for x in range(0,3):
                    prefix += (ipstart.split('.')[x] + '.')
                i,j=int(ipstart.split('.')[-1]),int(ipend.split('.')[-1])
                for x in range(i,j+1):
                    iplist.append(prefix+str(x))
    except:
        print("Input error")
    return iplist


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showlog')
def showlog():
    return render_template('log.html',data=getlog())



@app.route('/ssh', methods=['POST', 'GET'])
def ssh():
    if request.method == 'POST' and request.values['key'] == 'updateIp':
        print('updateIp')
        data['hosts'] = request.values['hosts']
        data['ips'] = trans2ip(data['hosts'])
    if request.method == 'POST' and request.values['key'] == 'changePasswd':
        print('changePasswd')
        data['passwd1'] = request.values['passwd1']
        data['passwd2'] = request.values['passwd2']
    if request.method == 'POST' and request.values['key'] == 'execmd':
        print('execmd')
        data['cmd'] = request.values['cmd']
        execmd()
    if request.method == 'POST'and request.values['key'] == 'showlog':
        print('hello')
        return redirect(Response=getlog())
    return render_template('ssh.html', data=data)


if __name__ == '__main__':

    app.run()