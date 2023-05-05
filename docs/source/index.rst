.. ValueSets API documentation master file, created by
   sphinx-quickstart on Tue May  2 12:34:13 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ValueSets API Documentation
=========================================

An Ensembl **ValueSet** is a collection of key/value pairs that are related to a given topic. In the context of Ensembl data, these represent definitions of certain terms that may be used in several different places. The **ValueSets API** allows to query the source of these terms in order to get their definitons.

A **ValueSet** item should have the following fields:

- *accession_id* (str): value set unique identifier - e.g. "mane.select"

- *label* (str): short human-friendly name - e.g. "MANE Select"

- *value* (str): short machine-friendly name - e.g. "select"

- *definition* (str): short description - e.g. "A Transcript which is matched between Ensembl/GENCODE and RefSeq as part of the MANE project"

- *description* (str): long verbose definition - e.g. "A Matched Annotation from NCBI and EMBL-EBI is a collaboration between Ensembl/GENCODE and RefSeq. The MANE Select is a default transcript per human gene that is representative of biology, well-supported, expressed and highly-conserved. This transcript set matches GRCh38 and is 100% identical between RefSeq and Ensembl/GENCODE for 5' UTR, CDS, splicing and 3'UTR."

.. toctree::
   :maxdepth: 2
   :caption: Contents:



.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`


Contents
--------

.. toctree::

   usage
   api
   license
