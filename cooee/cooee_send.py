# 
# This file is part of the bloomsky utilities distribution (https://github.com/michalkouril/bloomsky).
# Copyright (c) 2023 Michal Kouril.
# 
# This program is free software: you can redistribute it and/or modify  
# it under the terms of the GNU General Public License as published by  
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import socket
from Crypto.Cipher import AES
from time import sleep
import argparse


def cooee_encrypt(data):
   packetlen = len(data)+10+8
   headerHex = "2"+hex(packetlen)[2:].zfill(3)+"0000000000000000"
   header = bytes.fromhex(headerHex)

   key = b'abcdabcdabcdabcd'
   # nonce = b'\0\0\0\0\0\0\0\0wiced'
   nonce = header[2:]+b'wiced'

   # Encryption 
   cipher = AES.new(key, AES.MODE_CCM, nonce, mac_len=8)
   cipher.update(header)
   ciphertext, tag = cipher.encrypt_and_digest(data)

   # ciphertextTagHex = ciphertext.hex() + tag.hex()
   # return(headerHex + ciphertextTagHex)
   return(header + ciphertext + tag)


def send_cooee_raw(msg):

   # 239.254.x.x
   MCAST_GRP = '239.246.0.0'
   MCAST_PORT = 1503

   # regarding socket.IP_MULTICAST_TTL
   # ---------------------------------
   # for all packets sent, after two hops on the network the packet will not 
   # be re-sent/broadcast (see https://www.tldp.org/HOWTO/Multicast-HOWTO-6.html)
   MULTICAST_TTL = 1
   
   sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
   sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

   for i in range(0,3):
       sleep(0.015)
       sock.sendto(b'', (MCAST_GRP, MCAST_PORT))
  
   # pad the message
   if (len(msg)%2) != 0:
       msg += b'\0'

   msgLen=len(msg)
   bigarray=bytearray(msgLen+1)
   numPackets=round((msgLen+1)/2)
   for i in range(0,numPackets-1):
       mcast_ip = "239.254.{}.{}".format(msg[i*2],msg[i*2+1])
       if (i%4)==0:
           sock.sendto(b'', (MCAST_GRP, MCAST_PORT))
       sock.sendto(bigarray[:2*i], (mcast_ip, MCAST_PORT))
       sleep(0.015)


#
# parse command line parameters
#
parser = argparse.ArgumentParser(description='Intiate cooee WiFi SSID/Password bootstrap for BloomSky SKY1 device. First turn on the device using the power button. After a few seconds push the WiFi button and hold for 10 seconds. This will wipe the existing WiFi info and starts listening for cooee multicast on all 2.4GHz WiFi Channels. The WiFi LED start flashing slowly. The process will take a while (even a few minutes) -- once the WiFi LED starts flashing faster (once per second) the device acquired WiFi SSID/Password.')

parser.add_argument('--ssid', dest='ssid', required=True, help='WiFi network SSID (no default)')
parser.add_argument('--password', dest='password', required=True, help='WiFi network password (no default)')
parser.add_argument('--myip', dest='ip', required=False, help='Override my ip')

args = parser.parse_args()

# encode msg fields (SSID, password and mylocalip)

ssidBin = args.ssid.encode('ascii')
ssidLen = len(ssidBin)
ssidType = 0

passwordBin = args.password.encode('ascii')
passwordLen = len(passwordBin)
passwordType = 3

ip_address = args.ip
if ip_address == None:
   hostname = socket.gethostname()
   ip_address = socket.gethostbyname(hostname)

myIpBin = socket.inet_aton(ip_address)
myIpLen = 4
myIpType = 2

ssidField = ssidType.to_bytes()+ssidLen.to_bytes()+ssidBin
passwordField = passwordType.to_bytes()+passwordLen.to_bytes()+passwordBin
myIpField = myIpType.to_bytes()+myIpLen.to_bytes()+myIpBin

plain_data = ssidField + passwordField + myIpField

# encrypt the message
encrypted_data = cooee_encrypt(plain_data)

# send via multicast
for i in range(0,1000):
   send_cooee_raw(encrypted_data)
   sleep(2)
   print("retrying...")
