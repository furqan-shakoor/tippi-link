# tippi-link
A scraper for the TP-LINK router admin portal

### Installation
Use `pip install git+https://github.com/furqan-shakoor/tippi-link.git`<br/>
I haven't published it to pypi yet

### Usage
~~~
from tippiLink import TippiLink
tl = TippiLink('admin', 'password', '192.168.1.1')
output = tl.get_connected_clients()
"""
output is
[{'client_name': ‘client1’,
  'connected_time': '01:40:00’, # Time left on DHCP lease
  'ip': '192.168.1.2', 
  'mac_address': ‘AA-BC-DE-FF-DE-AD’},
 {'client_name': ‘client2’,
  'connected_time': '01:20:00’,
  'ip': '192.168.1.3’,
  'mac_address': ‘DC-AC-BC-EE-87-FE’}]
"""
~~~

### Contribution
Feel free to contribute changes as pull requests. If you run into bugs, please raise them as Github issues