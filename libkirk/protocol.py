"""
.. module:: protocol
    :platform: Linux
    :synopsis: everything related to protocols definitions

.. moduleauthor:: Andrea Cervesato <andrea.cervesato@suse.com>
"""


class IOBuffer:
    """
    IO stdout buffer. The API is similar to ``IO`` types.
    """

    async def write(self, data: str) -> None:
        """
        Write data.
        """
        raise NotImplementedError()


class ProtocolHandler:
    """
    This is an abstraction class for protocols supported by kirk.
    The class can be used to describe complex scenarios and SUT(s).
    """

    @property
    async def is_running(self) -> bool:
        """
        Return True if SUT is running.
        """
        raise NotImplementedError()

    async def ping(self) -> float:
        """
        If SUT is replying and it's available, ping will return time needed to
        wait for SUT reply.
        :returns: float
        """
        raise NotImplementedError()

    async def communicate(self, iobuffer: IOBuffer = None) -> None:
        """
        Start communicating with the SUT.
        :param iobuffer: buffer used to write SUT stdout
        :type iobuffer: IOBuffer
        """
        raise NotImplementedError()

    async def stop(self, iobuffer: IOBuffer = None) -> None:
        """
        Stop the current SUT session.
        :param iobuffer: buffer used to write SUT stdout
        :type iobuffer: IOBuffer
        """
        raise NotImplementedError()

    async def run_command(
            self,
            command: str,
            cwd: str = None,
            env: dict = None,
            iobuffer: IOBuffer = None) -> dict:
        """
        Coroutine to run command on target.
        :param command: command to execute
        :type command: str
        :param cwd: current working directory
        :type cwd: str
        :param env: environment variables
        :type env: dict
        :param iobuffer: buffer used to write SUT stdout
        :type iobuffer: IOBuffer
        :returns: dictionary containing command execution information

            {
                "command": <str>,
                "returncode": <int>,
                "stdout": <str>,
                "exec_time": <float>,
            }

            If None is returned, then callback failed.
        """
        raise NotImplementedError()

    async def fetch_file(self, target_path: str) -> bytes:
        """
        Fetch file from target path and return data from target path.
        :param target_path: path of the file to download from target
        :type target_path: str
        :returns: bytes contained in target_path
        """
        raise NotImplementedError()
