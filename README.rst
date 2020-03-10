Affordability in New Zealand
********************************
Web maps of affordability for various regions of New Zealand (NZ), focusing on rent and commute costs relative to income.


Requirements
============
- Python >= 3.6 along with the Python modules in ``requirements.txt``; for data processing
- `RapydCSS <https://bitbucket.org/pyjeon/rapydcss>`_ for compiling RapydCSS (.sass) files to CSS
- `RapydScript <https://bitbucket.org/pyjeon/rapydscript>`_ for compiling RapydScript (.pyj) files to JavaScript


Instructions
=============
- To view the website locally, run ``python -m http.server 8000`` in your cloned version of this repository and point your browser to ``localhost:8000``.
- For auto-compiling RapydScript files, `this Gist <https://gist.github.com/araichev/8923682>`_ is useful.


Notes
======
- Development status is Alpha
- This project uses semantic versioning
- More notes on data and methodology in the About page at ``about.html``
- This project is funded in part by `MRCagney <http://mrcagney.com>`_
- The data wrangling is done with Python in the IPython notebooks in ``py``
- The user interface is done with RapydCSS and RapydScript with the help of a few JavaScript libraries, such as jQuery and jQuery-UI; no JavaScript frameworks involved.
- Works on mobile-phone-size screens, but best on laptop-size screens


Authors
========
- Alex Raichev (2013-12-16)


Changes
========

1.0.0, 2020-03-10
-----------------
- Removed RapydML dependency. Will eventually replace it with Jinja2 templates.
- Removed Paver dependency.
- Updated rental bond data and median incomes.


0.5.0, 2019-07-16
-----------------
- Made more robust the downloading of new rental data in the notebook ``py/prepare_rents.ipynb``.


0.4.3, 2018-12-18
-----------------
- Switched from Pipenv to Poetry.
- Fixed dead links.


0.3.0, 2017-10-12
-----------------
- Updated rent data.
- Simplified code and notebooks.
- Used Git LFS on the NZ titles geodata file.


0.2.1, 2017-07-14
------------------
- Updated rent data.


0.2.0, 2017-07-13
------------------
- Updated Auckland transit costs to use card fares instead of cash fares.
- Tweaked style.


0.1.0, 2017-05-26
------------------
- First release with MBIE rental areas instead of census area units.