.. _dynamic-scraping-label:

How to scrape dynamic web sources
=================================

It is not an uncommon practice for a web sources today to load more
articles dynamically, for example, after a user scrolls or presses a
button. In such cases, it is often impossible to collect a significant
number of articles by just iterating over seed URLs. Alternative
solution would be employing frameworks that are capable of emulating
user activity. One of them is `selenium library <https://www.selenium.dev/>`__.

.. hint:: Follow `instruction <https://www.selenium.dev/
          documentation/webdriver/getting_started/install_drivers/>`__
          to install Chrome driver.

Let’s discuss how to imitate two most popular user activities: scrolling
and button pressing.

What if my web source expects a user to scroll to provide more URLs?
--------------------------------------------------------------------

Firstly, instantiate
`selenium.webdriver.Chrome <https://www.selenium.dev/documentation/webdriver/browsers/chrome/>`__
class. It emulates a native browsing. Save the Chrome instance to the
``driver`` attribute of a Crawler.

.. hint:: To disable a browser window pop-up, add ``headless`` mode
          argument to the ``selenium.webdriver.chrome.options.Options``
          instance. Pass the instance to the ``Chrome`` initialization method.
          Make sure to only do it when the corresponding field in the crawler
          configuration requires it.

Next, to open the page, use ``driver.get`` method.

Example usage:

.. code:: py

   self.driver.get(base_url=https://github.com/)

To perform scroll, execute the corresponding script:

.. code:: py

    self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

To extract resulting page HTML, refer to the driver’s ``page_source``
attribute.

What if my web source requires a user to click buttons to provide more URLs?
----------------------------------------------------------------------------

Just like with scrolling, one should start by instantiating a Chrome
driver (refer to the previous section for more details).

Next, the following steps must be taken. Firstly, it is necessary to
find the clickable buttons with ``driver.find_elements`` methods. Use
`documentation <https://www.selenium.dev/documentation/webdriver/elements/finders/>`__
to determine the arguments to be passed to find the desired elements.
Usually the elements corresponding to buttons possess ``click`` method.
In some cases it is necessary to emulate key pressing. To do this, refer
to ``button.send_keys`` method.

.. hint:: To find the ``send_keys`` argument that corresponds to the
          desired key, refer `here <https://github.com/SeleniumHQ/
          selenium/blob/selenium-4.2.0/py/selenium/webdriver/common/keys.py#L23>`__.

Example usage:

.. code:: py

   button = [button for button in self.driver.find_elements(
             by=By.TAG_NAME, value="button") if button.text == "Ещё"][0]
   button.send_keys(Keys.RETURN)

Sometimes it is necessary to wait until the button becomes clickable. To
perform this via ``selenium``, refer to
``selenium.webdriver.support.wait.WebDriverWait`` and
``selenium.webdriver.support.expected_conditions``.

Example usage:

.. code:: py

   button = WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(button))
