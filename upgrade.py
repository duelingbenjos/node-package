from datetime import datetime
from dateutil import parser
import asyncio
import os
import re
import socketio
import subprocess

sio = socketio.AsyncClient(logger=True, engineio_logger=True)

def validate_ip_address(ip_str):
    pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
    match = re.search(pattern, ip_str)

    return True if match else False

def parse_bootnodes(ips: list):
    return ':'.join(list(filter(lambda ip: validate_ip_address(ip), ips)))

@sio.event
async def connect():
    await sio.emit('join', {'room': 'upgrade'})

@sio.event
async def disconnect():
    await sio.emit('leave', {'room': 'upgrade'})

@sio.event
async def event(data):
    data = data['data']

    os.environ['LAMDEN_TAG'] = data['lamden_tag']
    os.environ['CONTRACTING_TAG'] = data['contracting_tag']
    os.environ['LAMDEN_BOOTNODES'] = parse_bootnodes(data['bootnode_ips'])
    os.environ.pop('LAMDEN_NETWORK', None)
    utc_when = parser.parse(data['utc_when'])

    subprocess.check_call(['make', 'build'])

    while utc_when > datetime.utcnow():
        asyncio.sleep(1)

    subprocess.check_call(['make', 'reboot'])

async def main():
    await sio.connect(f'http://localhost:17080')
    await sio.wait()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
