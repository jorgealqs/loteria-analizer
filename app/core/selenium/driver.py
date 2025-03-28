from selenium import webdriver
from selenium.webdriver.chrome.service import Service  # type: ignore
from selenium.webdriver.chrome.options import Options  # type: ignore
from fake_useragent import UserAgent  # type: ignore
import tempfile

CHROMEDRIVER_PATH = "/usr/bin/chromedriver"


def get_selenium_driver():
    """
    Configure and return a Chrome WebDriver instance with custom options.

    Returns:
        webdriver.Chrome: Configured Chrome WebDriver instance
    """
    ua = UserAgent()
    temp_dir = tempfile.mkdtemp()
    options = _get_chrome_options(ua, temp_dir)

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    return driver


def _get_chrome_options(ua: UserAgent, temp_dir: str) -> Options:
    """
    Configure Chrome options for WebDriver.

    Args:
        ua: UserAgent instance for random user agent
        temp_dir: Temporary directory path

    Returns:
        Options: Configured Chrome options
    """
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"user-agent={ua.random}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--lang=en-US,en;q=0.9")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--headless")
    options.add_argument(f"--user-data-dir={temp_dir}")

    return options
