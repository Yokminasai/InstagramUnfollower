from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
import getpass

INSTAGRAM_URL = "https://www.instagram.com/"

# --- ฟังก์ชันช่วย ---
def wait_for_element(driver, by, value, timeout=15):
    for _ in range(timeout * 2):
        try:
            el = driver.find_element(by, value)
            return el
        except NoSuchElementException:
            time.sleep(0.5)
    raise Exception(f"Timeout: {value}")

def login(driver, username, password):
    driver.get(INSTAGRAM_URL)
    time.sleep(3)
    # กรอก username/password
    wait_for_element(driver, By.NAME, "username").send_keys(username)
    wait_for_element(driver, By.NAME, "password").send_keys(password + Keys.RETURN)
    time.sleep(5)
    # --- ข้ามหน้า One Tap Login ---
    try:
        not_now_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]")
        not_now_btn.click()
        time.sleep(2)
    except NoSuchElementException:
        try:
            not_now_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'ภายหลัง')]")
            not_now_btn.click()
            time.sleep(2)
        except NoSuchElementException:
            pass  # ไม่มี popup นี้
    # ตรวจสอบ 2FA หรือ Challenge
    if "รหัสยืนยัน" in driver.page_source or "Enter Security Code" in driver.page_source or "verificationCode" in driver.page_source:
        print("[!] พบการยืนยันตัวตน 2FA หรือ OTP กรุณากรอกรหัสที่ได้รับ")
        try:
            code_input = wait_for_element(driver, By.NAME, "verificationCode", timeout=30)
        except Exception:
            code_input = None
        if code_input:
            code = input("กรุณากรอกรหัส OTP ที่ได้รับ: ")
            code_input.send_keys(code + Keys.RETURN)
            time.sleep(5)
        else:
            print("[!] ไม่พบช่องกรอกรหัส OTP อัตโนมัติ กรุณาตรวจสอบ browser และกรอกเองถ้ามี popup!")
            input("กด Enter หลังจากยืนยันตัวตนใน browser แล้ว...")
    # ตรวจสอบ Captcha หรือ Suspicious Login
    if "challenge" in driver.current_url or "captcha" in driver.page_source:
        print("[!] พบการยืนยันตัวตนหรือ Captcha กรุณาดำเนินการใน browser ด้วยตัวเอง!")
        input("กด Enter หลังจากยืนยันตัวตนใน browser แล้ว...")
    # ตรวจสอบว่าล็อกอินสำเร็จ
    try:
        wait_for_element(driver, By.XPATH, "//a[contains(@href, '/accounts/edit/') or contains(@href, '/accounts/onetap/?next=%2F') or contains(@href, '/direct/inbox/') or contains(@href, '/explore/') or contains(@href, '/accounts/activity/') or contains(@href, '/stories/')]", timeout=30)
        print("[+] Login สำเร็จ!")
    except Exception:
        print("[!] Login อาจไม่สำเร็จ กรุณาตรวจสอบหน้า browser ด้วยตัวเอง!")
        input("กด Enter เพื่อดำเนินการต่อ (หรือปิดโปรแกรมถ้า login ไม่สำเร็จ)...")

def get_following_list(driver, username):
    driver.get(f"{INSTAGRAM_URL}{username}/")
    time.sleep(3)

    # พยายามหา <a> following (โปรไฟล์ตัวเอง) ก่อน
    btn = None
    try:
        btn = driver.find_element(By.XPATH, "//a[contains(@href, '/following')]")
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(2)
    except Exception:
        # ถ้าไม่เจอ <a> ให้หา <button> Following (โปรไฟล์คนอื่น)
        try:
            btn = driver.find_element(By.XPATH, "//button[contains(., 'Following')]")
        except Exception:
            btn = driver.find_element(By.XPATH, "//button[contains(., 'กำลังติดตาม')]")
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(2)

    # Scroll เพื่อโหลดรายชื่อทั้งหมด
    try:
        scroll_box = wait_for_element(driver, By.XPATH, "//div[@role='dialog']//div[@role='dialog']/div[2]/div", timeout=10)
    except Exception:
        scroll_box = wait_for_element(driver, By.XPATH, "//div[@role='dialog']//div[contains(@style, 'overflow')]", timeout=10)
    last_height = 0
    while True:
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scroll_box)
        time.sleep(1)
        new_height = driver.execute_script('return arguments[0].scrollTop', scroll_box)
        if new_height == last_height:
            break
        last_height = new_height
    links = scroll_box.find_elements(By.TAG_NAME, 'a')
    following = [a.get_attribute('href').split('/')[-2] for a in links if a.get_attribute('href')]
    return following

def get_follower_list(driver, username):
    driver.get(f"{INSTAGRAM_URL}{username}/")
    time.sleep(3)
    try:
        btn = wait_for_element(driver, By.PARTIAL_LINK_TEXT, "ผู้ติดตาม", timeout=10)
    except Exception:
        btn = wait_for_element(driver, By.PARTIAL_LINK_TEXT, "Followers", timeout=10)
    btn.click()
    time.sleep(2)
    scroll_box = wait_for_element(driver, By.XPATH, "//div[@role='dialog']//div[@role='dialog']/div[2]/div")
    last_height = 0
    while True:
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scroll_box)
        time.sleep(1)
        new_height = driver.execute_script('return arguments[0].scrollTop', scroll_box)
        if new_height == last_height:
            break
        last_height = new_height
    links = scroll_box.find_elements(By.TAG_NAME, 'a')
    followers = [a.get_attribute('href').split('/')[-2] for a in links if a.get_attribute('href')]
    return followers

def unfollow_user(driver, username):
    try:
        driver.get(f"{INSTAGRAM_URL}{username}/")
        btn = wait_for_element(driver, By.XPATH, "//button[contains(text(), 'กำลังติดตาม') or contains(text(), 'Following') or contains(text(), 'Unfollow') or contains(text(), 'เลิกติดตาม')]")
        btn.click()
        time.sleep(1)
        # ยืนยัน unfollow (ถ้ามี popup)
        try:
            confirm = driver.find_element(By.XPATH, "//button[contains(text(), 'เลิกติดตาม') or contains(text(), 'Unfollow')]")
            confirm.click()
        except NoSuchElementException:
            pass
        print(f"[✓] Unfollow: {username}")
        return True
    except Exception as e:
        print(f"[!] ข้าม {username} ({e})")
        return False

def remove_follower(driver, username):
    try:
        driver.get(f"{INSTAGRAM_URL}{username}/")
        time.sleep(2)
        btn = wait_for_element(driver, By.XPATH, "//button[contains(text(), 'ผู้ติดตาม') or contains(text(), 'Followers')]")
        btn.click()
        time.sleep(2)
        dialog = wait_for_element(driver, By.XPATH, "//div[@role='dialog']//div[@role='dialog']/div[2]/div")
        # หาแถวแรกที่มีปุ่ม Remove/ลบ
        remove_btns = dialog.find_elements(By.XPATH, ".//button[contains(text(), 'ลบ') or contains(text(), 'Remove')]")
        if remove_btns:
            remove_btns[0].click()
            time.sleep(1)
            # ยืนยันลบ
            confirm = wait_for_element(driver, By.XPATH, "//button[contains(text(), 'ลบ') or contains(text(), 'Remove')]")
            confirm.click()
            print(f"[✓] Remove follower: {username}")
            return True
        else:
            print(f"[!] ไม่พบปุ่มลบ follower สำหรับ {username}")
            return False
    except Exception as e:
        print(f"[!] ข้าม {username} ({e})")
        return False

def unfollow_mass_fast(driver, profile_url, max_unfollow=50, delay=0.2):
    driver.get(profile_url)
    time.sleep(2)

    # 1. คลิกปุ่ม Following (เปิด dialog)
    following_btn = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/div/main/div/header/section[3]/ul/li[3]/div/a/span")
    following_btn.click()
    time.sleep(1.5)

    unfollowed = 0
    scroll_box = None

    while unfollowed < max_unfollow:
        if not scroll_box:
            try:
                scroll_box = driver.find_element(By.XPATH, "//div[@role='dialog']//div[contains(@style, 'overflow')]")
            except:
                scroll_box = driver.find_element(By.XPATH, "//div[@role='dialog']")
        # หา "Following" buttons ทุกปุ่มใน dialog
        follow_btns = driver.find_elements(By.XPATH, "//div[@role='dialog']//button")
        found = False
        for btn in follow_btns:
            try:
                # ข้ามปุ่มที่ไม่ใช่ "Following" หรือ "กำลังติดตาม" หรือปุ่มที่ disabled
                btn_text = btn.text.strip()
                if btn.get_attribute("disabled") or btn_text not in ["Following", "กำลังติดตาม"]:
                    continue
                driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                btn.click()
                time.sleep(0.15)
                # popup ยืนยัน unfollow
                confirm_btn = driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div/div/button[1]")
                confirm_btn.click()
                unfollowed += 1
                print(f"[✓] Unfollow {unfollowed}")
                time.sleep(delay)
                # Scroll dialog หลัง unfollow ทุกคน
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_box)
                time.sleep(0.2)
                found = True
                break  # ออกจาก for-loop เพื่อ refresh รายชื่อใหม่
            except Exception as e:
                print(f"[!] Error: {e}")
                continue
        if not found:
            print("ไม่พบปุ่ม Following ที่คลิกได้ใน dialog แล้ว")
            break
    print("Done.")

def main():
    print(r"""
       _             __     __     _____   _____   _   _    _____ 
      | |     /\     \ \   / /    / ____| |_   _| | \ | |  / ____|
      | |    /  \     \ \_/ /    | (___     | |   |  \| | | (___  
  _   | |   / /\ \     \   /      \___ \    | |   | . ` |  \___ \ 
 | |__| |  / ____ \     | |       ____) |  _| |_  | |\  |  ____) |
  \____/  /_/    \_\    |_|      |_____/  |_____| |_| \_| |_____/ 
                                                                  
                                                                  
""")
    print("==== Instagram Auto Unfollow/Remove Follower ====")
    print("1. Unfollow Following (เลิกติดตาม)")
    print("2. Remove Follower (ลบผู้ติดตาม)")
    mode = input("เลือกโหมด (1 หรือ 2): ").strip()
    username = input("Instagram Username: ")
    password = getpass.getpass("Instagram Password: ")
    max_action = int(input("จำนวนสูงสุดต่อรอบ (เช่น 10): "))
    delay = float(input("ดีเลย์ระหว่างแต่ละคน (วินาที, เช่น 3): "))

    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    # ไม่ใช้ headless เพื่อให้ผู้ใช้ยืนยันตัวเองได้
    driver = webdriver.Chrome(options=chrome_options)

    try:
        login(driver, username, password)
        if mode == '1':
            # unfollow following แบบเร็วและ scroll อัตโนมัติ
            unfollow_mass_fast(driver, f"https://www.instagram.com/{username}/", max_unfollow=max_action, delay=delay)
            print(f"\n[✓] Unfollow เสร็จสิ้น (สูงสุด {max_action} คน)")
        elif mode == '2':
            users = get_follower_list(driver, username)
            print(f"[i] พบ {len(users)} คนที่ติดตามคุณ")
            count = 0
            for user in users:
                if count >= max_action:
                    break
                if remove_follower(driver, user):
                    count += 1
                    time.sleep(delay)
            print(f"\n[✓] Remove follower เสร็จสิ้น {count} คน")
        else:
            print("[!] เลือกโหมดไม่ถูกต้อง")
    finally:
        driver.quit()

if __name__ == "__main__":
    main() 