import requests

import base64
import re




class TippiLink:
    def __init__(self, username, password, host="192.168.0.1"):
        self.username = username
        self.password = password
        self.host = host

    def get_connected_clients(self):
        headers = {
            'Referer': 'http://%s/userRpm/MenuRpm.htm' % self.host,
            'Authorization': self._auth_header(),
        }

        response = requests.get('http://%s/userRpm/AssignedIpAddrListRpm.htm' % self.host, headers=headers)

        content = response.content

        patt = re.compile(r".*var DHCPDynList = new Array\((.*?)\).*", re.DOTALL)

        matches = patt.match(content)

        if matches:
            matched = matches.group(1)
        else:
            raise Exception("Could not parse response")

        arr = matched.split(",")

        arr = arr[:-2]  # Getting rid of the 0,0 in the end, I don't know why its there
        arr = map(lambda x: x.strip()[1:-1], arr) # Stripping newlines and quotes

        hosts = arr[0::4]
        mac_addresses = arr[1::4]
        ips = arr[2::4]
        connected_time = arr[3::4]

        connected_clients = zip(hosts, mac_addresses, ips, connected_time)

        response = [{
            "host": client[0],
            "mac_address": client[1],
            "ip": client[2],
            "connected_time": client[3]
        } for client in connected_clients]

        return response

    def _auth_header(self):
        return "Basic %s" % base64.b64encode("%s:%s" % (self.username, self.password))

if __name__ == "__main__":
    tl = TippiLink("admin", "admin")
    tl.get_connected_clients()