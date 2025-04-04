"""
.. module:: ltp_install
    :platform: Linux
    :synopsis: module containing LTP framework installer

.. moduleauthor:: Andrea Cervesato <andrea.cervesato@suse.com>
"""
import asyncio
import logging
from libkirk.io import IOBuffer
from libkirk.sut import SUT
from libkirk.installer import Installer
from libkirk.installer import InstallerError


class LinuxDistro:
    """
    Distribution install information.
    """

    @property
    def refresh_cmd(self) -> str:
        """
        Cache refresh command.
        """
        raise NotImplementedError()

    @property
    def install_cmd(self) -> str:
        """
        Packages install command.
        """
        raise NotImplementedError()

    async def setup(self, m32_support: bool) -> list:
        """
        Setup distro and return packages used to install LTP from sources.
        :param m32_support: if True, support 32bit system
        :type m32_support: bool
        :returns: list of packages
        """
        raise NotImplementedError()


class SUSELinux(LinuxDistro):
    """
    openSUSE and SLES distributions.
    """

    @property
    def refresh_cmd(self) -> str:
        return "zypper --non-interactive refresh"

    @property
    def install_cmd(self) -> str:
        return "zypper --non-interactive --ignore-unknown install"

    async def setup(self, m32_support: bool) -> list:
        pkgs = [
            # build packages
            "autoconf",
            "automake",
            "gcc",
            "git",
            "kernel-devel",
            "make",
            "pkg-config",
            "unzip",

            # runtime packages
            "bc",
            "btrfsprogs",
            "dosfstools",
            "e2fsprogs",
            "nfs-kernel-server",
            "quota",
            "xfsprogs",

            # tools packages
            "libssh4"
        ]

        if m32_support:
            pkgs.extend([
                "libacl-devel-32bit",
                "libaio-devel-32bit",
                "libattr-devel-32bit",
            ])
        else:
            pkgs.extend([
                "libacl-devel",
                "libaio-devel",
                "libattr-devel",
                "libcap-devel",
                "libnuma-devel",
            ])

        return pkgs


class DebianLinux(LinuxDistro):
    """
    Debian distribution.
    """

    def __init__(self, sut: SUT) -> None:
        self._sut = sut

    async def _get_runtime_pkgs(self) -> list:
        """
        Inherit to change runtime packages.
        """
        runtime_pkgs = [
            "bc",
            "btrfs-progs",
            "dosfstools",
            "e2fsprogs",
            "nfs-kernel-server",
            "quota",
            "xfsprogs",
        ]

        ret = await self._sut.run_command('dpkg --print-architecture')
        if ret['returncode'] != 0:
            raise InstallerError(
                f"Can't read debian architecture: {ret['stdout']}")

        arch = ret['stdout'].rstrip()
        runtime_pkgs.append(f"linux-headers-{arch}")

        return runtime_pkgs

    async def setup(self, m32_support: bool) -> list:
        if m32_support:
            ret = await self._sut.run_command('dpkg --add-architecture i386')
            if ret['returncode'] != 0:
                raise InstallerError(
                    f"'{ret['command']}' command is failing: {ret['stdout']}")

        build_pkgs = [
            "automake",
            "autoconf",
            "git",
            "make",
            "pkg-config",
            "unzip",
        ]

        if m32_support:
            build_pkgs.append("gcc-multilib")
        else:
            build_pkgs.append("gcc")

        runtime_pkgs = await self._get_runtime_pkgs()

        libs_pkgs = [
            "libacl1-dev",
            "libaio-dev",
            "libattr1-dev",
            "libcap-dev",
            "libnuma-dev",
        ]

        if m32_support:
            libs_pkgs = [pkg + ":i386" for pkg in libs_pkgs]

        tools_pkgs = [
            "libssh-4"
        ]

        pkgs = []
        pkgs.extend(build_pkgs)
        pkgs.extend(runtime_pkgs)
        pkgs.extend(libs_pkgs)
        pkgs.extend(tools_pkgs)

        return pkgs

    @property
    def refresh_cmd(self) -> str:
        return "apt-get -y update"

    @property
    def install_cmd(self) -> str:
        cmd = "DEBIAN_FRONTEND=noninteractive "
        cmd += "apt-get -y --no-install-recommends install"
        return cmd


class UbuntuLinux(DebianLinux):
    """
    Installer for Ubuntu.
    """

    async def _get_runtime_pkgs(self) -> list:
        runtime_pkgs = [
            "bc",
            "btrfs-progs",
            "dosfstools",
            "e2fsprogs",
            "linux-headers-generic",
            "nfs-kernel-server",
            "quota",
            "xfsprogs",
        ]

        return runtime_pkgs


class AlpineLinux(LinuxDistro):
    """
    Alpine linux distribution.
    """

    @property
    def refresh_cmd(self) -> str:
        return "apk update"

    @property
    def install_cmd(self) -> str:
        return "apk add"

    async def setup(self, m32_support: bool) -> list:
        pkgs = [
            # build packages
            "autoconf",
            "automake",
            "build-base",
            "git",
            "linux-headers",
            "make",
            "pkgconf",
            "unzip",

            # runtime packages
            "bc",
            "btrfs-progs",
            "dosfstools",
            "e2fsprogs",
            "nfs-utils",
            "quota-tools",
            "xfsprogs",

            # libs packages
            "acl-dev",
            "attr-dev",
            "libaio-dev",
            "libcap-dev",
            "numactl-dev",

            # tools packages
            "libssh"
        ]

        return pkgs


class FedoraLinux(LinuxDistro):
    """
    Fedora Linux distribution.
    """

    @property
    def refresh_cmd(self) -> str:
        return "yum update -y"

    @property
    def install_cmd(self) -> str:
        return "yum install -y"

    async def setup(self, m32_support: bool) -> list:
        pkgs = [
            # build packages
            "autoconf",
            "automake",
            "gcc",
            "git",
            "kernel-devel",
            "make",
            "pkg-config",
            "unzip",

            # runtime packages
            "bc",
            "btrfs-progs",
            "dosfstools",
            "e2fsprogs",
            "nfs-utils",
            "quota",
            "xfsprogs",

            # tools packages
            "libssh"
        ]

        libs_pkgs = [
            "libacl-devel",
            "libaio-devel",
            "libattr-devel",
            "libcap-devel",
            "numactl-libs"
        ]

        if m32_support:
            libs_pkgs = [pkg + ".i686" for pkg in libs_pkgs]

        pkgs.extend(libs_pkgs)
        return pkgs


# pylint: disable=too-many-instance-attributes
class LTPInstaller(Installer):
    """
    Linux Test Project framework installer.
    """

    def __init__(self) -> None:
        self._logger = logging.getLogger("libkirk.ltp.install")
        self._install_lock = asyncio.Lock()
        self._sut = None
        self._buffer = None
        self._stop = False
        self._repo_dir = None
        self._m32_support = None
        self._branch = None
        self._commit = None
        self._install_dir = None
        self._url = None

    def setup(self, **kwargs: dict) -> None:
        self._sut = kwargs.get("sut", None)
        if not self._sut:
            raise ValueError("sut is not provided")

        tmpdir = kwargs.get("tmpdir", None)
        if not tmpdir:
            raise ValueError("tmpdir is empty")

        self._repo_dir = kwargs.get("repo_dir", f"{tmpdir}/ltp")
        self._m32_support = kwargs.get("m32_support", False)
        self._branch = kwargs.get("branch", "master")
        self._commit = kwargs.get("commit", None)
        self._install_dir = kwargs.get("install_dir", "/opt/ltp")
        self._url = kwargs.get(
            "url",
            "https://github.com/linux-test-project/ltp.git")

    @property
    def config_help(self) -> dict:
        return {
            "url": "git repo URL",
            "install_dir": "LTP install folder",
            "m32_support": "Support for 32bit",
            "branch": "git branch",
            "commit": "git commit",
        }

    @property
    def name(self) -> str:
        return "ltp"

    @property
    def is_running(self) -> list:
        self._install_lock.locked()

    async def _run_cmd(self, cmd: str, cwd: str = None) -> None:
        """
        Run a command via SUT and eventually raise an exception if it fails.
        """
        if self._stop or not await self._sut.is_running:
            return

        ret = await self._sut.run_command(cmd, cwd=cwd, iobuffer=self._buffer)
        if ret["returncode"] != 0:
            raise InstallerError(
                f"{ret['command']} failed with "
                f"{ret['returncode']}: {ret['stdout']}")

        return ret

    async def _get_distro_id(self) -> str:
        """
        Return the distro ID of SUT.
        """
        info = await self._sut.get_info()
        distro_id = info["distro"]
        if not distro_id:
            raise InstallerError("Can't read distribution name")

        return distro_id

    async def _get_distro(self, distro_id: str) -> Installer:
        """
        Return the distribution object.
        """
        if distro_id.startswith(("opensuse", "sles")):
            return SUSELinux()

        if distro_id == "debian":
            return DebianLinux(self._sut)

        if distro_id == "ubuntu":
            return UbuntuLinux(self._sut)

        if distro_id == "fedora":
            return FedoraLinux()

        if distro_id == "alpine":
            return AlpineLinux()

        raise InstallerError(
            f"'{distro_id}' distro is not supported")

    async def _install_requirements(self, distro: LinuxDistro) -> None:
        """
        Install requirements for LTP installation according with Linux distro.
        """
        self._logger.info("Installing requirements")

        pkgs = await distro.setup(self._m32_support)

        await self._run_cmd(distro.refresh_cmd)
        await self._run_cmd(f"{distro.install_cmd} {' '.join(pkgs)}")

        self._logger.info("Requirements has been installed")

    async def _clone_repo(self) -> None:
        """
        Run LTP installation from Git repository.
        """
        args = ""
        if self._branch == "master" and not self._commit:
            args = "--depth=1"

        self._logger.info("Cloning repository..")

        await self._run_cmd(f"git clone {args} {self._url} {self._repo_dir}")

        if self._branch != "master":
            await self._run_cmd(f"git -C {self._repo_dir} checkout {self._branch}")

        if self._commit:
            await self._run_cmd(f"git -C {self._repo_dir} checkout {self._commit}")

        self._logger.info("Repository cloning has been completed")

    async def _install_from_src(self) -> None:
        """
        Run LTP installation from Git repository.
        """
        self._logger.info("Compiling sources")

        ret = await self._run_cmd("getconf _NPROCESSORS_ONLN")
        cpus = ret['stdout'].rstrip()

        await self._run_cmd("make autotools", cwd=self._repo_dir)
        await self._run_cmd(f"./configure --prefix={self._install_dir}",
                            cwd=self._repo_dir)
        await self._run_cmd(f"make -j{cpus}", cwd=self._repo_dir)
        await self._run_cmd("make install", cwd=self._repo_dir)

        self._logger.info(
            "Compiling has been completed")

    async def install(self, buffer: IOBuffer = None) -> None:
        async with self._install_lock:
            self._buffer = buffer

            distro_id = await self._get_distro_id()
            distro = await self._get_distro(distro_id)

            await self._install_requirements(distro)
            await self._clone_repo()
            await self._install_from_src()

    async def stop(self) -> None:
        if not self.is_running:
            return

        self._stop = True

        # wait for install to be completed
        async with self._install_lock:
            pass

        self._stop = False
