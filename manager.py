from datetime import datetime
from dateutil import parser
import asyncio
import os
import socketio

async def run_command(args):
    with open(f'{"_".join(args)}.log', 'w') as f:
        process = await asyncio.create_subprocess_exec(*args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

        writer = asyncio.StreamWriter(f, None, None, loop)
        stdout, stderr = await asyncio.gather(process.stdout.read(), process.stderr.read())
        writer.write(stdout); writer.write(stderr)

        await writer.drain()
        writer.close()
        
    return await process.wait()

async def upgrade_handler(data: dict):
    os.environ['LAMDEN_TAG'] = data['lamden_tag']
    os.environ['CONTRACTING_TAG'] = data['contracting_tag']
    os.environ['LAMDEN_BOOTNODES'] = ':'.join(data['bootnode_ips'])
    os.environ.pop('LAMDEN_NETWORK', None)
    utc_when = parser.parse(data['utc_when'])

    if await run_command(['make', 'build']) != 0:
        return

    while utc_when > datetime.utcnow():
        await asyncio.sleep(1)

    await run_command(['make', 'restart'])

async def network_error_handler(data: dict):
    if await run_command(['make', 'stop']) != 0:
        return

    network_is_down = True
    while network_is_down:
        for ip in data['bootnode_ips']:
            if await run_command(['ping', '-c', '1', ip]) == 0:
                network_is_down = False
                break

    os.environ['LAMDEN_BOOTNODES'] = ':'.join(data['bootnode_ips'])
    os.environ.pop('LAMDEN_NETWORK', None)

    await run_command(['make', 'start'])

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
    asyncio.ensure_future(event_handlers[event['event']](event['data']))

async def main():
    await sio.connect(f'http://localhost:17080')
    await sio.wait()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
