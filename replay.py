from time import sleep
from SX127x.LoRa import *
from SX127x.board_config import BOARD
#import logging
#import parse
#import simplekml
#import requests

BOARD.setup()
encrypted_payloads = []
frames_received = 0
max_frames = 5

class LoRaRcvCont(LoRa):
    def __init__(self, verbose=False):
        super(LoRaRcvCont, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)

    def start(self):
        self.reset_ptr_rx()

    def on_rx_done(self):
        self.clear_irq_flags(RxDone=1)
        encrypted_payloads.append(self.read_payload(nocheck=True))
        utf_str = bytes(encrypted_payloads[-1]).decode("utf-8",'ignore')
        print(f"Received: {utf_str}")
        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT) 


def main():
    lora = LoRaRcvCont(verbose=False)
    lora.set_mode(MODE.STDBY)

    lora.set_freq(915.0)
    lora.start()

    lora.set_mode(MODE.RXCONT)
    while len(encrypted_payloads) < max_frames:
        sleep(.5)
        rssi_value = lora.get_rssi_value()
        status = lora.get_modem_status()
        sys.stdout.flush()
	
    lora.set_mode(MODE.SLEEP)
    print(f"{max_frames} frames received\nStarting transmission in 15 seconds...")
    sleep(15)
    for i in range(len(encrypted_payloads)):
        utf_str = bytes(encrypted_payloads[i]).decode("utf-8",'ignore')
        print(f"Sending: {utf_str}")
        lora.write_payload(encrypted_payloads[i])
        lora.set_mode(MODE.TX)
        sleep(10)
    print("Transmission done!")

if __name__ == "__main__":
	main()

	
