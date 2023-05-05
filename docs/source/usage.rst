Usage
=====

Requirements
------------

Software:

- Python 3.10+
- gRPC

Python Modules:

- grpcio >= 1.54.0

- grpcio-tools >= 1.54.0

- openpyxl >= 3.1.2

- pandas >= 2.0.1

- protobuf >= 4.22.3

- typer >= 0.7

- requests >= 2.28.2

- pylint

- pytest

Getting Started
---------------

Clone this repo:

.. code-block:: console

   git clone --depth 1 -b main https://github.com/Ensembl/ensembl-valuesets.git

Install the python requirements:

.. code-block:: console

   pip install ./ensembl-valuesets

Run the server, listening on default port 50051:

.. code-block:: console

   python ensembl-valuesets/src/python/ensembl/valuesets/valuesets_rpc_server.py

Test the server with the provided basic client:

.. code-block:: console

   python ensembl-valuesets/src/python/ensembl/utils/valuesets_rpc_tinyclient.py

Testing
-------

Run test suite:

.. code-block:: console

   cd ensembl-valuesets
   pytest