import os
import win32con
#import win32api
import win32gui
import ctypes
import time
import atexit
import cv2
import winsound
import threading

# Değiştirmeden önce imleci kaydediyoruz.
cursor = win32gui.LoadImage(0, 32512, win32con.IMAGE_CURSOR,
                            0, 0, win32con.LR_SHARED)
save_system_cursor = ctypes.windll.user32.CopyImage(cursor, win32con.IMAGE_CURSOR,
                                                    0, 0, win32con.LR_COPYFROMRESOURCE)


def restore_cursor():
    # Eski imleci yenisiyle değiştiriyoruz.
    print("restore_cursor")
    ctypes.windll.user32.SetSystemCursor(save_system_cursor, 32512)
    ctypes.windll.user32.DestroyCursor(save_system_cursor)


def change_speed(speed=1):
    # Sistemde fare hareketlerini yavaşlatmak için fonksiyon tanımlıyoruz.
    # 10 standart hızı, 1 de yavaş hızı temsil ediyor.
    # Biz burada yavaşlatmak istediğimiz için hızı 1'e eşitliyoruz.
    set_mouse_speed = 113
    ctypes.windll.user32.SystemParametersInfoA(set_mouse_speed, 0, speed, 0)


def cursor():
    # İmlecin sonunda yüklendiğinden emin oluyoruz.
    atexit.register(restore_cursor)

    # İmleci değiştiriyoruz.
    cursor = win32gui.LoadImage(0, "cursor.cur", win32con.IMAGE_CURSOR,
                                0, 0, win32con.LR_LOADFROMFILE)
    ctypes.windll.user32.SetSystemCursor(cursor, 32512)
    ctypes.windll.user32.DestroyCursor(cursor)
    change_speed()

# Saniye cinsinden ne kadar süre sonra kapanması gerektiğini yazıyoruz.


def shutdown():
    time.sleep(300)
    return os.system("shutdown /s /t 1")


def changeBG(path):
    changed = win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE
    ctypes.windll.user32.SystemParametersInfoW(
        win32con.SPI_SETDESKWALLPAPER, 0, path, changed)


def capture():
    while True:
        cam = cv2.VideoCapture(0)

        ret, frame = cam.read()

        if not ret:
            print('failed to grab frame')
        else:
            cv2.imwrite("capture.jpg", frame)

        # 5 saniyede 1 fotoğraf çekmesi için ayarlıyoruz.
        cam.release()
        path = os.path.join(os.getcwd(), 'capture.jpg')
        changeBG(path)
        time.sleep(5)


def sound_play():
    while True:
        winsound.PlaySound('chicken.wav', winsound.SND_FILENAME)
        time.sleep(3)
        # İstediğimiz sesi ekleyip kaç saniyede bir tekrar etmesi gerektiğini ayarlıyoruz.


# Ayarladığımız fonksiyonların aynı anda çalışabilmesi için
# threading kullanıyoruz.
shutdownthread = threading.Thread(target=shutdown)
cursorthread = threading.Thread(target=cursor)
soundthread = threading.Thread(target=sound_play)
capturethread = threading.Thread(target=capture)

shutdownthread.start()
cursorthread.start()
soundthread.start()
capturethread.start()
