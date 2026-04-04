.. _ctlr-faq-label:

Frequently asked questions
==========================

.. contents:: Content:
   :depth: 2

Lab 5. Scraper
---------------

I can open my website using browser, but I cannot connect to it via python and get 200 response code.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The golden rule goes as follows: if you can connect to the website with
your browser, you should also be able to connect to it using python, as
it means that the server of the website is working fine. So, it all
comes down to your ability to make your python request as similar to the
human user’s one as possible.

Thus, try adopting some headers, feed ``requests.get()`` cookies from
your own browser after visiting your target website, and wait for a
random amount of seconds in between requests. Experimenting with those
settings should do the trick.

I can successfully connect to my source via requests by running ``scraper.py``, but connection cannot be established when running tests.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In case in scraper.py you feed requests.get() any extra headers or
cookies, or if you program your scraper to wait for a certain time
period in between the requests, you are also expected to modify requests
in test files accordingly. In other words, test files perform the most
basic type of requests with no extra settings, so if you need those
extra settings, you have to add them manually. Check which tests fail,
find what module they belong to, and make your changes there, it is
allowed.

During execution of scraper, error 404 NOT FOUND arises, although seed URLs include valid links only.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This usually happens when the link that is fed to ``requests.get()`` is
constructed incorrectly. Note that many sources place incomplete
versions of URLs to related articles in their HTML code, so you have to
manually modify then before feeding to ``requests.get()``.

For instance,
`this <https://www.nn.ru/text/gorod/2022/05/01/71301596/>`__ ``nn.ru``
article contains the following link in its HTML source:
``/text/gorod/2022/05/01/71300711/``. Before you try to follow it, you
have to restore it to its full format by adding a protocol ``https://``
and a website root ``nn.ru``. As a result, you will get a full link
``https://nn.ru/text/gorod/2022/05/01/71300711/``, which can be safely
fed to ``requests.get()``. Also, sometimes students overdo it and try to
restore already full-formatted links, getting something like
``https://https://nn.ru``, which is obviously also invalid. All in all,
pay attention to what kind of URLs you pass to your ``requests.get()``.

What should I do if not every page of my source contains information about the author?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To get a mark higher than 4, you are expected to collect certain
metadata concerning your articles, including but not limited to their
authors. In case information about the author is missing, you can place
a NOT FOUND token in its place, tests are programmed to recognize this
sequence as valid.

Running tests
-------------

CI checks do not get started after I push my code.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In most cases it means that your pull request has conflicts with the
main branch of the repository. This can happen after updates have been
merges into your pull request by one of the mentors. So, you should
always make sure that you have pulled all the updates from your remote
branch before you commit any new changes to your code, it helps to
prevent such situations.

In the event it has already happened, you have to pull changes to your
local branch, resolve conflicts manually, commit your choices and push
it.

Some tests in CI get canceled without throwing any particular exceptions.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Automated testing works as a chain: in order for certain stages to
start, the previous ones should be successfully completed first. In such
a way, Crawler checks config will not be run until your pull request
passes code style, PR name and spelling checks. If you fail a spelling
check, ask mentors about it as it is likely not your fault. In case of
failing PR name or code style, you have to fix your pull request
according to the message from those stages before you can proceed to the
following checks, and so on.

CI stages get canceled, although the previous steps are completed successfully.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This usually happens in the event that your code takes too much time to
run. Firstly, try to restart checks. Sometimes that is enough.

However, if the issue is still there, closely examine your code for any
bottlenecks, make sure that you do not make any more requests than
necessary, ensure that there are no infinite loops and/or recursion
going on.

Apart from that, verify that you have established a reliable connection
with your target web-source, as sometimes servers stop responding to
automatically generated requests without explicitly rejecting them. This
may cause your program to wait for a response forever, until the time
reserved for the stage runs out.

If you are confident that the problem does not involve your code, make
your situation known to the mentors. There is a chance that it could be
a github malfunction.

When I push my code, I get ``ModuleNotFoundError`` in CI, yet locally everything works fine.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Make sure you have listed all the required libraries that your program
needs in requirements.txt. This directly impacts the way the testing
environment is set in CI.
