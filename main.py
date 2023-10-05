from flask import Flask, render_template
import subprocess, re

app = Flask(__name__)
def get_ip():
    p = subprocess.run(["ip", "addr", "show"], capture_output=True)\
    .stdout\
    .decode()

    def verify_ip(ipaddr: str):
        exclusion = frozenset(['127.0.0.1'])
        result = subprocess.run(f'ping -c 1 -W 2 {ipaddr}'
                                .split(), capture_output=True)
        if ipaddr.strip() in exclusion: return False
        if result is not None and re.findall(r"1 received", result.stdout.decode()):
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
get_ip()
'''
ip addr show | grep -oP 'inet (?!127\.0\.0\.1)([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)' | awk '{print $2}'

'''

@app.route("/")
def hoi():
    ips = get_ip()
    if len(ips) > 0:
        return render_template('index.html', status='connected', ip=ips[0])
    else:
        return render_template('index.html', status='disconnected')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')