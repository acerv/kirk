"""
.. module:: ltp
    :platform: Linux
    :synopsis: LTP framework definition

.. moduleauthor:: Andrea Cervesato <andrea.cervesato@suse.com>
"""
import os
import re
import json
import logging
from libkirk import KirkException
from libkirk.results import TestResults
from libkirk.sut import SUT
from libkirk.data import Suite
from libkirk.data import Test
from libkirk.framework import Framework


class LTPFramework(Framework):
    """
    Linux Test Project framework definition.
    """

    PARALLEL_BLACKLIST = [
        "needs_root",
        "needs_device",
        "mount_device",
        "mntpoint",
        "resource_file",
        "format_device",
        "save_restore",
        "max_runtime"
    ]

    def __init__(self) -> None:
        self._logger = logging.getLogger("libkirk.ltp")
        self._root = "/opt/ltp"
        self._env = {
            "LTPROOT": self._root,
            "TMPDIR": "/tmp",
            "LTP_COLORIZE_OUTPUT": "1",
        }

    @property
    def config_help(self) -> dict:
        return {
            "root": "LTP install folder",
        }

    def setup(self, **kwargs: dict) -> None:
        env = kwargs.get("env", None)
        if env:
            self._env.update(env)

        root = kwargs.get("root", None)
        if root:
            self._root = root
            self._env["LTPROOT"] = self._root

    # pylint: disable=too-many-locals
    def _read_runtest(
            self,
            suite_name: str,
            content: str,
            metadata: dict = None) -> Suite:
        """
        It reads a runtest file content and it returns a Suite object.
        :param suite_name: name of the test suite
        :type suite_name: str
        :param content: content of the runtest file
        :type content: str
        :param metadata: metadata JSON file content
        :type metadata: dict
        :returns: Suite
        """
        self._logger.info("collecting testing suite: %s", suite_name)

        metadata_tests = None
        if metadata:
            self._logger.info("Reading metadata content")
            metadata_tests = metadata.get("tests", None)

        tests = []
        lines = content.split('\n')
        tc_path = os.path.join(self._root, "testcases", "bin")

        for line in lines:
            if not line.strip() or line.strip().startswith("#"):
                continue

            self._logger.debug("Test declaration: %s", line)

            parts = line.split()
            if len(parts) < 2:
                raise KirkException(
                    "runtest file is not defining test command")

            test_name = parts[0]
            test_cmd = parts[1]
            test_args = []

            if len(parts) >= 3:
                test_args = parts[2:]

            parallelizable = True

            if not metadata_tests:
                # no metadata no party
                parallelizable = False
            else:
                test_params = metadata_tests.get(test_name, None)
                if test_params:
                    self._logger.info(
                        "Found %s test params in metadata", test_name)
                    self._logger.debug("params=%s", test_params)

                if test_params is None:
                    # this probably means test is not using new LTP API,
                    # so we can't decide if test can run in parallel or not
                    parallelizable = False
                else:
                    for blacklist_param in self.PARALLEL_BLACKLIST:
                        if blacklist_param in test_params:
                            parallelizable = False
                            break

            if not parallelizable:
                self._logger.info("Test '%s' is not parallelizable", test_name)
            else:
                self._logger.info("Test '%s' is parallelizable", test_name)

            test = Test(
                name=test_name,
                cmd=test_cmd,
                args=test_args,
                cwd=tc_path,
                env=self._env,
                parallelizable=parallelizable)

            tests.append(test)

            self._logger.debug("test: %s", test)

        self._logger.debug("Collected tests: %d", len(tests))

        suite = Suite(suite_name, tests)

        self._logger.debug(suite)
        self._logger.info("Collected testing suite: %s", suite_name)

        return suite

    @property
    def name(self) -> str:
        return "ltp"

    async def get_suites(self, sut: SUT) -> list:
        if not sut:
            raise ValueError("SUT is None")

        ret = await sut.run_command(f"test -d {self._root}")
        if ret["returncode"] != 0:
            raise KirkException(f"LTP folder doesn't exist: {self._root}")

        runtest_dir = os.path.join(self._root, "runtest")
        ret = await sut.run_command(f"test -d {runtest_dir}")
        if ret["returncode"] != 0:
            raise KirkException(f"'{runtest_dir}' doesn't exist inside SUT")

        ret = await sut.run_command(f"ls --format=single-column {runtest_dir}")
        stdout = ret["stdout"]
        if ret["returncode"] != 0:
            raise KirkException(f"command failed with: {stdout}")

        suites = [line for line in stdout.split('\n') if line]
        return suites

    async def find_suite(self, sut: SUT, name: str) -> Suite:
        if not sut:
            raise ValueError("SUT is None")

        if not name:
            raise ValueError("name is empty")

        ret = await sut.run_command(f"test -d {self._root}")
        if ret["returncode"] != 0:
            raise KirkException(f"LTP folder doesn't exist: {self._root}")

        suite_path = os.path.join(self._root, "runtest", name)

        ret = await sut.run_command(f"test -f {suite_path}")
        if ret["returncode"] != 0:
            raise KirkException(f"'{name}' suite doesn't exist")

        metadata_path = os.path.join(
            self._root,
            "metadata",
            "ltp.json"
        )

        metadata = None
        ret = await sut.run_command(f"cat {metadata_path}")
        if ret["returncode"] != 0:
            raise KirkException(f"Can't read metadata file: {metadata_path}")

        data = await sut.fetch_file(suite_path)
        content = data.decode(encoding="utf-8", errors="ignore")

        metadata = json.loads(ret['stdout'])
        suite = self._read_runtest(name, content, metadata)

        return suite

    async def read_result(
            self,
            test: Test,
            stdout: str,
            retcode: int,
            exec_t: float) -> TestResults:
        # get rid of colors from stdout
        stdout = re.sub(r'\u001b\[[0-9;]+[a-zA-Z]', '', stdout)

        match = re.search(
            r"Summary:\n"
            r"passed\s*(?P<passed>\d+)\n"
            r"failed\s*(?P<failed>\d+)\n"
            r"broken\s*(?P<broken>\d+)\n"
            r"skipped\s*(?P<skipped>\d+)\n"
            r"warnings\s*(?P<warnings>\d+)\n",
            stdout
        )

        passed = 0
        failed = 0
        skipped = 0
        broken = 0
        skipped = 0
        warnings = 0
        error = retcode == -1

        if match:
            passed = int(match.group("passed"))
            failed = int(match.group("failed"))
            skipped = int(match.group("skipped"))
            broken = int(match.group("broken"))
            skipped = int(match.group("skipped"))
            warnings = int(match.group("warnings"))
        else:
            passed = stdout.count("TPASS")
            failed = stdout.count("TFAIL")
            skipped = stdout.count("TSKIP")
            broken = stdout.count("TBROK")
            warnings = stdout.count("TWARN")

            if passed == 0 and \
                    failed == 0 and \
                    skipped == 0 and \
                    broken == 0 and \
                    warnings == 0:
                # if no results are given, this is probably an
                # old test implementation that fails when return
                # code is != 0
                if retcode == 0:
                    passed = 1
                elif retcode == 4:
                    warnings = 1
                elif retcode == 32:
                    skipped = 1
                elif not error:
                    failed = 1

        if error:
            broken = 1

        result = TestResults(
            test=test,
            failed=failed,
            passed=passed,
            broken=broken,
            skipped=skipped,
            warnings=warnings,
            exec_time=exec_t,
            retcode=retcode,
            stdout=stdout,
        )

        return result
