"""
.. module:: installer
    :platform: Linux
    :synopsis: module containing the generic framework installer definition

.. moduleauthor:: Andrea Cervesato <andrea.cervesato@suse.com>
"""
from libkirk import KirkException
from libkirk.io import IOBuffer
from libkirk.plugin import Plugin


class InstallerError(KirkException):
    """
    Raised when an error has been occured during installation.
    """


class Installer(Plugin):
    """
    Abstract class defining commands and packages in order to install
    a testing framework.
    """

    @property
    def is_running(self) -> list:
        """
        True if installation is running.
        """
        raise NotImplementedError()

    async def install(self, buffer: IOBuffer = None) -> None:
        """
        Install the testing framework inside SUT.
        :param buffer: buffer where to write stdout
        :type buffer: IOBuffer
        """
        raise NotImplementedError()

    async def stop(self) -> None:
        """
        Stop the installation.
        """
        raise NotImplementedError()
