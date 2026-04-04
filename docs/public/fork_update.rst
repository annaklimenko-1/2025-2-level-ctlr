Fork update
===========

During the course changes will be added to the main repository (changes
in tests, bug fixes, etc.) - these changes will not automatically appear
in your forks.

To add changes to your fork from the main repository, follow these steps:

1. Open the repository site sent to you by your lecturer.

2. Click ``Code``, select ``HTTPS`` and click the copy button.

   .. figure:: ../images/fork_update/copy_original_repo_url.png
      :alt: copy repo url

3. Open terminal in PyCharm development environment.

   .. figure:: ../images/starting_guide/pycharm_open_terminal.png
      :alt: open terminal

4. Run ``git remote add upstream <link-to-main-repository>``.

   .. image:: ../images/fork_update/add_upstream.png

5. Run ``git fetch upstream``.

   .. image:: ../images/fork_update/fetch_upstream.png

.. important:: Please note that the link in the screenshot
               above points to the parent repository.

6. Run ``git merge upstream/main --no-edit``.

   .. image:: ../images/fork_update/merge_upstream.png

.. note:: Depending on the number of changes, the output of the
          command will be different.

This command will result in the latest changes from
the main repository appearing in your local fork.

More information about the commands described above can be found
in the `official Git documentation <https://git-scm.com/docs>`__.

Fork update using a comment in a Pull Request
---------------------------------------------

Fork can be in several states in relation to the ``upstream`` repository:

1. Fork and ``upstream`` are aligned by states.
2. There are new changes in ``upstream`` that are not yet in the fork:

    1. For example, when adding fixes to existing files.

3. There were new changes in ``upstream`` that were not yet in the fork +
   there were changes in the fork that conflict with changes from ``upstream``:

    1. For example, when one of the laboratory works was added
       to the ``upstream`` as an exemplary.

For **cases 2 and 3**, automatic update mechanisms are provided via a comment in the Pull Request.

For **case 2**:

1. The update occurs using a comment containing the substring ``/update:get_new``

    1. The fork will contain changes from the ``upstream`` repository.

**Case 3** is divided into two scenarios based on the need to save
the student’s laboratory work in the fork:

1. If it is necessary to keep the version of the laboratory work from the fork,
   then the update occurs using a comment containing the substring ``/update:keep_fork``:

    1. The fork will contain changes from ``upstream`` that do not affect the ``main.py``
       and ``start.py`` files for laboratory work:

        1. The ``main.py`` and ``start.py`` files will be saved as they are in the fork.
        2. All other conflicts will be resolved in favor of ``upstream`` changes.

2. If it is necessary to upload a version of laboratory work from ``upstream`` to the fork,
   then the update occurs using a comment containing the substring ``/update:keep_upstream``

    1. The fork will be aligned with the ``upstream``.
    2. All conflicts will be resolved in favor of ``upstream`` changes.
