import Adafruit_TMP.TMP006 as TMP006
import time
import statistics
import logging
import socket


sensor = TMP006.TMP006()
sensor.begin(samplerate=TMP006.CFG_4SAMPLE)

TEMP_MIN=35
TEMP_MAX=41

def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def int_from_bytes(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')

def get_temp():
    return sensor.readObjTempC()

def get_humam_temp():
    temps = []
    for i in range(15):
        t = get_temp()
        print(t)
        if (TEMP_MIN <= t <= TEMP_MAX):
            temps.append(t)
        if (len(temps) == 3):
            break
        time.sleep(.6)
    print("Temperaturas capturadas: ", temps)
    if len(temps) >= 3:
        return statistics.median(temps)
    else:
        return None

logging.basicConfig(filename='temp.log', filemode='a', format='%(asctime)-15s - %(levelname)s - %(message)s', level=logging.INFO)


while True:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('localhost', 31023))
            s.listen()
            conn, addr = s.accept()
            with conn:
                while True:
                    pkg = conn.recv(128)
                    user = pkg.decode('utf-8')
                    print(user)
                    t = get_humam_temp()
                    temperatura = t if t != None else 0
                    conn.sendall(str(temperatura).encode('utf-8'))
                    logging.info("Temperatura do usuário " + str(user) + " registrada: " + str(temperatura))
    except Exception as e:
        logging.exception(e)
        print("Problema no socket", e)
        time.sleep(1)