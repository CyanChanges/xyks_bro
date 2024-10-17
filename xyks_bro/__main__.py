"""
小猿口算, 小子
"""

import binascii
import json
import sys
from functools import partial
from pathlib import Path
from typing import Any, TypedDict, Annotated

import typer
import frida
from frida._frida import Application
from frida.core import Script, Session, Device
from loguru import logger

logger.remove()
logger.add(
    sys.stderr,
    format="<white>[</white><green>{time:YYYY-MM-DD HH:mm:ss}</green><white>]</white> | "
           "<level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
           "{message}",
    level="INFO"
)

TIME_MS = 100

current_dir = Path(__file__).parent
hook_script_file = current_dir / 'hook.js'
aad_script_file = current_dir / 'aad.js'


class MessagePayload(TypedDict):
    type: str
    data: Any


class Message(TypedDict):
    payload: MessagePayload


def str2hex(input_str: str):
    return binascii.hexlify(input_str.encode('u8')).decode('u8')


def log_handler(payload: MessagePayload):
    data = payload['data']

    assert payload['type'] == 'log'
    assert 'level' in data
    assert 'message' in data

    def remote_log():
        message = data['message']
        match data['level']:
            case 'info':
                logger.info(message)
            case 'warning':
                logger.warning(message)
            case 'error':
                logger.error(message)
            case 'trace':
                logger.trace(message)

    remote_log()


def ex_handler(payload: dict):
    if 'type' in payload and payload['type'] == 'error':
        logger.warning(payload['description'])
    else:
        logger.trace(payload)


def fuck_anti_frida(session: Session):
    def aad_handler(script: Script, message: Message, extra: Any):
        if 'payload' not in message:
            return ex_handler(message)

        payload = message['payload']
        match payload['type']:
            case 'log':
                log_handler(payload)
            case ty:
                logger.warning("unknown payload type: {ty}", ty=ty)
                return

    aad_script = aad_script_file.read_text("u8")
    aad = session.create_script(aad_script)
    aad.on("message", partial(aad_handler, aad))
    aad.load()


def load_script(session: Session):
    def sc_handler(script: Script, message: Message, extra: Any):
        if 'payload' not in message:
            return ex_handler(message)
        payload = message['payload']
        match payload['type']:
            case 'log':
                log_handler(payload)
                return
            case 'data':
                pass
            case 'ready':
                logger.success("Hook success, ready to go")
                return
            case ty:
                logger.warning("unknown payload type: {ty}", ty=ty)
                return

        binary = bytes.fromhex(payload['data'])
        data = binary.decode('u8')

        json_data = json.loads(data)

        if 'costTime' in json_data:
            old_cost_time = json_data['costTime']
            logger.info('Update Cost Time：{} -> {}', old_cost_time, TIME_MS)
            json_data['costTime'] = TIME_MS
        else:
            logger.debug("Skipping {}", json_data)

        data = json.dumps(json_data)

        script.post({'type': 'patch', 'data': data})

    hook_script = hook_script_file.read_text("u8")
    sc: Script = session.create_script(hook_script)
    sc.on("message", partial(sc_handler, sc))
    sc.load()


def main(
        target: Annotated[str, typer.Argument(help="remote frida server address in `host:port`")],
        skip_aad: Annotated[bool, typer.Option(
            "-s", "--skip-aad",
            help="Skip remove the anti-debug library")
        ] = False
):
    """
    Automatic launch and hook XYKS,
    provide remote frida server address of your Android device and go

    Have Fun!
    """
    package_name = "com.fenbi.android.leo"

    logger.info("Connecting to device...")
    manager = frida.get_device_manager()
    device: Device = manager.add_remote_device(target)
    logger.info("Connected to device")

    for application in device.enumerate_applications():
        application: Application
        if application.name == "小猿口算" and application.pid != 0:
            device.kill(application.pid)

    logger.info("Spawn `{}`", package_name)
    pid = device.spawn([package_name])

    logger.debug("Attach to {pid}", pid=pid)
    # session = device.attach('小猿口算')
    session = device.attach(pid)

    if not skip_aad:
        logger.info("Fuck Anti-Frida")
        fuck_anti_frida(session)

    logger.debug(f"Resume {pid}...")
    device.resume(pid)

    logger.info("Run Good scripts")
    load_script(session)

    sys.stdin.read()


if __name__ == "__main__":
    typer.run(main)
