# import keyboard
# import pyautogui
# import time

# screen_width, screen_height = pyautogui.size()
# print(f'Screen width: {screen_width}')
# print(f'Screen height: {screen_height}')

# right_side_region = (screen_width // 2, 0, screen_width // 2, screen_height)
# print(f'Right side region: {right_side_region}')

# count = 0
# while True:
#     try:
#         nova_logo = pyautogui.locateCenterOnScreen('nova_video_logo.png', confidence=0.999, region=right_side_region)
#         print(f'{count}. Ad is currently not playing!') 
#         count += 1  
#         time.sleep(0.2)
#     except pyautogui.ImageNotFoundException:
#         try:
#             mute_sound = pyautogui.locateOnScreen('mute_sound.png', confidence=0.9) 
#             print('Logo is not on screen.')
#             if mute_sound is not None:
#                 print('Mute sound located.')
#                 pyautogui.moveTo(mute_sound)
#                 pyautogui.click()
#                 time.sleep(0.2)
        
#             skip_ad = pyautogui.locateOnScreen('nova_skip_ads.png', confidence=1)  # Look for the image on the screen
#             if skip_ad is not None:
#                 print('Skipping ad.')
#                 pyautogui.moveTo(skip_ad)
#                 pyautogui.click()
#         except pyautogui.ImageNotFoundException:
#             continue

import pyautogui
import time
import logging

# --- Configuration ---
LOG_LEVEL = logging.INFO
CONFIDENCE_LOGO = 0.9
CONFIDENCE_MUTE = 0.8
CONFIDENCE_SKIP = 0.8
SLEEP_MAIN = 0.2
SLEEP_ERROR = 1

# --- Logging Setup ---
logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s',
    level=LOG_LEVEL
)

def get_screen_region():
    screen_width, screen_height = pyautogui.size()
    logging.info(f'Screen width: {screen_width}, height: {screen_height}')
    region = (screen_width // 2, 0, screen_width // 2, screen_height)
    logging.info(f'Right side region: {region}')
    return region

def locate_and_click(image, confidence, description):
    location = pyautogui.locateOnScreen(image, confidence=confidence)
    if location:
        logging.info(f'{description} located.')
        pyautogui.moveTo(location)
        pyautogui.click()
        return True
    else:
        logging.info(f'{description} not found.')
        return False

def mute_sound():
    return locate_and_click('mute_sound.png', CONFIDENCE_MUTE, 'Mute sound')

def skip_ad():
    return locate_and_click('nova_skip_ads.png', CONFIDENCE_SKIP, 'Skip ad')

def unmute_sound():
    return locate_and_click('mute_sound.png', CONFIDENCE_MUTE, 'Unmute sound')

def main():
    region = get_screen_region()
    while True:
        try:
            nova_logo = pyautogui.locateOnScreen('nova_video_logo.png', region=region, confidence=CONFIDENCE_LOGO)
            if nova_logo:
                logging.info('Nova logo image on screen.')
                time.sleep(SLEEP_MAIN)
                continue
            else:
                raise pyautogui.ImageNotFoundException
        except pyautogui.ImageNotFoundException:
            logging.info('Nova logo is not on screen.')
            time.sleep(SLEEP_MAIN)
            if mute_sound():
                logging.info('Sound muted.')
                while True:
                    if skip_ad():
                        logging.info('Ad was skipped.')
                        time.sleep(SLEEP_MAIN)
                        nova_logo_2 = pyautogui.locateOnScreen('nova_video_logo.png', region=region, confidence=CONFIDENCE_LOGO)
                        if nova_logo_2:
                            logging.info('Located Nova logo on screen.')
                            if unmute_sound():
                                logging.info('Sound unmuted.')
                            break
                        else:
                            continue
                    else:
                        time.sleep(SLEEP_MAIN)
                        continue
            else:
                logging.info("Can't locate mute_sound.")
                time.sleep(SLEEP_ERROR)
                continue

if __name__ == "__main__":
    main()
        
