import cv2
import numpy as np
import pyautogui
import time
import pygame

# 이미지 로드
def load_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"이미지를 읽을 수 없습니다. 경로를 확인하세요: {image_path}")
    return image.astype(np.uint8)

def load_images(image_paths):
    images = {}
    for i, path in enumerate(image_paths, start=1):
        image = load_image(path)
        images[f"img{i}"] = image
    return images

monster_image_paths = ["image/img1.png", "image/img2.png", "image/img3.png",
               "image/img4.png", "image/img5.png", "image/img6.png",
               "image/img7.png", "image/img8.png", "image/img9.png",
               "image/img10.png"]
monster_images = load_images(monster_image_paths)

w_icon_template = load_image("image/w_skill_icon.png")






def capture_screen():
    screenshot = pyautogui.screenshot()
    screen = np.array(screenshot)
    screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
    return screen

def is_image_on_screen(template, screen, threshold):
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)
    return max_val > threshold

def play_music(sound_path):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()



def detect_monster(images, screen):
    for img_name, template in images.items():
        try:
            image_found = is_image_on_screen(template, screen, 0.5)

            # 이미지가 존재하면 결과 출력하고 즉시 루프 종료
            if image_found:
                print(f"{img_name}이(가) 존재합니다.")

                # 경고음 재생
                if current_music is not None and pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
                play_music("music/monster_appear.mp3")

                return True

        except ValueError as e:
            print(f"오류: {e}")

    # 모든 이미지가 존재하지 않을 때의 메시지 출력
    else:
        print("모든 이미지가 화면에 존재하지 않습니다.")
        pygame.mixer.music.stop()

    return False

def detect_attack_skill(screen):
    global is_attack_trigger, wtime
    if is_attack_trigger:
        is_attack = is_image_on_screen(w_icon_template, screen, 0.9)
        if is_attack:
            # 이후 3분동안 감지하지 않음
            is_attack_trigger = False
            wtime = time.time()
            play_music("music/skill_use.mp3")
            print("W 감지")
    else:
        if time.time() - wtime > 180:
            is_attack_trigger = True
            play_music("music/skill_cool_done.mp3")
            print("w 쿨타임 완료")  






pygame.mixer.init()
current_music = None
is_attack_trigger = True

while True:
    # 화면 캡처후 특정 이미지 존재 여부 검사
    screen = capture_screen()

    # 몬스터 감지 및 소리 재생
    if detect_monster(monster_images, screen):
        continue  # Skip the rest of the loop if a monster is found

    # 공격 스킬 사용 감지
    detect_attack_skill(screen)
        
    time.sleep(0.5)
