#!/usr/bin/python3
from flask import Flask, render_template
import subprocess
import re
import os
def is_raspberry() -> bool:
    return True if os.name == 'posix'\
        and 'Raspberry' in execute_command("cat /proc/cpuinfo") else\
            False
def execute_command(cmd: str) -> str:
    if os.name == 'nt':
        return subprocess.run(['C:\Windows\System32\WindowsPowerShell\\v1.0\powershell.exe', '-Command', cmd],
                              capture_output=True)\
                                  .stdout\
                                      .decode()\
                                          .strip()
    return subprocess.run(cmd, shell=True, capture_output=True).stdout.decode().strip()

app = Flask(__name__)
def get_ip() -> tuple:
    if os.name == 'nt':
        return (execute_command("(Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias (Get-NetAdapter | Where-Object {$_.Status -eq 'Up'} | Select-Object -First 1).Name).IPAddress"),)
        
    p = execute_command("ip addr show")
    def verify_ip(ipaddr: str):
        exclusion = frozenset(['127.0.0.1'])
        result = execute_command(f'ping -c 1 -W 2 {ipaddr}')
        if ipaddr in exclusion:
            return False
        if result is not None and re.findall(r"1 received", result):
            #TODO: Change received = 1 to 1 received
            return True
        return False
    matches = tuple(filter(verify_ip,
                            re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', p)))
    '''
    Difficult regex 
    '''
    if matches:
        return matches
    return tuple()


@app.route("/")
def hoi():
    ips = get_ip()
    if len(ips) > 0:
        if os.name != 'nt':
            return render_template('index.html', status='connected', ip=ips[0],
                                ssid=execute_command('iwgetid -r'),
                                raspberry=is_raspberry(),
                                os_=os.name)
        else:
            SSID = execute_command('(get-netconnectionProfile).Name')\
                .split('\n')
            return render_template('index.html', status='connected',
                                   ip=ips[0],
                                   ssid=SSID[0],
                                   raspberry=False,
                                   os_=os.name)
    else:
        return render_template('index.html', status='disconnected')


if __name__ == '__main__':
    print("TEST SERVER GESTART, RUN een van de setup-and-run scripts voor productie.")
    app.run(debug=True, host='127.0.0.1', port=9090)
    # specifiek voor poort 9090 gekozen want port 80 heeft sudo nodig.
