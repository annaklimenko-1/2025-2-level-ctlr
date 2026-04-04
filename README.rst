Technical Track of Computer Tools for Linguistic Research (2024/2025)
=====================================================================

As a part of a compulsory course `Computer Tools for Linguistic
Research <https://nnov.hse.ru/ba/ling/courses/902203327.html>`__ in `National
Research University Higher School of Economics <https://www.hse.ru/>`__.

This technical track is aimed at building basic skills for retrieving
data from external WWW resources and processing it for future linguistic
research. The idea is to automatically obtain a dataset that has a
certain structure and appropriate content, perform morphological
analysis using various natural language processing (NLP) libraries.
Dataset requirements :ref:`dataset-label`.

Instructors:
------------

-  `Klimova Margarita Andreevna <https://www.hse.ru/org/persons/91748436>`__ -
   linguistic track lecturer
-  `Lyashevskaya Olga Nikolaevna <https://www.hse.ru/staff/olesar>`__ -
   linguistic track lecturer
-  `Demidovskij Alexander
   Vladimirovich <https://www.hse.ru/staff/demidovs#sci>`__ - technical
   track lecturer
-  `Uraev Dmitry Yurievich <https://www.hse.ru/org/persons/208529395>`__ -
   technical track practice lecturer
-  `Kashchikhin Andrei Nikolaevich <https://github.com/WhiteJaeger>`__ -
   technical track expert
-  `Zharikov Egor Igorevich <https://t.me/godb0i>`__ - technical track senior
   assistant
-  `Nurtdinova Sofia Alekseevna <https://t.me/sunrielly>`__ - technical track
   assistant
-  `Podpryatova Anna Sergeevna <https://t.me/anpruch>`__ - technical
   track assistant
-  `Khomutova Ekaterina Sergeevna <https://t.me/ekaterina_hom>`__ -
   technical track assistant

Project Timeline
----------------

1. **Scraper**:

   1. Short summary: Your code can automatically parse a media website
      you are going to choose, save texts and its metadata in a proper
      format.
   2. Deadline: **May, 2**.
   3. Format: each student works in their own PR.
   4. Dataset volume: 5-7 articles.
   5. Design document: :ref:`scraper-label`.

2. **Pipeline**:

   1. Short summary: Your code can automatically process raw texts from
      previous step, make point-of-speech tagging and basic
      morphological analysis.
   2. Deadline: **May, 23**.
   3. Format: each student works in their own PR.
   4. Dataset volume: 5-7 articles.
   5. Design document: :ref:`pipeline-label`.

Lectures history
----------------

+------------+---------------------+--------------------------------------------------------------+
| Date       | Lecture topic       | Important links                                              |
+============+================================================+===================================+
| 04.04.2025 | Lecture:            | Lab no. 5 description                                        |
|            | Introduction to     |                                                              |
|            | technical track.    |                                                              |
+------------+---------------------+--------------------------------------------------------------+
| 04.04.2025 | Seminar: Local      | N/A                                                          |
|            | setup. Choose       |                                                              |
|            | website.            |                                                              |
+------------+---------------------+--------------------------------------------------------------+
| 11.04.2025 | Lecture: 3rd party  | N/A                                                          |
|            | libraries. Browser  |                                                              |
|            | headers.            |                                                              |
+------------+---------------------+--------------------------------------------------------------+
| 11.04.2025 | Seminar:            | `Листинг <./seminars/seminar_04_08_2025/try_requests.py>`__. |
|            | ``requests``:   .   |                                                              |
|            | install, API.       |                                                              |
+------------+---------------------+--------------------------------------------------------------+
| 18.04.2025 | Lecture: HTML       | N/A                                                          |
|            | structure. ``bs4``  |                                                              |
|            | library.            |                                                              |
+------------+---------------------+--------------------------------------------------------------+
| 18.04.2025 | Seminar:            | `Листинг <./seminars/seminar_04_17_2025/try_bs.py>`__.       |
|            | ``bs4``:   .        |                                                              |
|            | install, API.       |                                                              |
+------------+---------------------+--------------------------------------------------------------+
| 25.04.2025 | Lecture: Filesystem | N/A                                                          |
|            | with ``pathlib``.   |                                                              |
|            | Dates.              |                                                              |
+------------+---------------------+--------------------------------------------------------------+
| 25.04.2025 | Seminar:            | `Листинг <./seminars/seminar_04_25_2025/try_paths.py>`__.    |
|            | filesystem with     | `Листинг <./seminars/seminar_04_25_2025/try_json.py>`__.     |
|            | ``pathlib``, dates. | `Листинг <./seminars/seminar_04_25_2025/try_dates.py>`__.    |
+------------+---------------------+--------------------------------------------------------------+
| 02.05.2025 | Distant Lab 5       | N/A                                                          |
|            | acceptance for      |                                                              |
|            | defense.            |                                                              |
+------------+---------------------+--------------------------------------------------------------+
| 09.05.2025 | Holidays.           | N/A                                                          |
+------------+---------------------+--------------------------------------------------------------+
| 16.05.2025 | Lecture: text       | `Листинг <./seminars/seminar_05_16_2025/try_udpipe.py>`__.   |
|            | analysis with       | `Листинг <./seminars/seminar_05_16_2025/try_stanza.py>`__.   |
|            | ``udpipe``,         | `Листинг <./seminars/seminar_05_16_2025/try_networkx.py>`__. |
|            | ``stanza``.         |                                                              |
+------------+---------------------+--------------------------------------------------------------+
| 16.05.2025 | Seminar:  Lab 5     | N/A                                                          |
|            | handover.           |                                                              |
+------------+---------------------+--------------------------------------------------------------+
| 23.05.2025 | Seminar:  Lab 6     | N/A                                                          |
|            | handover.           |                                                              |
+------------+---------------------+--------------------------------------------------------------+
| 30.05.2025 | Extra handover day  | N/A                                                          |
|            | (with penalties).   |                                                              |
+------------+---------------------+--------------------------------------------------------------+

You can find a more complete summary from lectures in :ref:`ctlr-lectures-label`.

Technical solution
------------------

+-----------------------+---------------------------+--------------+---------+
| Module                | Description               | Component    | Need to |
|                       |                           |              | get     |
+=======================+===========================+==============+=========+
| `pathlib              | working with file paths   | scraper      | 4       |
| <https://pypi.org     |                           |              |         |
| /project/pathlib/>`__ |                           |              |         |
+-----------------------+---------------------------+--------------+---------+
| `requests <https://   | downloading web pages     | scraper      | 4       |
| pypi.org/project/reque|                           |              |         |
| sts/2.25.1/>`__       |                           |              |         |
+-----------------------+---------------------------+--------------+---------+
| `BeautifulSoup4       | finding information on    | scraper      | 4       |
| <https://pypi.org     | web pages                 |              |         |
| /project/beautifulso  |                           |              |         |
| up4/4.11.1/>`__       |                           |              |         |
+-----------------------+---------------------------+--------------+---------+
| `lxml <https://pypi.  | **optional** parsing HTML | scraper      | 6       |
| org/project/lxml/>`__ |                           |              |         |
+-----------------------+---------------------------+--------------+---------+
| ``datetime``          | working with dates        | scraper      | 6       |
+-----------------------+---------------------------+--------------+---------+
| ``json``              | working with json text    | scraper,     | 4       |
|                       | format                    | pipeline     |         |
+-----------------------+---------------------------+--------------+---------+
| `spacy_udpipe <https: | module for morphological  | pipeline     | 6       |
| //pypi.org/project    | analysis                  |              |         |
| /spacy-udpipe/>`__    |                           |              |         |
+-----------------------+---------------------------+--------------+---------+
| `networkx <https:/    | working with graphs       | pipeline     | 10      |
| /pypi.org/project     |                           |              |         |
| /networkx/>`__        |                           |              |         |
+-----------------------+---------------------------+--------------+---------+

Software solution is built on top of three components:

1. `scraper.py <https://github.com/fipl-hse/2024-2-level-ctlr/blob/main/lab_5_scraper/scraper.py>`__
   - a module for finding articles from the given media, extracting text and dumping it to
   the file system. Students need to implement it.
2. `pipeline.py <https://github.com/fipl-hse/2023-2-level-ctlr/blob/main/lab_6_pipeline/pipeline.py>`__
   - a module for processing text: point-of-speech tagging and basic
   morphological analysis. Students need to implement it.
3. `article.py <https://github.com/fipl-hse/2024-2-level-ctlr/blob/main/core_utils/article/article.py>`__
   - a module for article abstraction to encapsulate low-level manipulations with the article.

Handing over your work
----------------------

1. Lab work is accepted for oral presentation.
2. A student has explained the work of the program and showed it in
   action.
3. A student has completed the mini-task from a mentor that requires some
   slight code modifications.
4. A student receives a mark:

   1. That corresponds to the expected one, if all the steps above are
      completed and mentor is satisfied with the answer.
   2. One point bigger than the expected one, if all the steps above are
      completed and mentor is very satisfied with the answer.
   3. One point smaller than the expected one, if a lab is handed over
      one week later than the deadline and criteria from 4.1 are
      satisfied.
   4. Two points smaller than the expected one, if a lab is handed over
      more than one week later than the deadline and criteria from 4.1
      are satisfied.

.. note:: A student might improve their mark for the lab, if they
          complete tasks of the next level after handing over the lab.

**A lab work is accepted for oral presentation if all the criteria below
are satisfied:**

1. There is a Pull Request (PR) with a correctly formatted name:
   ``Scraper, <NAME> <SURNAME> - <UNIVERSITY GROUP NAME>``.

   1. Example: ``Scraper, Irina Novikova - 20FPL2``.

2. Has a filled file ``settings.json`` with an expected mark.
   Acceptable values: 4, 6, 8, 10.
3. Has green status.
4. Has a label ``done``, set by mentor.

Resources
---------

1. `Academic performance
   <https://docs.google.com/spreadsheets/d/19-TM-fWjZyjSk46TXgnP78cRAJGd3U4jRHw4VtOWYy4/edit?gid=0#gid=0>`__
2. `Media websites list
   <https://docs.google.com/spreadsheets/d/1xScC58eEQBe6PmLuEOSCb09KJC6TpeKd/edit?gid=672060649#gid=672060649>`__
3. `Documentation website <https://fipl-hse.github.io/>`__
4. `Python programming course from previous semester
   <https://github.com/fipl-hse/2024-2-level-labs>`__
5. `Scraping tutorials (Russian) <https://youtu.be/7hn1_t2ZtJQ>`__
6. `Scraping tutorials (English)
   <https://www.youtube.com/playlist?list=PL1jK3K11NINiOn4DdIDVdyQpcU3kaNxl0>`__
7. :ref:`starting-guide-en-label`
8. :ref:`ctlr-tests-label`
9. :ref:`run-in-terminal-label`
10. :ref:`ctlr-faq-label`
