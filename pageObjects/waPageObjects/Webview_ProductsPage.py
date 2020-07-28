import csv

from selenium.webdriver.common.by import By

from utilities.BaseClass import BaseClass


class Webview_ProductsPage(BaseClass):

    def __init__(self, driver):
        self.driver = driver
        self.verifyPresence(Webview_ProductsPage.PRODUCT_TILES_XPATH)

    PRODUCT_TILES_XPATH = (By.XPATH, '//div[contains(@id,"product-")]')

    def verify_correct_prices_in_products(self, path):
        """
        Compare products prices in webview with the list send by the cliente and verifies proces are correct
        :param path: path of the csv file provided by the client that includes description of the product and price.
        """
        log = self.getLogger()
        products = self.get_product_tiles()
        names_grams = []
        prices = []
        dict = {}
        for product in products:
            divide_str = product.text.splitlines()
            names_grams.append(divide_str[0])
            amount = divide_str[2].split('$')
            final_price = amount[1].rstrip('0') if '.' in amount[1] else amount[1]
            if final_price[-1] == '.':
                price_final = final_price.split('.')
                prices.append(price_final[0])
            else:
                prices.append(final_price)
        index = 0
        for key in names_grams:
            dict[key] = prices[index]
            index = index + 1
        csvfile = open(path, 'r', newline='')
        obj = csv.reader(csvfile)
        csv_dict = {}
        for row in obj:
            if len(row) < 2:
                continue
            else:
                csv_dict[row[0]] = row[3]
        for prod in dict.keys():
            counter = 0
            for prod_csv in csv_dict.keys():
                prod_trim = "".join(prod.split())
                prod_csv_trim = "".join(prod_csv.split())
                if prod_trim in prod_csv_trim:
                    try:
                        assert dict[prod] == csv_dict[prod_csv]
                        log.info("try : Actual value of " + prod + " is %s" % dict[
                            prod] + ":" + " Expected Value in csv of " + prod_csv +
                                 " is " + csv_dict[prod_csv] + "  found in line:  " + str(counter))
                    except AssertionError:
                        log.error("Actual value of " + prod + " is %s" % dict[
                            prod] + ":" + " Expected Value in csv of " + prod_csv +
                                  " is " + csv_dict[prod_csv] + " found in line: " + str(counter))
                else:
                    counter = counter + 1
                    if counter > 500:
                        log.info(" ***************************************** " + prod + " not in list ")

    def get_product_tiles(self):
        """ Returns a list of elements that matches the product tile locator.
        """
        return self.driver.find_elements(*Webview_ProductsPage.PRODUCT_TILES_XPATH)


