# pip install cv2imshow adbblitz adbkit locate-pixelcolor-cpppragma
from adbblitz import AdbShotTCP
import numpy as np
from cv2imshow.cv2imshow import cv2_imshow_multi
from locate_pixelcolor_cpppragma import search_colors
from adbkit import ADBTools
adb_path = r"C:\ProgramData\chocolatey\lib\scrcpy\tools\scrcpy-win64-v2.0\adb.exe"
deviceserial = "localhost:5555"
adb = ADBTools(adb_path=adb_path, deviceserial=deviceserial, sdcard="/sdcard/")
adb.aa_connect_to_device()
adb.aa_root_bluestacks_instances()
adb.aa_enable_root().aa_disable_roblox_textures()
colors0 = np.ascontiguousarray(
    np.array([[x, x, x] for x in range(70, 256, 1)], dtype=np.uint8)
)
width, height = 1920, 1080
click_button = 978, 978
start_crop, end_crop = (200, 150), (1600, 800)
cpu = 4
show_screenshot = False

verification_var = 0
wait = False
wait_counter = 0
old = 0
waitcounterlimit = 1000

def crop_imageselection(image, start: tuple, end: tuple):
    return image[start[1] : end[1], start[0] : end[0]]


with AdbShotTCP(
    device_serial=deviceserial,
    adb_path=adb_path,
    max_video_width=width,
) as shosho:
    for bi in shosho:
        print(f"{wait=}, {wait_counter=}",end='\r')
        if wait_counter >= waitcounterlimit:
            wait = False
            wait_counter = 0
        if wait:
            while wait_counter < waitcounterlimit:
                if wait_counter == waitcounterlimit // 2:
                    adb.aa_input_tap(*click_button)
                wait_counter += 1
                break
            continue
        if bi.dtype == np.uint16:
            continue
        bi = crop_imageselection(bi, start_crop, end_crop)
        resus0 = search_colors(pic=bi, colors=colors0, cpus=cpu)
        numpix = resus0.shape[0]
        if abs(numpix - old) > 0:
            print(f"{numpix - old}", end="\n")
            verification_var = 0
        else:
            print(f"\t\t{numpix - old}")
            verification_var += 1
        if verification_var > 4:
            print("found")
            adb.aa_input_tap(*click_button)
            wait = True
            verification_var = 0
        if show_screenshot:
            cv2_imshow_multi(
                title="screenshot_pic",
                image=bi,
                killkeys="ctrl+alt+h",  # switch on/off
            )
        old = numpix



