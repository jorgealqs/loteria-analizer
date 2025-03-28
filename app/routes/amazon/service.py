from app.core.selenium.driver import get_selenium_driver
from app.routes.amazon.schemas import AmazonProductResponse
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.support.ui import WebDriverWait  # type: ignore
from selenium.webdriver.support import (  # type: ignore
    expected_conditions as EC
)
from selenium.common.exceptions import (  # type: ignore
    TimeoutException, NoSuchElementException
)


class AmazonScraperService:
    BASE_URL = "https://www.amazon.com/dp/"

    async def get_product_info(self, asin: str) -> AmazonProductResponse:
        driver = get_selenium_driver()
        try:
            product_info = self._scrape_product_data(
                driver, f"{self.BASE_URL}{asin}"
            )
            return AmazonProductResponse(**product_info)
        finally:
            driver.quit()

    def _scrape_product_data(self, driver, url: str) -> dict:
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        return {
            "title": self._get_title(wait),
            "price": self._get_price(wait, driver),
            "availability": self._get_availability(wait),
            "reviews": self._get_reviews(wait)
        }

    def _get_title(self, wait: WebDriverWait) -> str:
        try:
            element = wait.until(
                EC.presence_of_element_located((By.ID, "productTitle"))
            )
            return element.text.strip()
        except TimeoutException:
            return "Not found"

    def _get_price(self, wait: WebDriverWait, driver) -> str:
        try:
            element = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "span.a-price > span.a-offscreen")
                )
            )
            return element.text.strip()
        except TimeoutException:
            try:
                element = driver.find_element(
                    By.CSS_SELECTOR, "span#price_inside_buybox"
                )
                return element.text.strip()
            except NoSuchElementException:
                return "Not available"

    def _get_availability(self, wait: WebDriverWait) -> str:
        try:
            element = wait.until(
                EC.presence_of_element_located((By.ID, "availability"))
            )
            return element.text.strip()
        except TimeoutException:
            return "Not specified"

    def _get_reviews(self, wait: WebDriverWait) -> str:
        try:
            element = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "span#acrCustomerReviewText")
                )
            )
            return element.text.strip()
        except TimeoutException:
            return "Not available"
