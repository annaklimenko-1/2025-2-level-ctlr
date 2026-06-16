Final project. Analyze and correct UD annotation
================================================

Final project is dedicated to using :py:class:`lab_6_pipeline.pipeline.UDPipeAnalyzer`
to process a corpus of texts and correcting mistakes that might be present in the
retrieved UD linguistic annotation.

Stage 0. Create PR
~~~~~~~~~~~~~~~~~~

Start your implementation with creating Pull Request (PR).

.. note::

    There is a Pull Request (PR) with a correctly formatted name:
    ``[PROJECT] Final Project, Team <TEAM NUMBER> - <UNIVERSITY GROUP NAME>``.

    Example: ``[PROJECT] Final Project, Team 7 - 22FPL2``.


Fill in the team number in the ``final_project/settings.json`` and set the
``target_score`` as `10`. For example:

.. code:: json

    {
        "target_score": 10,
        "parameters": {
            "ctlr": {
                "project_team": 1
            }
        }
    }

Stage 1. Put the files for processing in the folder.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You will be working with ``N_raw.txt`` files, which are collected by
running ``lab_5_scraper/scraper.py``. Your team number and texts are determined by
Anna Yuryevna. Put them in the folder ``final_project/assets/articles``.
This is the corpus you will be working with.

Stage 2. Processing data.
~~~~~~~~~~~~~~~~~~~~~~~~~

The task is to process a corpus of texts, get ``.conllu`` file and correct the mistakes
that could appear in the created file.

Stage 2.1. Create ``.conllu`` file for the corpus
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The needed logic for data processing should be written in ``final_project/main.py`` file.
Firstly, all the `.txt` files from ``final_project/assets`` are to be joint into one `.txt`
file and then processed using :py:class:`lab_6_pipeline.pipeline.UDPipeAnalyzer`
into a single ``auto_annotated.conllu`` file.

.. important::

    Running ``main.py`` file should result in creation of
    ``auto_annotated.conllu`` in folder ``final_project/dist``.
    If the ``dist`` folder does not exist, it must be created automatically.

.. note::

    Remember to use ``pathlib`` module in order
    to operate paths.

.. note::

    It is mandatory to use the
    :py:class:`lab_6_pipeline.pipeline.UDPipeAnalyzer`.

.. attention::

    Before processing, make sure to validate the input:

    - The folder with corpus must exist. If it does not, raise ``FileNotFoundError``.
    - At least one ``.txt`` file must be found in the folder. If none are found,
      raise ``ValueError``.
    - The result returned by ``UDPipeAnalyzer.analyze()`` must not be empty.

.. note::

    The resulting ``.conllu`` file must end with a newline.

Stage 2.2. Correct morphological annotation manually
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The resulting file is to be opened in text editor and then copied to an
`.xlsx` file. To work with the file, you will need the following columns in the table:
token number - token - lemma - part of speech - morphological characteristics.
Please, delete all the remaining columns provided by UDPipe and add three new columns:
``comments to POS tags``, ``comments to characteristics`` and ``comments to tokens``.

Using the .conllu file you are supposed to make up the word frequency dictionary.
Once it is ready, you are welcome to work with the least popular word forms to find
the mistakes in tokenization made by UDPipe. If any of the word forms turn out to
be words joint with punctuation marks or words divided into tokens, you are supposed
to correct the mistakes in the .conllu file and write comments in the
``comments to tokens`` column in the `.xlsx` file.

.. attention::

    Your `.xlsx` file or frequency list may be uploaded to the folder
    ``final_project/dist/table_work`` if you wish, but this folder will not appear
    in your fork after pushing the commit.

Next comes checking the table for mistakes in morphological annotation made by UDPipe.
Whenever you come across any mistakes in either POS tags or characteristics, you are
welcome to fill in the corresponding column with the comment in the `.xlsx` file and
make corrections in the `.conllu` file. When making judgements as to the mistakes in
morphological annotation, you are welcome to use the following sources:

1. UD POS tags: https://universaldependencies.org/u/pos/all.html
2. UD POS features: https://universaldependencies.org/u/feat/index.html
3. UD Russian POS tags and features: https://universaldependencies.org/treebanks/ru_gsd/index.html
4. Dictionaries of the Russian language containing morphological information

Please do not forget to refer to the sources you use in the comments.
You are supposed to stop working with the `.conllu` and `.xlsx` files
and send them to Anna Yuryevna together with the frequency dictionary in the .xlsx format by **TBD**.

Anna Yuryevna will check your annotations and suggest improvements, if any.


Stage 2.3. Upload corrected ``.conllu`` file.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After you correct all mistakes in automatically annotated `.conllu`, you should
upload the final corrected `.conllu` file to the folder ``final_project/dist``
under the name ``final.conllu``.

Stage 3. Pass the checks.
~~~~~~~~~~~~~~~~~~~~~~~~~

To get extra point for the exam, your markup should pass all the checks.

Correctness of the `.conllu` file will be checked with a script taken from the repository
with code from the Technical Track: ``admin_utils/final_project/checker.py``

You can also use it to check the `.conllu` file locally.

Note that this script can be run from PyCharm terminal or PowerShell
from a root of the project, like this:

.. code-block:: bash

    python admin_utils/final_project/checker.py final_project/dist/auto_annotated.conllu

Your forks should contain this script already, so pull and use, otherwise,
write to the chat and ask assistants.

Stage 4. Preparing exam presentation.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Meanwhile, your task will be to prepare an exam presentation,
which should include a report on the mistakes in tokenization and morphological
annotation you came across - both a quantitative and qualitative
(typology of mistakes, possible reasons for them, etc.) analysis.

Time limit of the presentation - **7 minutes**.

The presentation is to be delivered at the exam.
**Assessment criteria**:

- the proportion of identified mistakes;
- the quality of their analysis in the comments section of the table and the presentation;
- the precision of corrections in the .conllu file;
- adherence to the time limit;
- the quality of the oral presentation (memorization of the text, fluency,
  and intelligibility of speech);
- the quality of the computer presentation;
- the quality of answers to follow-up questions.

.. attention::

    The mark for the exam you will receive as a result has a coefficient of 0.9.
    The remaining 10% of your exam mark is based on your work with NeuroKryaBot.
