Affordability in New Zealand
********************************
Web maps of affordability for various regions of New Zealand (NZ), focusing on rent and commute costs relative to income.


Requirements
============
- Python >= 3.4 along with the Python modules in ``requirements.txt``; for data processing
- `RapydML <https://bitbucket.org/pyjeon/rapydml>`_ for compiling RapydML (.pyml) files to HTML
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
- The data wrangling takes place in the IPython notebooks in ``py``


Authors
========
- Alex Raichev (2013-12-16)