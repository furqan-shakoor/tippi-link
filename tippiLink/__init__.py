import requests

import base64
import re




class TippiLink:
    def __init__(self, username, password, host="192.168.0.1"):
        self._username = username
        self._password = password
        self._host = host

    def get_connected_clients(self):
        arr = self._get_array_from_page("WlanStationRpm", "hostList")
        connected_macs = arr[0::4]
        dhcp = self.get_dhcp_leases()
        connected_dhcp = filter(lambda client: client['mac_address'] in connected_macs, dhcp)
        return connected_dhcp

    def get_dhcp_leases(self):
        arr = self._get_array_from_page("AssignedIpAddrListRpm", "DHCPDynList")

        hosts = arr[0::4]
        mac_addresses = arr[1::4]
        ips = arr[2::4]
        connected_time = arr[3::4]

        connected_clients = zip(hosts, mac_addresses, ips, connected_time)

        response = [{
            "client_name": client[0],
            "mac_address": client[1],
            "ip": client[2],
            "connected_time": client[3]
        } for client in connected_clients]

        return response

    def _get_array_from_page(self, pageName, arrayName):
        headers = {
            'Referer': 'http://%s/userRpm/MenuRpm.htm' % self._host,
            'Authorization': self._auth_header(),
        }

        response = requests.get('http://%s/userRpm/%s.htm' % (self._host, pageName), headers=headers)

        content = response.content

        patt = re.compile(r".*var %s = new Array\((.*?)\).*" % arrayName, re.DOTALL)

        matches = patt.match(content)

        if matches:
            matched = matches.group(1)
        else:
            raise Exception("Could not parse response")

        arr = matched.split(",")

        arr = arr[:-2]  # Getting rid of the 0,0 in the end, I don't know why its there
        arr = map(lambda x: x.strip()[1:-1] if "\"" in x else x.strip(), arr)  # Stripping newlines and quotes

        return arr

    def _auth_header(self):
        return "Basic %s" % base64.b64encode("%s:%s" % (self._username, self._password))

if __name__ == "__main__":
    tl = TippiLink("admin", "admin")
    print tl.get_connected_clients()