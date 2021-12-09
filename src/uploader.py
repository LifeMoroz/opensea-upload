import os
import time
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By


class Uploader:
    def __init__(self):
        # Get the base directories
        bin_base = os.path.join(os.getcwd(), "bin")
        chromedriver_path = os.path.join(bin_base, "chromedriver")
        ext_path = os.path.join(bin_base, "metamask.crx")
        self.__METAMASK_URL = "chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html"
        self.__METAMASK_ID = "nkbihfbeogaeaoehlefnkodbefgpgknn"
        self.__collection_url = ""

        # Initialize the driver
        opt = webdriver.ChromeOptions()
        opt.add_extension(extension=ext_path)
        opt.add_argument("--log-level=3")
        self.__driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=opt)

        # Close the metamask popup and navigate back to the correct window
        sleep(4)
        self.__driver.switch_to.window(self.__driver.window_handles[0])
        self.__driver.close()
        self.__driver.switch_to.window(self.__driver.window_handles[0])

    def connect_metamask(self, seed_phrase: str, password: str):
        """
        Connect to Metamask
        """

        # Navigate to metamask screen
        self.__driver.get(f"{self.__METAMASK_URL}#initialize/welcome")
        sleep(1)

        # Skip through wallet setup screen
        self.__driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/button').click()
        self.__driver.find_element(
            By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div[2]/div/div[2]/div[1]/button'
        ).click()
        self.__driver.find_element(
            By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[5]/div[1]/footer/button[1]'
        ).click()
        sleep(0.5)

        # Enter wallet seed phrase and password
        self.__driver.find_element(
            By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/form/div[4]/div[1]/div/input'
        ).send_keys(seed_phrase)
        self.__driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)
        self.__driver.find_element(By.XPATH, '//*[@id="confirm-password"]').send_keys(password)
        self.__driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/form/div[7]/div').click()
        self.__driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/form/button').click()
        sleep(2)

    def set_network(self, rpc_url: str, chain_id: int, preconfigured_network: int = None):
        """
        Sets the specified network to Metamask and selects it. Also adds it if it is not a default network.
        """

        # Go to the networks tab
        self.__driver.get("data:")
        sleep(1)
        self.__driver.get(f"{self.__METAMASK_URL}#settings/networks")
        sleep(2)

        # Choose one of the preconfigured networks if specified
        if preconfigured_network is None:
            self.__driver.find_element(
                By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[1]/div/button'
            ).click()
            self.__driver.find_element(
                By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/label/input'
            ).send_keys("Network")
            self.__driver.find_element(
                By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/label/input'
            ).send_keys(rpc_url)
            self.__driver.find_element(
                By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[3]/label/input'
            ).send_keys(chain_id)
            self.__driver.find_element(
                By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[3]/button[2]'
            ).click()
            preconfigured_network = 7
        else:
            # Select the network
            self.__driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[1]/div/div[2]/div[1]/div').click()
            self.__driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div[1]/div[3]/span/a').click()

            self.__driver.find_element(
                By.XPATH,
                '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div[2]/div[7]/div[2]/div/div/div[1]/div[2]/div',
            ).click()
            self.__driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[1]/div/div[2]/div[1]/div').click()
            sleep(1)
            self.__driver.find_element(
                By.XPATH, f'//*[@id="app-content"]/div/div[2]/div/div[2]/div/li[{preconfigured_network}]'
            ).click()
        sleep(2)

    def open_metamask(self):
        """
        Open Metamask in new window
        """

        # Open the extension in a new tab and switch back
        self.__driver.execute_script("window.open('');")
        self.__driver.switch_to.window(self.__driver.window_handles[1])
        self.__driver.get(f"chrome-extension://{self.__METAMASK_ID}/popup.html")
        self.__driver.switch_to.window(self.__driver.window_handles[0])

    def __metamask_execute(self, fn):
        """
        Execute an operation within Metamask and then switch back
        """

        self.__driver.switch_to.window(self.__driver.window_handles[1])
        self.__driver.refresh()
        sleep(2)
        fn()
        sleep(2)
        self.__driver.switch_to.window(self.__driver.window_handles[0])

    def connect_opensea(self, test: bool):
        """
        Connect OpenSea with Metamask
        """

        self.__driver.get("https://testnets.opensea.io/login" if test else "https://opensea.io/login")
        sleep(2)
        self.__driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/main/div/div/div/div[2]/ul/li[1]/button').click()
        sleep(1)

        def connect():
            self.__driver.find_element(
                By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div[2]/div[4]/div[2]/button[2]'
            ).click()
            self.__driver.find_element(
                By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div[2]/div[2]/div[2]/footer/button[2]'
            ).click()
            sleep(2)

        self.__metamask_execute(connect)

    def sign_transaction(self):
        def sign():
            try:
                self.__driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[3]/button[2]').click()
            except Exception:
                self.__driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div[3]/button[2]').click()
            sleep(1)

        self.__metamask_execute(sign)

    def set_collection_url(self, collection_url: str):
        """
        Sets the OpenSea collection URL to upload to
        """

        self.__collection_url = collection_url

    def upload(self, data):
        """
        Upload a single NFT to OpenSea.
        """

        # Add an item to the collection
        self.__driver.get(f"{self.__collection_url}/assets/create")
        sleep(1)

        # Input the data
        self.__driver.find_element(By.XPATH, '//*[@id="media"]').send_keys(data["image"])
        self.__driver.find_element(By.XPATH, '//*[@id="name"]').send_keys(data["name"])
        self.__driver.find_element(
            By.XPATH, '//*[@id="main"]/div/div/section/div/form/section/div[1]/div/div[2]/button'
        ).click()
        time.sleep(0.5)
        for i, attribute in enumerate(data["attributes"], start=1):
            self.__driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/section/button").click()
            self.__driver.find_element(
                By.XPATH, f"/html/body/div[2]/div/div/div/section/table/tbody/tr[{i}]/td[1]/div/div/input"
            ).send_keys(attribute["trait_type"])

            self.__driver.find_element(
                By.XPATH, f"/html/body/div[2]/div/div/div/section/table/tbody/tr[{i}]/td[2]/div/div/input"
            ).send_keys(attribute["value"])
        self.__driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/footer/button").click()
        time.sleep(0.5)

        # =================================
        # Add your other NFT metadata here
        # =================================

        self.__driver.find_element(
            By.XPATH, '//*[@id="main"]/div/div/section/div[2]/form/div[9]/div[1]/span/button'
        ).click()
        sleep(2)

    def sell(self):
        self.__driver.find_element(By.XPATH, "/html/body/div[5]/div/div/div/div[2]/button/i").click()
        time.sleep(1)
        self.__driver.find_element(By.XPATH, '//*[@id="main"]/div/div/div[1]/div/span[2]/a').click()
        time.sleep(2)
        self.__driver.find_element(
            By.XPATH, '//*[@id="main"]/div/div/div[2]/div/div[1]/div/form/div[1]/div/div[2]/div/div/div[2]/input'
        ).send_keys(0.042)
        self.__driver.find_element(By.XPATH, '//*[@id="main"]/div/div/div[2]/div/div[1]/div/form/div[5]/button').click()
        time.sleep(2)
        self.__driver.find_element(
            By.XPATH, "/html/body/div[4]/div/div/div/section/div/div/section/div/div/div/div/div/div/div/button"
        ).click()
        time.sleep(1)
        self.sign_transaction()

    def close(self):
        for window_handle in self.__driver.window_handles:
            self.__driver.switch_to.window(window_handle)
            self.__driver.close()
