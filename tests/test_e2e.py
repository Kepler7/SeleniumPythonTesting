from pageObjects.CheckoutPage import CheckoutPage
from pageObjects.HomePage import HomePage
from utilities.BaseClass import BaseClass


class TestOne(BaseClass):

    def test_e2e(self):
        log = self.getLogger()
        homePage = HomePage(self.driver)
        checkout = homePage.clickShop()
        cards = checkout.getCardTitles()
        log.info("Getting all card titles")
        addToCartBtns = checkout.getAddToCartButtons()
        log.info("Getting all add to card buttons")
        try:
            for card, button in zip(cards, addToCartBtns):
                cardText = card.text
                addButton = button
                if cardText == "Blackberry":
                    addButton.click()
                    log.info("add to cart button clicked")
        except:
            print("I was not able to make it")

        confirmationPage = checkout.clickCheckoutButton()
        proto = confirmationPage.clickCheckoutButtonSuccess()






