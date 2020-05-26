hosts_file = '/etc/hosts'
address = []
dns_f = open('/etc/dnsmasq.d/hadoop', 'w+')
with open(hosts_file, 'r') as f:
    for item in f.readlines():
        if item != '\n':
            line = item.replace('\n', '').replace('   ', ' ').replace(
                '    ', ' ').replace('  ', ' ').replace('   ', ' ')
            item = line.split(' ')
            ip = item[0]
            host = item[1]
            host2 = ''
            if len(item) > 2:
                host2 = item[2]
            address.append('address=/' + host + '/' + ip)
            if host2 != '':
                address.append('address=/' + host2 + '/' + ip)
dns_f.write('\n'.join(address))
dns_f.close()
