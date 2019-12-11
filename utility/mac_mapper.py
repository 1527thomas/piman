from pysnmp.hlapi import *
import config
import sys


#Reference SNMAP-WALK from:https://www.google.com/search?q=snmp+walk+solarwinds&oq=snmp+walk&aqs=chrome.5.69i57j0l5.2209j0j4&sourceid=chrome&ie=UTF-8

#.env file need to have VLAN number & Switch address

host = config.SWITCH_ADDR
vlan = config.VLAN


def decToHexAddress(arg):
    arr = arg.split(".")
    output = ''

    for i in range(len(arr)):
        if i == len(arr) - 1:
            output = output + hex(int(arr[i])).replace('0x', '').upper()
        else:
            output = output + hex(int(arr[i])).replace('0x', '').upper() + ":"
    return output


def mac_mapper():
    output = []
    for (errorIndication, errorStatus, errorIndex, varBinds) in nextCmd(SnmpEngine(),
         CommunityData('private@' + vlan), UdpTransportTarget((host, 161)), ContextData(),
         ObjectType(ObjectIdentity('1.3.6.1.2.1.17.4.3.1.2')), lexicographicMode=False):
        
        if errorIndication:
            print(errorIndication, file=sys.stderr)
            break
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'),
                  file=sys.stderr)
            break
        else:
            data = []

            for varBind in varBinds:
                #data.append(str(varBind))

                element = str(varBind)
                element = element.replace("SNMPv2-SMI::mib-2.17.4.3.1.2.", "").replace(" = ", ";")
                splitArr = element.split(";")
                data.append(host + ',' + element.replace(splitArr[0],decToHexAddress(splitArr[0])))


            print("['SWITCH ADDRESS,MAC ADDRESS;PORT']")
            print(data)

        output.extend(data)

    text = ""
    for j in output:
        text += j + '\n'

    with open('utility/mac_mapper.txt', "w") as f:
        f.write(text)


if __name__ == "__main__":
    mac_mapper()
