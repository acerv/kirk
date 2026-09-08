.. SPDX-License-Identifier: GPL-2.0-or-later

Start using kirk
================

The tool works out of the box by running ``kirk`` script.
Minimum python requirement is 3.6+ and *optional* dependencies are the following:

- :doc:`ssh` (requires `asyncssh <https://pypi.org/project/asyncssh/>`_)
- :doc:`ltx` (requires `msgpack <https://pypi.org/project/msgpack/>`_)

kirk will detect if dependencies are installed and activate the corresponding
support.

To use kirk via git repository:

.. code-block:: bash

    git clone https://github.com/linux-test-project/kirk.git
    cd kirk
    pip install .

    kirk --help

kirk is also present in `PyPI <https://pypi.org/project/kirk>`_ and it can be
installed via ``pip`` command:

.. code-block:: bash

   pip install --user kirk

Basic usage
-----------

Some basic commands are the following:

.. code-block:: bash

    # run LTP syscalls testing suite on host
    kirk --run-suite syscalls

    # run LTP syscalls testing suite in parallel on host using 16 workers
    kirk --run-suite syscalls --workers 16

    # pass environment variables (list of key=value separated by ':')
    kirk --run-suite net.features \
         --env 'VIRT_PERF_THRESHOLD=180:LTP_NET_FEATURES_IGNORE_PERFORMANCE_FAILURE=1'

It's possible to run a single command before running testing suites using
``--run-command`` option as following:

.. code-block:: bash

    kirk --run-command ./setup_sut.sh \
         --run-suite syscalls

For remote execution and virtual machines, see :doc:`qemu`, :doc:`ssh`, and
:doc:`ltx`.

