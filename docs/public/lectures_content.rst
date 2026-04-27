.. _ctlr-lectures-label:

Short summary of lectures
=========================

Lecture 1. Introduction to technical track
------------------------------------------

Web scraping as a craft. Place of technical track in overall discipline: conceptually and
assessment formula. Technical track overview. Programming assignment overview.
Client-server architecture in World Wide Web. Request. Response.
Python package manager ``pip``. ``requirements.txt`` as a manifest of project dependencies.

Lecture 2. Headers. HTML structure
----------------------------------

Types of HTTP methods:
``GET``, ``POST``, ``DELETE``, ``PUT``.
Idea of mimicking to human-made requests.
Tip no. 1: random timeouts among calls.
Tip no. 2: sending requests with headers from browser. Obtaining headers from browser.
Basics of HTML structure: hierarchical form, tag as a basic element, properties of tags.

Lecture 3. Search in HTML page
------------------------------

Check for request status: implicit cast to ``bool``, check for status code,
switch on exception raising. Introduction to HTML scraping.
Key strategies for finding elements:
by ``id``, by class, by attribute, by tag name, by child-parent relations, and by combination
of aforementioned approaches. Making requests with ``requests`` API.
`bs4`: installation, basic API. Finding elements in `HTML` page with `find`, `find_all`.
