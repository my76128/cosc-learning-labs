# Copyright 2014 Cisco Systems, Inc.
# 
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from collections import namedtuple
try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus

from lxml import etree

from basics.odl_http import odl_http_get
from basics.html import html_bind

_url_template = 'operational/opendaylight-inventory:nodes/node/%s/yang-ext:mount/Cisco-IOS-XR-ifmgr-oper:interface-properties/data-nodes/data-node/0%%2F0%%2FCPU0/system-view/interfaces/interface/%s'

InterfaceProperties = namedtuple('InterfaceProperties', [
    'name',
    'type',
    'bandwidth',
    'encapsulation',
    'encapsulationType',
    'state',  # physical state
    'lineState',  # layer 2 state
    'actualState',
    'actualLineState',
    'l2Transport',
    'mtu',
    'subInterfaceMtuOverhead'])

_interface_properties_html_template = '''
<table border="1">
<thead>
<tr>
<th style="text-align: left">Name</th>
<th style="text-align: center">Type</th>
<th style="text-align: right">Bandwidth</th>
<th style="text-align: center" colspan="2">Encapsulation</th>
<th style="text-align: center">L2 Transport</th>
</tr>
</thead>
<tbody>
%s
</tbody>
</table>
<p/>
<table border="1">
<thead><tr>
<th style="text-align: left">Name</th>
<th style="text-align: center">State</th>
<th style="text-align: center">Line State</th>
<th style="text-align: center">Actual State</th>
<th style="text-align: center">Actual Line State</th>
<th style="text-align: right">MTU</th>
</tr></thead>
<tbody>
%s
</tbody>
</table>
'''

_interface_properties_html_table1_row_template = '''
<tr>
<td style="text-align: left">%s</td>
<td style="text-align: left">%s</td>
<td style="text-align: center">%s</td>
<td style="text-align: center">%s</td>
<td style="text-align: center">%s</td>
<td style="text-align: center">%s</td>
</tr>
'''

_interface_properties_html_table2_row_template = '''
<tr>
<td style="text-align: left">%s</td>
<td style="text-align: center">%s</td>
<td style="text-align: center">%s</td>
<td style="text-align: center">%s</td>
<td style="text-align: center">%s</td>
<td style="text-align: right">%s</td>
</tr>
'''

def interface_properties_as_html(*args):
    table1_rows = [_interface_properties_html_table1_row_template % (ip.name, ip.type, str(ip.bandwidth), ip.encapsulation, ip.encapsulationType, ip.l2Transport) for ip in args]
    table2_rows = [_interface_properties_html_table2_row_template % (ip.name, ip.state, ip.lineState, ip.actualState, ip.actualLineState, str(ip.mtu)) for ip in args]
    return _interface_properties_html_template % ('\n'.join(table1_rows), '\n'.join(table2_rows))
#     return '<p>here it comes</p>' 

def print_html_interface_properties(*args):
    print(interface_properties_as_html(*args))
    
html_bind(InterfaceProperties, print_html_interface_properties)

def interface_properties(
    device_name,
    interface_name
):
    'Return a named tuple containing the information available for the specified interface of the specified, mounted device.'
    url = _url_template % (device_name, quote_plus(interface_name))
    response = odl_http_get(url, 'application/xml')
    tree = etree.parse(StringIO(response.text))
    return InterfaceProperties(
        name=tree.findtext('{*}interface-name'),
        type=tree.findtext('{*}type'),
        bandwidth=tree.findtext('{*}bandwidth'),
        encapsulation=tree.findtext('{*}encapsulation'),
        encapsulationType=tree.findtext('{*}encapsulation-type-string'),
        state=tree.findtext('{*}state'),
        lineState=tree.findtext('{*}line-state'),
        actualState=tree.findtext('{*}actual-state'),
        actualLineState=tree.findtext('{*}actual-line-state'),
        l2Transport=tree.findtext('{*}l2-transport') == 'true',
        mtu=tree.findtext('{*}mtu'),
        subInterfaceMtuOverhead=tree.findtext('{*}sub-interface-mtu-overhead'))
