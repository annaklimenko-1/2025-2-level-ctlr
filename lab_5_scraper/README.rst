.. _scraper-label:

Laboratory work №5. Retrieve raw data from World Wide Web
=========================================================

.. toctree::
    :maxdepth: 1
    :titlesonly:
    :caption: Full API

    lab_5_scraper.api.rst

Python competencies required to complete this tutorial:

   -  working with external dependencies, going beyond Python standard library;
   -  working with external modules: local and downloaded from PyPi;
   -  working with files: create/read/update;
   -  downloading web pages;
   -  parsing web pages as HTML structure.

Scraping as a process contains the following steps:

1. Crawling the website and collecting all pages that satisfy criteria
   given.
2. Downloading selected pages content.
3. Extracting specific content from pages downloaded.
4. Saving necessary information.

As a part of the first milestone, you need to implement scraping logic
as a ``scraper.py`` module. When it is run as a standalone Python
program, it should perform all aforementioned stages.

Executing scraper
------------------

Example execution (``Windows``):

.. code:: bash

   python scraper.py

Expected result:

1. ``N`` articles from the given URL are parsed.
2. All articles are downloaded to the ``tmp/articles`` directory.
   ``tmp`` directory should conform to the following structure:

.. code:: text

   +-- 2025-2-level-ctlr
       +-- tmp
           +-- articles
               +-- 1_raw.txt     <- the paper with the ID as the name
               +-- 1_meta.json   <- the paper meta-information
               +-- ...

.. note:: When using CI (Continuous Integration), generated
          ``raw-dataset.zip`` is available in build artifacts. Go to
          ``Actions`` tab in GitHub UI of your fork, open the last job and if
          there is an artifact, you can download it.

Configuring scraper
--------------------

Scraper behavior is fully defined by a configuration file that is
called ``scraper_config.json`` and it is placed at the same level as
``scraper.py``. It is JSON file, simply speaking it is a set of
key-value pairs.

+-------------------------------------+-------------------------------------+---------+
| Config parameter                    | Description                         | Type    |
+=====================================+=====================================+=========+
| ``seed_urls``                       | Entry points for crawling.          | ``list``|
|                                     | Can contain several URLs as there   |         |
|                                     | is no guarantee that                |         |
|                                     | there will be enough article        |         |
|                                     | links on a single page              |         |
|                                     | For example, ``[                    |         |
|                                     | "https://www.nn.ru/text/?page=2",   |         |
|                                     | "https://www.nn.ru/text/?page=3"]`` |         |
+-------------------------------------+-------------------------------------+---------+
| ``headers``                         | Headers let you pass additional     | ``dict``|
|                                     | information                         |         |
|                                     | within request to the web page.     |         |
|                                     | For example,                        |         |
|                                     | ``{"user-agent": "Mozilla/5.0"}``   |         |
+-------------------------------------+-------------------------------------+---------+
| ``total_articles_to_find_and_parse``| Number of articles to parse.        | ``int`` |
|                                     | Range: ``0<x<=150``.                |         |
+-------------------------------------+-------------------------------------+---------+
| ``encoding``                        | This parameter specifies encoding   | ``str`` |
|                                     | for the                             |         |
|                                     | response received by the web page   |         |
|                                     | you request. For example, ``utf-8``.|         |
+-------------------------------------+-------------------------------------+---------+
| ``timeout``                         | The amount of time you wait for a   | ``int`` |
|                                     | response from your web page.        |         |
|                                     | If the page does not respond in the |         |
|                                     | specified time, an exception will   |         |
|                                     | be received.                        |         |
|                                     | Range: ``0<x<=60``.                 |         |
+-------------------------------------+-------------------------------------+---------+
| ``should_verify_certificate``       | Parameter that enables or disables  | ``bool``|
|                                     | the security certificate check      |         |
|                                     | of your requests to the page.       |         |
|                                     | Disable it if you cannot pass       |         |
|                                     | web page security certification.    |         |
|                                     | For example, ``true`` or ``false``. |         |
+-------------------------------------+-------------------------------------+---------+
| ``headless_mode``                   | Not used.                           |         |
+-------------------------------------+-------------------------------------+---------+

.. note:: ``seed_urls`` and ``total_articles_to_find_and_parse`` are used
          in :py:class:`lab_5_scraper.scraper.Crawler` abstraction.
          ``headers``, ``encoding``, ``timeout``, ``should_verify_certificate`` are used
          in :py:func:`lab_5_scraper.scraper.make_request` function.
          ``headless_mode`` is used only if you work with dynamic websites. See
          definition and requirements for these abstractions and functions
          within further steps.

Assessment criteria
-------------------

You state your ambitions on the mark by editing ``target_score`` parameter
in ``settings.json`` file. Possible values are ``4``, ``6``,
``8``, and ``10``. See example below:

.. code:: bash

   6

would mean that you have made tasks for mark ``6`` and request mentors
to check if you can get it. See mark requirements and explanations
below:

1. Desired mark **4**:

   1. ``pylint`` level: ``5/10``.
   2. Scraper validates config and fails appropriately if the latter is
      incorrect.
   3. Scraper downloads articles from the selected newspaper.
   4. Scraper produces only ``_raw.txt`` files in the ``tmp/articles``
      directory (*no metadata files*).

2. Desired mark **6**:

   1. ``pylint`` level: ``7/10``.
   2. All requirements for the mark **4**.
   3. Scraper produces ``_meta.json`` files for each article, however,
      it is allowed for each meta file to contain reduced number of
      keys: ``id``, ``title``, ``author``, ``url``.

3. Desired mark **8**:

   1. ``pylint`` level: ``10/10``.
   2. All requirements for the mark **6**.
   3. Scraper produces ``_meta.json`` files for each article, meta file
      should be full: ``id``, ``title``, ``author``, ``url``, ``date``,
      ``topics``. In contrast to the task for mark **6**, it is
      mandatory to collect a date for each of the articles in the
      appropriate format.

4. Desired mark **10**:

   1. ``pylint`` level: ``10/10``;
   2. All requirements for the mark **8**.
   3. Given just one seed url, crawler can find and visit all website
      pages requested.

.. note:: Date should be in the special format.
          Read :ref:`dataset-label` for technical details.

Implementation tactics
----------------------

All logic for instantiating and using needed abstractions
should be implemented in a special block of the module ``scraper.py``.

.. code:: py

   if __name__ == '__main__':
      print('Your code goes here')

Stage 0. Choose the media
~~~~~~~~~~~~~~~~~~~~~~~~~

Start your implementation by selecting a website you are going to scrape.
Pick the website that interests you the most. If you plan on working on
a mark higher than **4**, make sure all the necessary information is
present on your chosen website.

Stage 1. Extract and validate config first
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Stage 1.1. Use ``ConfigDTO`` abstraction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You are provided with :py:class:`core_utils.config_dto.ConfigDTO` abstraction.
It is located in ``core_utils`` package.
Use it to store you scraper configuration data from ``scraper_config.json``.
Examine class fields closely.

For more information about DTO object fields refer to description of
scraper configuration parameters above.

.. tip:: DTO is a short for Data Transfer Object. It is commonly used
         term and programming pattern. You may read more about DTO
         `here <https://www.okta.com/identity-101/dto/>`__.

Stage 1.2. Introduce Config abstraction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To be able to read, validate, and use scraper configuration data inside
your program you need to implement special
:py:class:`lab_5_scraper.scraper.Config` abstraction that
is responsible for extracting and validating data from
``scraper_config.json`` file.

See the intended instantiation:

.. code:: py

   configuration = Config(path_to_config=CRAWLER_CONFIG_PATH)

where ``CRAWLER_CONFIG_PATH`` is the path to the config of the crawler.
It is mandatory to initialize :py:class:`lab_5_scraper.scraper.Config` class
instance with passing a global variable ``CRAWLER_CONFIG_PATH``
that should be properly imported from the ``core_utils/constants.py`` module.

Stage 1.3. Extract configuration data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To be able to use scraper configuration data inside your program you
need to define :py:meth:`lab_5_scraper.scraper.Config._extract_config_content`
method for extracting configuration data.

The method should open configuration file, create and fill the
:py:class:`core_utils.config_dto.ConfigDTO` instance with
all configuration parameters filled.

.. note:: This method returns a :py:class:`core_utils.config_dto.ConfigDTO`
          instance. It can be called both from
          :py:meth:`lab_5_scraper.scraper.Config._validate_config_content`
          (for validation purposes) and from
          :py:meth:`lab_5_scraper.scraper.Config`
          (to store validated values in instance attributes).

Stage 1.4. Validate configuration data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:py:class:`lab_5_scraper.scraper.Config` class is responsible
not only for configuration data extraction, but for its validation as well.
Hence you need to implement
:py:meth:`lab_5_scraper.scraper.Config._validate_config_content` method.

Inside the method you need to define and check formal criteria for valid
configuration. When config is invalid:

1. One of the following errors is thrown:

   -  ``IncorrectSeedURLError``: seed URL does not match standard
      pattern ``"https?://(www.)?"``;
   -  ``NumberOfArticlesOutOfRangeError``: total number of articles is
      out of range from 1 to 150;
   -  ``IncorrectNumberOfArticlesError``: total number of articles to
      parse is not integer or less than 0;
   -  ``IncorrectHeadersError``: headers are not in a form of
      dictionary;
   -  ``IncorrectEncodingError``: encoding must be specified as a
      string;
   -  ``IncorrectTimeoutError``: timeout value must be a positive
      integer less than 60;
   -  ``IncorrectVerifyError``: verify certificate and headless mode values must either be
      ``True`` or ``False``.

2. Script immediately finishes execution.

When all validation criteria are passed there is no exception thrown and
program continues its execution.

.. note::
   :py:meth:`lab_5_scraper.scraper.Config._validate_config_content` method
   is called during :py:class:`lab_5_scraper.scraper.Config` class instance
   initialization. Inside this method, you should call
   :py:meth:`lab_5_scraper.scraper.Config._extract_config_content` to load
   configuration data into a :py:class:`core_utils.config_dto.ConfigDTO` instance,
   and then validate the DTO fields against the required criteria.

   This ensures that config is checked before its values are stored in the
   :py:class:`lab_5_scraper.scraper.Config` instance attributes, but the DTO
   is still available for validation within the same method.

Stage 1.5. Provide getting methods for configuration parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To be able to further use configuration data extracted across your
program you need to specify methods for getting each configuration
parameter.

For example, :py:meth:`lab_5_scraper.scraper.Config.get_seed_urls` method
should return seed urls value from scraper config file extracted when needed.
Similar methods should be defined for all scraper configuration parameters that
you will be using across the program.

Stage 2. Set up work environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Stage 2.1. Set up folder for articles
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When config is correct (the :py:class:`lab_5_scraper.scraper.Config`
class instance is initialized meaning config is valid and loaded inside the program),
you should prepare appropriate environment for your scraper to work. Basically,
you must check that a directory provided by ``ASSETS_PATH`` does in fact
exist and is empty. In order to do that, implement
:py:func:`lab_5_scraper.scraper.prepare_environment` function.

It is mandatory to call this function after the config file is validated
and before crawler is run.

.. note:: If folder specified by ``ASSETS_PATH`` is already created and
          filled with some files (for example, from your previous scraper run)
          you need to remove the existing folder and then create an empty
          folder with this name in current method.

Stage 2.2. Set up website requesting function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You will need to make requests inside you program to the website several
times during each scraper run, so it is wise to create service function
making request to your website for reusing across program when needed.
Implement :py:func:`lab_5_scraper.scraper.make_request` function.

.. note:: Inside this function use config getting methods that you should
          have defined previously inside
          :py:class:`lab_5_scraper.scraper.Config` class to get request
          configuration parameters, for example
          :py:meth:`lab_5_scraper.scraper.Config.get_timeout` to get timeout value.

Stage 3. Find necessary number of article URLs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Stage 3.1. Introduce Crawler abstraction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:py:class:`lab_5_scraper.scraper.Crawler` is an entity
that visits ``seed_urls`` with the intention to
collect URLs of the articles that should be parsed later.
**Seed url** - this is a known term, you can read more in
`Wikipedia <https://en.wikipedia.org/wiki/Web_crawler#Overview>`__ or
any other more reliable source of information you trust.

It should be instantiated with the following instruction:

.. code:: py

   crawler = Crawler(config=configuration)

:py:class:`lab_5_scraper.scraper.Crawler` instance saves
provided configuration instance in an attribute
with the corresponding name. Each instance should also have an
additional ``self.urls`` attribute, initialized with empty list.

Stage 3.2. Implement a method for collecting article URLs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once the crawler is instantiated, it can be started by executing its
:py:meth:`lab_5_scraper.scraper.Crawler.find_articles` method.
The method should iterate over the list of seeds, download them and
extract article URLs from it. As a result, the internal attribute
``self.urls`` should be filled with collected URLs.

.. note:: Each URL in ``self.urls`` should be a valid URL, not just a
          suffix. For example, we need
          ``https://www.nn.ru/text/transport/2022/03/09/70495829/`` instead of
          ``text/transport/2022/03/09/70495829/``.

:py:meth:`lab_5_scraper.scraper.Crawler.find_articles` method
must call another method of Crawler:
:py:meth:`lab_5_scraper.scraper.Crawler._extract_url`.
This method is responsible for retrieving a URL from
HTML of the page. Make sure that :py:meth:`lab_5_scraper.scraper.Crawler.find_articles`
only iterates over seed URLs and stores newly collected ones, while all the extraction is
performed via protected :py:meth:`lab_5_scraper.scraper.Crawler._extract_url` method.

.. warning:: At this point, an approach for extracting articles URLs is
             different for each website.

Finally, to access seed URLs of the crawler,
:py:meth:`lab_5_scraper.scraper.Crawler.get_search_urls` must be employed.

.. note:: It is possible that at some point your crawler will encounter an
          unavailable website (for example, its response code is not 200). In
          such case, your crawler must continue processing the other URLs
          provided. Ensure that your crawler handles such URLs without throwing
          an exception.

Some web resources load new articles only after a user performs a
special interaction (for example, scrolling or button pressing). If this
is your case, refer to :ref:`dynamic-scraping-label`.

Stage 4. Extract data from every article page
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Stage 4.1. Introduce ``HTMLParser`` abstraction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:py:class:`lab_5_scraper.scraper.HTMLParser` is an entity
that is responsible for extraction of all
needed information from a single article web page.
Parser is initialized the following way:

.. code:: py

   parser = HTMLParser(full_url=full_url, article_id=i, config=configuration)

:py:class:`lab_5_scraper.scraper.HTMLParser` instance
saves all constructor arguments in attributes with corresponding names.
Each instance should also have an additional ``self.article`` attribute,
initialized with a new instance of
:py:class:`core_utils.article.article.Article` class.

:py:class:`core_utils.article.article.Article` is an abstraction
that is implemented for you. You must use it
in your implementation. A more detailed description of the Article class
can be found in :ref:`ctlr-article-label`.

Stage 4.2. Implement main ``HTMLParser`` method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :py:class:`lab_5_scraper.scraper.HTMLParser`
interface includes a single
:py:meth:`lab_5_scraper.scraper.HTMLParser.parse` method that
encapsulates the logic of extracting all necessary data from the article
web page. It should do the following:

1. Download the web page.
2. Initialize ``BeautifulSoup`` object on top of downloaded page (we
   will call it ``article_bs``).
3. Fill :py:class:`core_utils.article.article.Article` instance
   by calling private methods to extract text (more details in the next sections).

The :py:meth:`lab_5_scraper.scraper.HTMLParser.parse` method returns
the instance of :py:class:`core_utils.article.article.Article` that is
stored in ``self.article`` field.

Stage 4.3. Implement extraction of text from article page
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Extraction of the text should happen in the private
:py:meth:`lab_5_scraper.scraper.HTMLParser._fill_article_with_text` method.

A call to this method results in filling the internal
:py:class:`core_utils.article.article.Article` instance with text.

.. note:: It is very likely that the text on pages of a chosen website is
          split across different HTML blocks, make sure to collect text from
          them all.

Stage 5. Save article
~~~~~~~~~~~~~~~~~~~~~

.. important:: **Stages 0-5** are required to get the mark **4**.

Make sure that you save each :py:class:`core_utils.article.article.Article`
object as a text file on the file system by using the appropriate
API method :py:func:`core_utils.article.io.to_raw` from ``io.py`` module.
Read more in :ref:`ctlr-article-label`.

As we return the :py:class:`core_utils.article.article.Article` instance
from the :py:meth:`lab_5_scraper.scraper.HTMLParser.parse` method, saving
the article is out of scope of an :py:class:`lab_5_scraper.scraper.HTMLParser`.
This means that you need to save the articles in the place where you call
:py:meth:`lab_5_scraper.scraper.HTMLParser.parse`.

Stage 6. Collect basic article metadata
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. important:: **Stages 0-6** are required to get the mark **6**.

According to the :ref:`dataset-label`, the
dataset that is generated by your code should contain meta-information
about each article including its id, title, author.

Implement
:py:meth:`lab_5_scraper.scraper.HTMLParser._fill_article_with_meta_information`
method. A call to this method results in filling the internal
:py:class:`core_utils.article.article.Article` instance with meta-information.

.. note:: Authors must be saved as a list of strings.
          If there is no author in your newspaper, fill the field with a
          list with a single string “NOT FOUND”.

To save the collected meta-information, refer
:py:func:`core_utils.article.io.to_meta` method.
Saving must be performed outside of parser methods.

Stage 7. Collect advanced metadata: publication date and topics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There is plenty of information that can be collected from each page,
much more than title and author. It is very common to also collect
publication date. Working with dates often becomes a nightmare for a
data scientist. It can be represented very differently: ``2009Feb17``,
``2009/02/17``, ``20130623T13:22-0500``, or even ``48/2009`` (do you
understand what 48 stand for?).

The task is to ensure that each article metadata is extended with dates.
However, the task is even harder as you have to follow the required
format. In particular, you need to translate it to the format shown by
example: ``2021-01-26 07:30:00``. For example, in `this
paper <https://www.nn.ru/text/realty/2021/01/26/69724161/>`__ it is
stated that the article was published at ``26 ЯНВАРЯ 2021, 07:30``, but
in the meta-information it must be written as\ ``2021-01-26 07:30:00``.

To correctly process the date, implement
:py:meth:`lab_5_scraper.scraper.HTMLParser.unify_date_format`
method.

.. hint:: Use `datetime <https://docs.python.org/3/library/datetime.html>`__
          module for such manipulations. In particular, you need to parse the
          date from your website that is represented as a string and transform
          it to the instance of ``datetime``. For that it might be useful to
          look into `datetime.datetime.strptime() <https://docs.python.org/3/library/
          datetime.html#strftime-strptime-behavior>`__ method.

Except for that, you are also expected to extract information about
topics, or keywords, which relate to the article you are parsing. You
are expected to store them in a meta-information file as a list-like
value for the key ``topics``. In case there are not any topics or
keywords present in your source, leave this list empty.

You should extend
:py:meth:`lab_5_scraper.scraper.HTMLParser._fill_article_with_meta_information`
method with a call to :py:meth:`lab_5_scraper.scraper.HTMLParser.unify_date_format`
method and topics extraction.

Stage 8. Determine the optimal number of seed URLs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. important:: **Stages 0-8** are required to get the mark **8**.

As it was stated in **Stage 2.1**,
:py:class:`lab_5_scraper.scraper.Crawler` is an entity that visits
``seed_urls`` with the intention to collect URLs with articles that
should be parsed later. Often you can reach the situation when there
are not enough article links on the given URL. For example, you may want
to collect 100 articles whereas each newspaper page contains links to
only 10 articles. This brings the need in at least 10 seed URLs to be
used for crawling. At this stage you need to ensure that your Crawler is
able to find and parse the required number of articles. Do this by
determining exactly how many seed URLs it takes.

As before, such settings are specified in the config file.

.. important:: Ensure you have enough seeds in your configuration file to
               get at least 100 articles in your dataset. 100 is a required number
               of papers for the final part of the course.

Stage 9. Turn your crawler into a real recursive crawler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Crawlers used in production or even just for collection of documents
from a website should be much more robust and tricky than what you have
implemented during the previous steps. To name a few challenges:

1. **Content is not in HTML**. Yes, it can happen that your website is an
   empty HTML by default and content appears dynamically when you click,
   scroll, etc. For example, many pages have so-called virtual scroll,
   it is when new content appears when you scroll the page. You can
   think of feed in VKontakte, for example.
2. **The website’s defense against your crawler**. Even if data is public,
   your crawler that sends thousands of requests produces huge load on
   the server and exposes risks for business continuity. Therefore,
   websites may reject too much traffic of suspicious origins.
3. **There may be no way to specify seed URLs - due to website size or
   budget constraints**. Imagine you need to collect 100k articles of the
   Wikipedia. Do you think you would be able to copy-paste enough seeds?
   How about the task of collection 1M articles?
4. **Software and hardware limitations and accidents**. Imagine you have
   your crawler running for 24 hours, and it crashes. If you have not
   mitigated this risk, you lose everything and have to restart your
   crawler.

And we are not talking about such objective challenges as impossibility
of building universal crawlers.

Therefore, your **Stage 9** is about addressing some of these questions. In
particular, you need to implement your crawler in a recursive manner:
you provide a single seed url of your newspaper, and it visits every
page of the website and collects *all* articles from the website. You
need to make a child of :py:class:`lab_5_scraper.scraper.Crawler` class and name it
:py:class:`lab_5_scraper.scraper.CrawlerRecursive`.
Follow the interface of :py:class:`lab_5_scraper.scraper.Crawler`.

A required addition is an ability to stop crawler at any time. When it
is started again, it continues search and crawling process without
repetitions.

.. hint:: Think of storing intermediate information in one or few files?
          What information do you need to store?

Stage 9.1. Introduce ``CrawlerRecursive`` abstraction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:py:class:`lab_5_scraper.scraper.CrawlerRecursive` must inherit
from :py:class:`lab_5_scraper.scraper.Crawler`.
The initialization interface is the same as for :py:class:`lab_5_scraper.scraper.Crawler`.
During initialization, make sure to create a ``self.start_url`` field:
it is a single URL that will be used as a seed.
Fill ``self.start_url`` with one of the seed URLs
presented in the configuration instance.

Stage 9.2. Re-implement ``find_articles`` method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. important:: **Stages 0-9.2** are required to get the mark **10**.

The key idea of recursive crawling is collecting a required number of
URLs (however large it may be) given just one seed URL. It can be
achieved in the following way:

1. Extract all the available URLs from the seed URL provided.

    1. If the number of extracted URLs is smaller than the required number,
       extract all the available URLs from the URLs
       that were extracted during the previous step.

2. Repeat this process until the desired number of URLs is found.

.. hint:: :py:meth:`lab_5_scraper.scraper.CrawlerRecursive.find_articles`
          must be called inside the
          :py:meth:`lab_5_scraper.scraper.CrawlerRecursive.find_articles`.

FAQ
---

If you still have questions about Lab 5 implementation, or you have
problems with it, we hope you will find a solution in :ref:`ctlr-faq-label`.
