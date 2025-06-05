"""
A command-line interface (CLI) for a Spanish dictionary that 
helps non spanish speakers learn Spanish words and their meanings.
"""
import argparse
import os
import cloudscraper
from google import genai
from bs4 import BeautifulSoup
class Word:
    """
    A class for scraping and representing a word from the RAE (Real Academia Española)
    dictionary website.

    Attributes:
        _url (str): The base URL of the RAE dictionary.

        scraper (cloudscraper.CloudScraper):
        The HTTP scraper instance configured for the specified browser and platform.

        html_response (requests.Response): 
        The HTTP response object containing the HTML of the dictionary page.

        _word (str): The word being represented or scraped.

    Args:
        wordstr (str, optional): The initial word to represent. Defaults to "".
        browser (str, optional): The browser type to emulate for scraping. Defaults to "firefox".
        platform (str, optional): The platform type to emulate for scraping. Defaults to "linux".

    Properties:
        word (str): Gets or sets the current word.
        url (str): Gets or sets the base URL for the dictionary.

    Methods:
        wotd():
            Scrapes and updates the word of the day from the RAE dictionary homepage.
    """
    def __init__(self, wordstr:str = "", browser:str = "firefox", platform:str = "linux"):
        self._url = "https://dle.rae.es"

        self.scraper = cloudscraper.create_scraper(
            browser={
                "browser": f"{browser}",
                "platform": f"{platform}",
            },
        )
        self.html_response = self.scraper.get(url=self.url)
        self._word = wordstr

    @property
    def word(self) -> str:
        """
        Getter for the word property.
        """
        return self._word

    @word.setter
    def word(self, word: str):
        """
        Setter for the word property.
        """
        self._word = word

    @property
    def url(self) -> str:
        """
        Getter for the url property.
        """
        return self._url

    @url.setter
    def url(self, url:str):
        self._url = url


    def wotd(self):
        """
        Extracts the 'word of the day' from the HTML response and
        assigns it to the 'word' attribute.

        Uses BeautifulSoup to parse the HTML content and finds the text within the
        <span> element with class 'c-word-day__word'.

        Raises:
            AttributeError: If the expected element is not found in the HTML.
        """
        soup = BeautifulSoup(self.html_response.text, "html.parser")
        self.word = soup.find("span", class_="c-word-day__word").text

class Dictionary:
    """
    A class for searching word definitions and retrieving the
    word of the day from an online dictionary.

    Methods
    -------
    __init__():
        Initializes the Dictionary instance.

    search_word(target: str):
        Searches for the given word in the dictionary,
        returning its introduction and definitions if found.

        Parameters:
            target (str): The word to search for.
        Returns:
            tuple: (intro_text, definitions) if found,
            or (error_message, []) if not found or on HTTP error.

    get_wotd():
        Retrieves and prints the word of the day, then searches for its definitions.
        Returns:
            tuple: The result of search_word for the word of the day.
    """
    def __init__(self):
        self.soup = None

    def search_word(self, target: str):
        """
        Searches for the given word in the online dictionary,
        retrieves its introduction and definitions.

        Args:
            target (str): The word to search for.

        Returns:
            tuple:
                - str: A message containing the word and its introduction,
                or an error message if not found.

                - list or str: A list of definitions for the word,
                or an empty list if not found or on error.
        """
        word = Word(wordstr=target)

        url = word.url + f"/{target}?m=form"

        html_response = word.scraper.get(url=url)

        if html_response.status_code == 200:
            self.soup = BeautifulSoup(html_response.text, "html.parser")

            if self.soup.find("div", class_="n2 c-text-intro"):
                intro = self.soup.find("div", class_="n2 c-text-intro").text

            else:
                intro = ""

            definitions = self.soup.find_all("li", class_="j")

            if not definitions:
                return f"Word '{target}' not found in the dictionary. Check the spelling.", []

            return f"{target}:\n{intro}", "\n".join([definition.text for definition in definitions])

        else:
            return f"HTTP error code: {html_response.status_code}", []

    def get_wotd(self):
        """
        Retrieves and displays the word of the day.

        This method creates a new Word instance, fetches the word of the day,
        prints a header, and returns the result of searching for the word of the day.

        Returns:
            The result of searching for the word of the day using the search_word method.
        """
        word = Word()
        word.wotd()

        print("Word of the day:\n")
        return self.search_word(word.word)

class Cli:
    """
    Command-line interface (CLI) class for interacting with a dictionary application.
    Attributes:
        dictionary (Dictionary): An instance of the Dictionary class used for word lookups.
        argument (str): The word or phrase to be searched or processed.
        _result (tuple or None): Stores the result of the latest dictionary operation.
    Properties:
        result (tuple or None): Gets or sets the result of the latest dictionary operation.
    Methods:
        print_result(header: str, definitions: str):
            Prints the header and definitions to the console.
        execute_search():
            Searches for the word specified in 'argument'
            using the dictionary and stores the result.

        execute_wotd():
            Retrieves the word of the day from the dictionary and stores the result.

        execute_translation():
            Translates the latest result using a prompt from a file and the Gemini API,
            then prints the translation.
    """
    def __init__(self,  argument:str = ""):
        self.dictionary = Dictionary()
        self.argument = argument
        self._result = None

    @property
    def result(self):
        """
        Getter for the result property.
        """
        return self._result

    @result.setter
    def result(self, result):
        """
        Setter for the result property.
        """
        self._result = result

    def print_result(self, header:str, definitions:str):
        """
        Prints the provided header and definitions to the console.

        Args:
            header (str): The header or title to be printed.
            definitions (str): The definitions or content to be printed below the header.
        """
        print(header)
        print(definitions)

    def execute_search(self):
        """
        Executes a search for the target word using the dictionary instance.

        Retrieves the header and definition for the specified target word (self.argument)
        by calling the dictionary's search_word method. Stores the result as a tuple
        (header, definition) in self.result.
        """
        header, definition = self.dictionary.search_word(target=self.argument)
        self.result = (header, definition)

    def execute_wotd(self):
        """
        Retrieves the word of the day (WOTD) and its definition from the dictionary,
        then stores the result as a tuple (header, definition) in the `self.result` attribute.

        Returns:
            None
        """
        header, definition = self.dictionary.get_wotd()
        self.result = (header, definition)

    def execute_translation(self):
        """
        Executes the translation process by reading a prompt from a file,
        appending the current translation results,
        and sending the combined prompt to the Gemini API for content generation.

        If translation results are available, the method:
            - Reads the prompt from 'prompt.txt'.
            - Appends the source and translated text to the prompt.
            - Sends the prompt to the Gemini API using the specified model.
            - Prints the generated response text.

        If no translation results are found, prints a message and exits.

        Returns:
            None
        """
        if self.result[1]:
            with open("./prompt.txt", "r", encoding="utf-8") as file:
                prompt = file.read()

            prompt = f"{prompt}\n\n{self.result[0]}\n{self.result[1]}"
            client = genai.Client(api_key=os.environ["api_key"])
            response = client.models.generate_content(
                model="gemini-2.0-flash", contents=prompt
            )
            print(response.text)
        else:
            print("No definitions found for the word.")
            return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog= "Spanish dictionary",
                                     description="A spanish dictionary to teach words in " \
                                     "spanish and thgeir meaning.")

    parser.add_argument('-s', '--search', help="Search for the definition of a Spanish word.")
    parser.add_argument('-w', '--wotd',
                        help="Show the word of the day and its definition.",
                        action='store_true')
    parser.add_argument('-t', '--translate',
                        help="Translate the word of the day to English.",
                        action='store_true')

    args = parser.parse_args()

    if args.wotd and args.search:
        print("You can only pick one mode")
        exit()

    if args.wotd:
        cli = Cli()
        cli.execute_wotd()
        if args.translate:
            cli.execute_translation()
        else:
            cli.print_result(*cli.result)

    elif args.search:
        cli = Cli(args.search)
        cli.execute_search()

        if args.translate:
            cli.execute_translation()

        else:
            cli.print_result(*cli.result)

    else:
        print("No valid option picked")
        print("Use -h or --help for more information.")
