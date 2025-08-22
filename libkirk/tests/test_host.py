"""
Unittests for host SUT implementations.
"""

import pytest

from libkirk.host import HostSUT
from libkirk.tests.test_session import _TestSession
from libkirk.tests.test_sut import _TestSUT

pytestmark = pytest.mark.asyncio


@pytest.fixture
async def sut():
    _sut = HostSUT()
    _sut.setup()

    yield _sut

    if await _sut.is_running:
        await _sut.stop()


class TestHostSUT(_TestSUT):
    """
    Test HostSUT implementation.
    """

    @pytest.fixture
    def sut_stop_sleep(self, request):
        """
        Host SUT test doesn't require time sleep in `test_stop_communicate`.
        """
        return request.param * 0

    async def test_fetch_file_stop(self):
        pytest.skip(reason="Coroutines don't support I/O file handling")


class TestHostSession(_TestSession):
    """
    Test Session implementation.
    """
