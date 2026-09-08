.. SPDX-License-Identifier: GPL-2.0-or-later

Changelog
=========

v4.2.0 (2026-09-08)
-------------------

* Add ``--dry-run`` option to preview test execution
* Add configurable fault injection interval option (``--fault-injection-interval``)
* Persist and export partial test suite results when aborted mid-suite
* Fix ``--exec-timeout`` not killing tests in the shell channel
* Fix JSON report file being opened in read/write instead of write-only mode
* Fix incorrect log message when test parameters are missing in LTP metadata
* Fix exception handling in the event subsystem
* Fix ``--randomize`` command-line description
* Move ``IOBuffer`` implementations inside the ``sut`` module
* Use ``IntEnum`` for kernel status in scheduler
* Major documentation restructuring and expansion (quickstart, SSH, LTX, QEMU, plugins)
* Improve test suite coverage and resolve flaky tests

v4.1.0 (2026-03-30)
-------------------

* Support LTP network tests configurations
* Remove unused ``PASSWD`` and ``RUSER`` variables in LTP framework
* Ensure test results dictionaries are not shared across instances
* Fix mismatch between event and event handler name in monitor
* Fix potential ``ValueError`` on ``task_done()`` in events subsystem
* Fix wrong return type annotation in SUT module

v4.0.0 (2026-02-23)
-------------------

* Major performance optimizations across scheduler, session, events, and UI
* Optimize internal scheduler algorithm to reduce test suite loading times
* Add ``/proc/cmdline`` printing in target information summary
* Add slot release lock and loop cleanup fixes in LTX communication
* Fix potential deadlock during SUT reboot in scheduler
* Fix race condition in SUT ``qsize()``
* Fix fire-and-forget buffer write issue in SSH channel
* Fix returncode handling for processes in shell channel
* Remove deprecated ``--env`` option

v3.2.1 (2026-01-28)
-------------------

* Fix ``LTPROOT`` retrieval in LTP framework
* Documentation updates for upgrading kirk inside LTP after release

v3.2 (2026-01-12)
-----------------

* Add ``--optimize-sut`` option
* Refactor ``Framework`` to be an internal session object rather than a plugin
* Improve test suite performance and reduce CI overhead

v3.1 (2025-12-10)
-----------------

* Implement forceful stop on session interruption
* Ignore UTF-8 decoding errors during SSH connection setup
* Stabilize SSH ``MaxSessions`` detection
* Document semantic versioning policy
* Fix docstrings across ``libkirk``

v3.0 (2025-10-23)
-----------------

* Introduce new communication channels architecture (Shell, SSH, LTX, Qemu)
* Redesign SUT API and communication channel API (``libkirk.com``)
* Add ``--com`` and ``--plugins`` command-line options
* Make plugins cloneable
* Set ``CONF`` status for timed-out tests in scheduler
* Add internal architecture and plugins sections to documentation
* Enable testing on Python 3.14

v2.3 (2025-09-22)
-----------------

* Catch ``ConnectionError`` during SSH communication
* Respect user-defined ``LTP_TIMEOUT_MUL`` environment variable
* Make Qemu ``hvc0`` console parameter explicit
* Complete strong typing annotations across all modules
* Add Ruff configuration and linting integration

v2.2.2 (2025-08-26)
-------------------

* Fix data fetch and empty match object checks in Qemu SUT
* Fix and re-enable LTX tests using ``KILL`` command
* Add maintainer release documentation

v2.2.1 (2025-08-25)
-------------------

* Comprehensive migration to Ruff for linting and formatting
* Add static type checking and complete type annotations
* Rename ``events`` module to ``evt``
* Stabilize SSH and LTX test suites under CI

v2.2 (2025-08-18)
-----------------

* Introduce ``errors`` module for structured exception handling
* Add fault injection support to SUT and CLI
* Add test parallelization support in session and UI
* Add script to convert results JSON to logs
* Respect ``LTPROOT`` from environment
* Output test ending messages to ``/dev/kmsg``

v2.1 (2025-05-27)
-----------------

* Add support for ``known_hosts`` configuration in SSH
* Improve exception handling in SSH channel
* Complete UI events properly on ``KeyboardInterrupt``
* Remove external frameworks support

v2.0 (2025-04-16)
-----------------

* Add ``--monitor`` option for event monitoring
* Add ``--runtime``, ``--randomize``, ``--suite-iterate``, and ``--run-pattern`` options
* Introduce ``io`` module with ``AsyncFile``
* Support ordered event firing in events subsystem
* Add JSON-to-HTML results conversion utility
* Improve session graceful stop handling on interrupts

v1.5 (2025-02-12)
-----------------

* Register missing event handler for suite timeout
* Aggregate test results statistics across all executed test suites
* Transition packaging configuration to ``pyproject.toml``
* Expand Python version support

v1.4 (2024-07-26)
-----------------

* Package metadata and setuptools build script improvements
* Display version information via standard CLI conventions

v1.3 (2024-06-07)
-----------------

* Fix SSH command execution output redirection and live streaming
* Prevent crash when stopping tests during SSH execution
* Document environment variable passing in README
* Fix test collection in Linux kselftests module

v1.2 (2023-11-29)
-----------------

* Replace ``epoll()`` usage with threaded I/O in LTX communication
* Add command search capabilities to test frameworks
* Fix runtest file argument parsing with quotes
* Improve Qemu login prompt recognition
* Add build system integration for LTP

v1.1 (2023-08-17)
------------------

* Initial public release as the LTP test executor
* Support SUT backends: Host, SSH, QEMU, and LTX
* Support LTP, Linux kselftest, and liburing test frameworks
* Support parallel test execution and test timeouts
* Support kernel panic and tainted kernel detection
* Export structured test execution results to JSON
