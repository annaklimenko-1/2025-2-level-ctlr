.. _ctlr-article-label:

Article package
===============

.. toctree::
    :maxdepth: 1
    :titlesonly:
    :caption: Full API

    ../../core_utils/article/article.api.rst

The ``article`` package is responsible for handling the articles you
have collected from your website.

.. hint:: In case you think you have found a mistake in this package,
          contact your assistant. Those who considerably improve this module
          will get additional bonuses.

``article`` module
------------------

``article`` module represents the methods to work with the
:py:class:`core_utils.article.article.Article` abstraction.

:py:class:`core_utils.article.article.Article` class is responsible
for storing article raw, meta and ``.conllu`` data and working with it.
During the implementation of Lab 5 and Lab 6, you should use the methods of this class.
The lab descriptions will contain hints on when to use one or another class method,
but we advise you to study all the methods: they may be useful to you.

.. note:: Do not forget to create a new instance of the
          :py:class:`core_utils.article.article.Article` class to use its methods.

In addition to the ``Article`` class, the module has:

1. :py:func:`core_utils.article.article.date_from_meta` function which converts
   text date to ``datetime`` object.
2. :py:func:`core_utils.article.article.get_article_id_from_filepath` function which
   extracts the article id from its path.
3. :py:class:`core_utils.article.article.ArtifactType` abstraction which provides
   types of artifacts that can be created by text processing pipelines, such as ``CLEANED``
   and ``UDPIPE_CONLLU``.

The description of each artifact you can find in :ref:`dataset-label`.

.. note:: You should utilize attributes of :py:class:`core_utils.article.article.ArtifactType`
          in order to save processed versions of files. Otherwise, if you pass a string
          itself to some saving function, your code will be much more fragile.

``io`` module
-------------

``io`` module provide functions to work with input/output operations for
the :py:class:`core_utils.article.article.Article` abstraction.

It consists of the following functions, which are grouped by usage in the labs:

Lab_5
~~~~~

-  :py:func:`core_utils.article.io.to_raw` - use to save raw texts of each article;
-  :py:func:`core_utils.article.io.to_meta` - use to save meta-information about each article.

Lab_6
~~~~~

-  :py:func:`core_utils.article.io.from_raw` - use to load raw texts and
   create the :py:class:`core_utils.article.article.Article` abstraction;
-  :py:func:`core_utils.article.io.to_cleaned` - use to save cleaned texts
   of each article, i.e. lowercased texts with no punctuation;
-  :py:func:`core_utils.article.io.to_meta` - use to save POS information
   and required syntactic patterns from each article;
-  :py:func:`core_utils.article.io.from_meta` - use to load
   meta-information about each article and create the
   :py:class:`core_utils.article.article.Article` abstraction;
