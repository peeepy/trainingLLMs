from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
import requests
from bs4 import BeautifulSoup
import argparse
import re

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url',
                        help="Specify the URL to be scraped", required=True)
    parser.add_argument('--s',
                        help="Specify the selector for the posts to be scraped. S = Selector.")
    """parser.add_argument('--a',
                        help='Specify the CSS selector of the author names.')"""
    parser.add_argument('--n', help="Specify the CSS selector to jump to the next thread, if applicable.")
    parser.add_argument('--all', action='store_true',
                        help='Scrape an entire site. Input will be required to allow for navigation.')

    args = parser.parse_args()

    if args.all:
        # Import scrape_all.py
        from scrape_all import *
    else:
        # Set up Firefox webdriver and navigate to the page
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options, executable_path=r'/bin/geckodriver')

        while True:
            # Navigate to the URL
            driver.get(args.url)

            page = requests.get(args.url)
            soup = BeautifulSoup(page.content, 'html.parser')

            find_posts = driver.find_element(By.CSS_SELECTOR, args.s)
            print(find_posts)

            pattern = r'[\\/:*?"<>|]'
            file_title = driver.title
            filename = re.sub(pattern, '', file_title)
            filename += '.txt'
            
            # Extract the text content of the matching div elements
            with open(filename, 'a') as f:
                # for post in find_posts:
                title = driver.title
                """author_element = post.find_element(By.CSS_SELECTOR, args.a)
                if author_element is not None:
                    author = author_element.text
                    content = f'Title: {title} Author: {author} Body: {post}\n\n'
                else:"""
                content = f'Title: {title} Body: {find_posts.text}\n\n'
                f.writelines(content)

            try:
                # Check for the existence of "Next Page" using the provided XPath
                driver.find_element(By.LINK_TEXT, 'Next').click()
                args.url = driver.current_url
            except NoSuchElementException:
                if args.n:
                    new_thread = driver.find_element(By.LINK_TEXT, args.n).click()
                    args.url = driver.current_url
                else:
                    continueScraping = input("Do you want to continue scraping? (y/n): ")
                    if continueScraping == 'y'.lower(): 
                        new_url = input("Enter a new URL to scrape from: ")
                        args.url = new_url
                    else:
                # "Next Page" not found, exit the loop and finish the script
                        break

        # Quit the driver
        driver.quit()