from datetime import datetime
from dateutil import parser
import asyncio
import os
import socketio
import subprocess

def upgrade_handler(data: dict):
    os.environ['LAMDEN_TAG'] = data['lamden_tag']
    os.environ['CONTRACTING_TAG'] = data['contracting_tag']
    os.environ['LAMDEN_BOOTNODES'] = ':'.join(data['bootnode_ips'])
    os.environ.pop('LAMDEN_NETWORK', None)
    utc_when = parser.parse(data['utc_when'])

    subprocess.check_call(['make', 'build'])

    while utc_when > datetime.utcnow():
        asyncio.sleep(1)

    subprocess.check_call(['make', 'reboot'])

def network_error_handler(data: dict):
    subprocess.check_call(['make', 'stop'])

    network_is_down = True
    while network_is_down:
        for ip in data['bootnode_ips']:
            if subprocess.call(['ping', '-c', '1', ip]) == 0:
                network_is_down = False
                break

    os.environ['LAMDEN_BOOTNODES'] = ':'.join(bootnode_ips)
    os.environ.pop('LAMDEN_NETWORK', None)

    subprocess.call(['make', 'reboot'])

event_handlers = {
    'upgrade': upgrade_handler,
    'network_error': network_error_handler
}

sio = socketio.AsyncClient(logger=True, engineio_logger=True)

@sio.event
async def connect():
    for room in list(event_handlers.keys()):
        await sio.emit('join', {'room': room})

@sio.event
async def disconnect():
    for room in list(event_handlers.keys()):
        await sio.emit('leave', {'room': room})

@sio.event
async def event(event: dict):
    event_handlers[event['event']](event['data'])

async def main():
    await sio.connect(f'http://localhost:{os.environ["LAMDEN_ES_PORT"]}')
    await sio.wait()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
