.. vim: set fileencoding=utf-8 :
.. Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
.. Thu Apr 16 16:39:01 CEST 2015



.. image:: http://img.shields.io/badge/docs-stable-yellow.png
   :target: http://pythonhosted.org/bob.db.pericrosseye/index.html
.. image:: http://img.shields.io/badge/docs-latest-orange.png
   :target: https://www.idiap.ch/software/bob/docs/latest/bob/bob.db.pericrosseye/master/index.html
.. image:: https://gitlab.idiap.ch/bob/bob.db.cuhk_cufs/badges/master/build.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.pericrosseye/commits/master
.. image:: https://img.shields.io/badge/gitlab-project-0000c0.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.pericrosseye
.. image:: http://img.shields.io/pypi/v/bob.db.pericrosseye.png
   :target: https://pypi.python.org/pypi/bob.db.pericrosseye
.. image:: http://img.shields.io/pypi/dm/bob.db.pericrosseye.png
   :target: https://pypi.python.org/pypi/bob.db.pericrosseye
.. image:: https://img.shields.io/badge/original-data--files-a000a0.png
   :target: https://sites.google.com/site/crossspectrumcompetition/guidelines


=======================================================
Cross-Spectrum Iris/Periocular Recognition Database
=======================================================

This package contains the access API and descriptions for the `Cross-Spectrum Iris/Periocular Recognition COMPETITION <https://sites.google.com/site/crossspectrumcompetition/guidelines>`.
The actual raw data for the database should be downloaded from the original URL. 
This package only contains the Bob accessor methods to use the DB directly from python, with the original protocol of the database.

This database is for research on VIS-NIR periocular recognition.
It includes samples of 20 identities captured in both VIS and NIR.


Installation
------------

Follow our `installation`_ instructions. Then, using the Python interpreter
provided by the distribution, bootstrap and buildout this package::

  $ python bootstrap-buildout.py
  $ ./bin/buildout


Contact
-------

For questions or reporting issues to this software package, contact our
development `mailing list`_.


.. Place your references here:
.. _bob: https://www.idiap.ch/software/bob
.. _installation: https://gitlab.idiap.ch/bob/bob/wikis/Installation
.. _mailing list: https://groups.google.com/forum/?fromgroups#!forum/bob-devel