from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import json
import logging
import subprocess
import socket

server_ip = socket.gethostbyname(socket.gethostname())

port_number = 8088

logfile = '/var/log/dnshttp.log'

formatter = logging.Formatter(
    '%(asctime)s [%(levelname)s] %(module)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
fh = logging.FileHandler(logfile)
fh.setFormatter(formatter)
logging.getLogger().addHandler(fh)
logging.getLogger().setLevel(logging.INFO)

logger = logging.getLogger(__name__)


def shell_cmd(cmd):
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return p.returncode, out.rstrip(), err.rstrip()


class DNSArecord():
    def __init__(self):
        self.dns_file = '/etc/dnsmasq.d/hadoop'
        self.dns_records_host = {}
        self.dns_records_ip = {}
        self.get_all_dns()

    def get_all_dns(self):
        with open(self.dns_file, 'r') as f:
            content = f.readlines()
            for item in content:
                other, host, ip = item.split('/')
                ip = ip.strip()
                self.dns_records_host.update({str(host): str(ip)})
                self.dns_records_ip.update({str(ip): str(host)})
        return self.dns_records_host

    def add_host(self, record):
        host = record.get('host', None)
        ip = record.get('ip', None)
        if host is None or host in self.dns_records_host:
            return
        self.dns_records_host.update({str(host): str(ip)})
        self.dns_records_ip.update({str(ip): str(host)})

        self.write_dns_file()

    def del_host(self, record):
        host = record.get('host', None)
        ip = record.get('ip', None)
        if host is None or host not in self.dns_records_host:
            return
        self.dns_records_host.pop(str(host), None)
        self.dns_records_ip.pop(str(ip), None)

        self.write_dns_file()

    def write_dns_file(self):
        address = []
        for host, ip in self.dns_records_host.iteritems():
            address.append('address=/' + str(host) + '/' + str(ip))
        with open(self.dns_file, 'w+') as f:
            f.write('\n'.join(address))


dns_a_record = DNSArecord()


class Myhander(BaseHTTPRequestHandler):
    cmd = 'systemctl restart dnsmasq'

    def do_GET(self):
        message = {
            'code': 200,
            'message': 'thanks',
            'data': dns_a_record.get_all_dns()
        }
        self.send_header('Content-Type', 'application/json')
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps(message))
        return

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': self.headers['Content-Type'],
            })
        post_data = {}
        for field in form.keys():
            post_data.update({field: form[field].value})
        logger.info(self.client_address)
        logger.info(json.dumps(post_data))

        message = {'code': 200, 'message': 'sucess', 'data': ''}
        try:
            dns_a_record.add_host(post_data)
            returncode, out, err = shell_cmd(self.cmd)
            logger.info('{0} returncode {1} , out {2} , err {3}'.format(
                self.cmd, returncode, out, err))
        except Exception as e:
            message = {'code': 500, 'message': str(e), 'data': ''}
            logger.error(str(e))

        self.send_header('Content-Type', 'application/json')
        self.send_response(200)
        self.end_headers()
        self.wfile.write(message)
        return

    def do_DELETE(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': self.headers['Content-Type'],
            })
        post_data = {}
        for field in form.keys():
            post_data.update({field: form[field].value})
        logger.info(self.client_address)
        logger.info(json.dumps(post_data))

        message = {'code': 200, 'message': 'sucess', 'data': ''}
        try:
            dns_a_record.del_host(post_data)
            returncode, out, err = shell_cmd(self.cmd)
            logger.info('{0} returncode {1} , out {2} , err {3}'.format(
                self.cmd, returncode, out, err))
        except Exception as e:
            message = {'code': 500, 'message': str(e), 'data': ''}
            logger.error(str(e))
        self.send_header('Content-Type', 'application/json')
        self.send_response(200)
        self.end_headers()
        self.wfile.write(message)
        return


try:
    server = HTTPServer((server_ip, port_number), Myhander)
    server.serve_forever()
except Exception as e:
    logger.error(str(e))
