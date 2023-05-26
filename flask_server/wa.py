from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options


options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument(
    f"user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3312.0 Safari/537.36"
)
driver = webdriver.Chrome(executable_path="/home/ubuntu/chromedriver", options=options)

# Open WhatsApp URL in chrome browser
driver.get("https://web.whatsapp.com/")
init_wait = WebDriverWait(driver, 15)
wait = WebDriverWait(driver, 40)

wa_list = []
wa_status = 0


def send_attach_msg(img, msg, doc=None):

    global driver

    # Locate attachment button through x_path
    time.sleep(12)
    clip_button = init_wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-icon='clip']"))
    )

    ##Sending Attachments
    image_xpath = "/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div[1]/div/ul/li[1]/button/input"
    doc_xpath = "/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div[1]/div/ul/li[4]/button/input"

    # send image
    clip_button.click()
    time.sleep(0.5)
    driver.find_element_by_xpath(image_xpath).send_keys(img)
    send_button = wait.until(
        lambda driver: driver.find_element_by_css_selector("._1w1m1")
    )

    for line in msg.split("\n"):
        ActionChains(driver).send_keys(line).perform()
        ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(
            Keys.SHIFT
        ).key_up(Keys.ENTER).perform()

    time.sleep(1.7)
    ActionChains(driver).send_keys(Keys.RETURN).perform()

    # send Document
    if doc:
        time.sleep(2)
        clip_button = init_wait.until(
            lambda driver: driver.find_element_by_css_selector("span[data-icon='clip']")
        )
        clip_button.click()
        time.sleep(0.3)
        driver.find_element_by_xpath(doc_xpath).send_keys(doc)
        send_button = wait.until(
            lambda driver: driver.find_element_by_css_selector("._1w1m1")
        )
        send_button.click()

    time.sleep(5)


msgs_attch = (
    [
        "/home/ubuntu/ascent/flask_server/location_video.mp4",
        f"""*Own your Dream Home near Veer Surendra Sai Airport at our 10 Acre project - Airport Enclave , Jharsuguda* - airportenclave.com""",
    ],
    [
        "/home/ubuntu/ascent/flask_server/explain_video.mp4",
        """Book your *4BHK Duplex Villa at our Gated Society - Airport Enclave, Jharsuguda* @ 85 Lacs only

📞 Call :
*7735383236 , 8094011162*""",
    ],
)


def wa_sched_job():
    print("Started Kernel ---->>> ")
    global wa_status, wa_list

    if wa_status or len(wa_list) == 0:
        print(f"Kernel BUSY : {wa_status} or no Leads to send WA : {len(wa_list)}!!!")
        return "Kernel Busy"

    else:
        print("Starting WA SENDING !!!")
        # set kernel to busy
        wa_status = 1

        for mob in wa_list:
            print(f"Opening page for : {mob}")
            driver.get(f"https://web.whatsapp.com/send?phone={mob}")
            time.sleep(7)

            # Check if number is on whatsapp else skip
            try:
                error_box = init_wait.until(
                    lambda driver: driver.find_element_by_xpath(
                        "// div[contains(text(),'Phone number shared via url is invalid.')]"
                    )
                )
                print(f"ERROR -- >  {mob}")
                wa_list.remove(mob)
                continue
            except:
                pass

            print("Sending messages ---")
            # send videos with text
            send_attach_msg(*msgs_attch[0])
            send_attach_msg(
                *msgs_attch[1],
                doc="/home/ubuntu/ascent/flask_server/brochure_ariport_enclave_6.pdf",
            )

            wa_list.remove(mob)

        # job completed so switch off
        wa_status = 0
        print(f"Swtiched off kernel : {wa_status}")
