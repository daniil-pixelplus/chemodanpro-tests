import pytest
import requests
import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="module")
def driver():
    print("Настройка драйвера...")
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=opts)
    driver.maximize_window()
    yield driver
    print("Закрытие драйвера...")
    driver.quit()

@pytest.fixture(scope="module")
def fixture_get_temp_email(driver):
    print("Получение временного адреса электронной почты...")
    driver.get("https://www.minuteinbox.com/")
    wait = WebDriverWait(driver, 10)
    email_element = wait.until(EC.visibility_of_element_located((By.ID, "email")))
    temp_email = email_element.text
    return temp_email

def test_registration(driver, fixture_get_temp_email):
    print("Запуск теста регистрации...")
    temp_email = fixture_get_temp_email
    driver.get("https://www.chemodanpro.ru/")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/header/div[2]/div/div/div/div[3]/div/ul/li[7]/a")))
    login_button = driver.find_element(By.XPATH, "/html/body/header/div[2]/div/div/div/div[3]/div/ul/li[7]/a")
    login_button.click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//a[@href='/login/?register=yes']")))
    registration_link = driver.find_element(By.XPATH, "//a[@href='/login/?register=yes']")
    registration_link.click()
    assert "register=yes" in driver.current_url
    print("Тест регистрации начат...")
    wait.until(EC.visibility_of_element_located((By.ID, "register_form")))
    fill_registration_form(driver, temp_email)
    print("Тест регистрации завершен успешно.")
    nonexistent_login(driver, fixture_get_temp_email)
    print("Тест несуществующий аккаунт.")
    register_user(temp_email)
    print(temp_email)

def fill_registration_form(driver, temp_email):
    print("Заполнение формы регистрации...")
    wait = WebDriverWait(driver, 10)
    user_type_dropdown = driver.find_element(By.CLASS_NAME, "select2-selection__rendered")
    user_type_dropdown.click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//li[@class='select2-results__option']")))
    physical_person_option = driver.find_element(By.XPATH, "//li[contains(text(),'Физическое лицо')]")
    physical_person_option.click()
    print("Тип пользователя выбран: Физическое лицо.")
    driver.find_element(By.NAME, "USER_LAST_NAME").send_keys("Ваша_фамилия")
    driver.find_element(By.NAME, "USER_NAME").send_keys("Ваше_имя")
    driver.find_element(By.NAME, "USER_EMAIL").send_keys(temp_email)
    driver.find_element(By.ID, "password").send_keys("123456")
    driver.find_element(By.ID, "confirmPassword").send_keys("123456")
    driver.find_element(By.XPATH, "//*[@id=\"register_form\"]/div[1]/div[17]/div/label[1]").click()
    driver.find_element(By.XPATH, "//*[@id=\"register_form\"]/div[1]/div[17]/div/label[2]").click()
    registration_button = driver.find_element(By.CSS_SELECTOR, "input.button.button--primary.button--block[type='submit']")
    time.sleep(5)
    pyautogui.scroll(-100)
    current_x, current_y = pyautogui.position()
    pyautogui.moveTo(627, 916)
    pyautogui.click()
    pyautogui.moveTo(current_x, current_y)

def nonexistent_login(driver, fixture_get_temp_email):
    print("Запуск теста неудачного входа...")
    temp_email = fixture_get_temp_email
    driver.get("https://www.chemodanpro.ru/")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/header/div[2]/div/div/div/div[3]/div/ul/li[7]/a")))
    login_button = driver.find_element(By.XPATH, "/html/body/header/div[2]/div/div/div/div[3]/div/ul/li[7]/a")
    login_button.click()
    wait.until(EC.visibility_of_element_located((By.ID, "USER_LOGIN")))
    driver.find_element(By.ID, "USER_LOGIN").send_keys(temp_email)
    password_input = driver.find_element(By.ID, "USER_PASSWORD")
    password = "123456"
    password_input.send_keys(password)
    login_submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='АВТОРИЗОВАТЬСЯ']")))
    login_submit_button.click()

def register_user(temp_email):
    print("Регистрация пользователя...")
    url = "https://www.chemodanpro.ru/login/?register=yes"  # Замените на адрес страницы регистрации вашего сайта

    payload = {
        "AUTH_FORM": "Y",
        "TYPE": "REGISTRATION",
        "USER_TYPE": "1",
        "USER_NAME": "Тест Пиксель Плюс",
        "USER_LAST_NAME": "Тест Пиксель Плюс",
        "USER_LOGIN": "",
        "USER_EMAIL": temp_email,
        "USER_PASSWORD": "123456",
        "USER_CONFIRM_PASSWORD": "123456",
        "UF_LE_PACC": "",
        "UF_LE_CONTACT": "",
        "UF_LE_PHONE": "",
        "UF_LE_CACC": "",
        "UF_LE_BIK": "",
        "UF_LE_FADDRESS": "",
        "UF_LE_FULLNAME": "",
        "UF_LE_INN": "",
        "UF_LE_KPP": "",
        "UF_LE_ADDRESS": "",
        "PL_CHEMODANPRO": "Y",
        "UF_CONFIRM_NOTIF": "Y",
        "UF_CONFIRM_NOTIF_EMAIL": "Y",
        "UF_CONFIRM_RULES": "Y",
        "Register": "РЕГИСТРАЦИЯ"
    }

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        print("Регистрация прошла успешно!")
        print(response.status_code)
    else:
        print("Ошибка при регистрации. Статус код:", response.status_code)
        print(temp_email)
