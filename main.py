# 컨트롤러 중앙 418 818 차이 각각 100씩 (중복입력시 50씩 차이)
# 공격 1359 893
# 궁 1435 737
# 스킬 1266 739
# 대쉬 1188 913

# w: 418 718
# a: 318 818
# s: 418 918
# d: 518 818

# w and a: 368 768
# w and d: 468 768
# s and a: 368 868
# s and d: 468 868

# space: 1188 913
# shift: 1266 739
# r: 1359 893

import threading
import time
from pynput import keyboard
import pyautogui

# 좌표 설정
coordinates = {
    'w': (418, 718),
    'a': (318, 818),
    's': (418, 918),
    'd': (518, 818),
    'wa': (368, 768),
    'wd': (468, 768),
    'sa': (368, 868),
    'sd': (468, 868),
    'space': (1188, 913),
    'shift': (1266, 739),
    'e': (1359, 893),
    'r': (1435, 737)
}

# 현재 눌린 키들
pressed_keys = set()
clicking = False
click_thread = None

def get_click_position():
    if 'space' in pressed_keys:
        return coordinates['space']
    if 'shift' in pressed_keys:
        return coordinates['shift']
    if 'e' in pressed_keys:
        return coordinates['e']
    if 'r' in pressed_keys:
        return coordinates['r']
    if 'w' in pressed_keys and 'a' in pressed_keys:
        return coordinates['wa']
    if 'w' in pressed_keys and 'd' in pressed_keys:
        return coordinates['wd']
    if 's' in pressed_keys and 'a' in pressed_keys:
        return coordinates['sa']
    if 's' in pressed_keys and 'd' in pressed_keys:
        return coordinates['sd']
    if 'w' in pressed_keys:
        return coordinates['w']
    if 'a' in pressed_keys:
        return coordinates['a']
    if 's' in pressed_keys:
        return coordinates['s']
    if 'd' in pressed_keys:
        return coordinates['d']
    return None

def click_loop():
    global clicking
    while clicking:
        pos = get_click_position()
        if pos:
            pyautogui.click(pos)
        time.sleep(0.1)

def on_press(key):
    global clicking, click_thread
    try:
        if key.char in 'wasdr':
            pressed_keys.add(key.char)
    except AttributeError:
        if key == keyboard.Key.space:
            pressed_keys.add('space')
        elif key == keyboard.Key.shift:
            pressed_keys.add('shift')
    except:
        return
    
    if not clicking and pressed_keys:
        clicking = True
        click_thread = threading.Thread(target=click_loop)
        click_thread.start()

def on_release(key):
    global clicking
    try:
        if key.char in 'wasdr':
            pressed_keys.discard(key.char)
    except AttributeError:
        if key == keyboard.Key.space:
            pressed_keys.discard('space')
        elif key == keyboard.Key.shift:
            pressed_keys.discard('shift')
    except:
        return
    
    if not pressed_keys and clicking:
        clicking = False
        click_thread.join()

# 리스너 설정
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
