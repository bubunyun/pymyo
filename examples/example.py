# ruff: noqa: T201, INP001
from __future__ import annotations

import asyncio

from bleak import BleakScanner

from pymyo import Myo
from pymyo.types import EmgMode, EmgValue, ImuMode, SleepMode, UnsupportedFeatureError

# Put your own Myo Bluetooth address here or device UUID if you're on macOS.
MYO_ADDRESS = "DD:31:D8:40:BC:22"


async def main() -> None:
    # You can use an asynchronous context manager to manage connection/disconnection
    myo_device = await BleakScanner.find_device_by_address(MYO_ADDRESS)
    async with Myo(myo_device) as myo:
        # Access information using awaitable properties
        print("Device name:", await myo.name)
        print("Battery level:", await myo.battery)
        print("Firmware version:", await myo.firmware_version)
        print("Firmware info:", await myo.info)

        await myo.vibrate2((250, 255), (250, 128), (250, 255))

        # Register an event listener
        def on_tap(direction: int, count: int) -> None:
            print(f"Tap: direction: {direction} count: {count}")

        myo.on_tap(on_tap)

        # Register an event listener using a decorator
        @myo.on_emg
        def on_emg(emg: tuple[EmgValue, EmgValue]) -> None:
            print(emg)

        # Enable the optional battery notifications
        @myo.on_battery
        def battery_callback(level: int) -> None:
            print(f"Battery level: {level}")

        try:
            await myo.enable_battery_notifications()
        except UnsupportedFeatureError as e:
            print(e)

        await myo.set_sleep_mode(SleepMode.NEVER_SLEEP)
        await asyncio.sleep(1)
        await myo.set_mode(emg_mode=EmgMode.EMG, imu_mode=ImuMode.EVENTS)

        while True:
            await asyncio.sleep(1)  # Do other stuff


if __name__ == "__main__":
    asyncio.run(main())
