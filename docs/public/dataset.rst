.. _dataset-label:

Dataset requirements
====================

For effective analysis of the collected articles, it is necessary to
organize the data in a consistent way. The description of the structure
and each of the elements of the dataset is provided below.

.. contents:: Content:
   :depth: 2

Structure
---------

.. code:: text

   +-- 2025-2-level-ctlr
       +-- tmp
           +-- articles
               +-- articles
                   +-- 1_raw.txt <- the raw text of the article with the ID as the name
                   +-- 1_meta.json <- the meta-information of the article
                   +-- 1_cleaned.txt <- lowercased text with no punctuation
                   +-- 1_udpipe.conllu <- processed text in the UD format (by UDPipe model)
                   +-- 1_image.png <- POS frequencies bar chart
                   +-- 2_raw.txt
                   +-- 2_meta.json
                   +-- 2_cleaned.txt
                   +-- 2_udpipe.conllu
                   +-- 2_image.png
                   +-- ...
                   +-- 100_raw.txt
                   +-- 100_meta.json
                   +-- 100_cleaned.txt
                   +-- 100_udpipe.conllu
                   +-- 100_image.png

Raw texts
---------

Raw articles texts are stored in ``N_raw.txt`` files where ``N``
corresponds to the index of the article. The text is not preprocessed in
any way.

Example:

.. code:: text

   Красивая - мама красиво, училась в ПДД и ЖКУ по адресу Львовская 10 лет с почтой test .

Processed texts
---------------

Ideally, the dataset consists of three processed texts examples:

-  cleaned text
-  morphological and syntactic annotation from UDPipe model

Cleaned text
~~~~~~~~~~~~

Cleaned texts are stored in ``N_cleaned.txt`` files where ``N``
corresponds to the index of the article.

Cleaned text is lowercased and does not include any punctuation.
Word forms are the same as in the raw text.

Example:

.. code:: text

   красивая мама красиво училась в пдд и жку по адресу львовская 10 лет с почтой test

Morphological and syntactic annotation from UDPipe models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Texts with morphological and syntactic annotation
from UDPipe models are stored in ``N_udpipe.conllu`` files
where ``N`` corresponds to the index of the article.

The files contain the following information about the tags: ``ID``,
``FORM``, ``LEMMA``, ``UPOS``, ``XPOS``, ``FEATS``, ``HEAD``, ``DEPREL``,
``DEPS``, and ``MISC``.

.. attention:: Read more about the structure of such files
               in :ref:`ud-format-label` and look at the example files
               for `UDPipe model <https://github.com/fipl-hse/2025-2-level-ctlr/
               blob/main/lab_6_pipeline/tests/test_files/reference_udpipe_test.conllu>`__.

Meta information
----------------

Meta information is stored in files with ``N_meta.json`` names where
``N`` corresponds to the index of the article.

Meta-information includes:

1. Article id (it must match the id of the file)
2. Article URL
3. Article title
4. Article date
5. Article author
6. Article topics
7. Article POS frequencies (Lab 6 for mark 8)
8. Article pattern matches (Lab 6 for mark 10)

Example:

.. code:: json

   {
       "id": 2,
       "url": "https://www.nn.ru/text/style/2023/03/11/72125285/",
       "title": "«Вы актер или батюшка?» Простой рабочий одевается как Пушкин и ходит так на оборонный завод",
       "date": "2023-03-11 17:30:00",
       "author": [
           "Дарья Манохина"
       ],
       "topics": [
           "Стиль и красота"
       ],
       "pos_frequencies": {},
       "pattern_matches": {}
   }

Volume
------

Aim at collecting not less than ``100`` articles from your chosen web source.
