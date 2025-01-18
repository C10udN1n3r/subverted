import subprocess
import logging
from pathlib import Path
from rich.console import Console

log = logging.getLogger()


class SubversionConnector:
    """
    A Wrapper for Subversion operations, providing a pythonic interface for
    managing and interacting with Subversion repositories.
    """

    def __init__(self, repo_path: Path) -> None:
        """Intialize the SubversionConnectior.

        Args:
            repo_path (Path): Path to the local SVN working copy.
        """
        svn_dir = repo_path / ".svn"
        if not (repo_path.exists() and repo_path.is_dir() and svn_dir.exists()):
            Console().print(
                f"Given path is not a valid repo:\n  {repo_path}", style="bold red"
            )
        self.repo_path = repo_path.absolute()

    def _run_command(self, command: list[str]) -> str:
        """Run an SVN command in the repository

        Args:
            command (list[str]): List of command arguments (e.g. ['status])

        Returns:
            str: Output of the SVN command
        """
        try:
            command = ["svn"] + command
            log.debug(f"Running command: \"{' '.join(command)}\"")
            result = subprocess.run(
                command,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )
            if result:
                log.debug(f'Command result: "{result}"')
            return result.stdout.strip()
        except subprocess.CalledProcessError as err:
            raise RuntimeError(
                f"Subversion command failed: {err.stderr.strip()}")

    def status(self) -> str:
        """Get the status of the repo

        Returns:
            str: The output of the "status" command.
        """
        return self._run_command(["status"])

    def log(self, limit: int = 10) -> str:
        """Get the repo logs

        Args:
            limit (int, optional): The max number of log entries to grab. Defaults to 10.

        Returns:
            str: The output of the "log" command.
        """
        return self._run_command(["log", "--limit", str(limit)])

    def update(self) -> str:
        """Update the local repo, pulling in changes from the server.

        Returns:
            str: The output of the "update" command.
        """
        return self._run_command(["update"])

    def add(self, file_path: Path) -> str:
        """Add a file or directory to version control.

        Args:
            file_path (Path): Path to the file or directory to add.

        Returns:
            str: The output of the "add" command.
        """
        if not file_path.exists():
            raise ValueError(f"File or directory does not exist: {file_path}")
        return self._run_command(["add", str(file_path)])

    def commit(self, message: str) -> str:
        """Commits the currently staged files with the given message.

        Args:
            message (str): The message to attach to the commit.

        Raises:
            ValueError: Errors if there is no message included with the commit.

        Returns:
            str: The output of the "commit" command.
        """
        if len(message) == 0 or not message:
            raise ValueError("Must include a message with your commit.")
        return self._run_command(["commit", "-m", message])

    def info(self) -> str:
        """Get the repo information.

            TODO: Implement selecting a specific target and revision

        Returns:
            str: The output of the "info" command.
        """
        # TODO: Implement sylizing the text (might be done in a different file.)
        return self._run_command(["info"])

    def list_branches(self, branch_url: str) -> list[str]:
        """List branches in the repository.

        Args:
            branch_url (str): URL of the branches directory in the repository.

        Returns:
            list[str]: A list of branch names.
        """
        output = self._run_command(["list", branch_url])
        return output.splitlines()

    def diff(self, file_path: Path = None) -> str:
        """Show changes between the working copy and the repository.

        Args:
            file_path (Path, optional): Path to a specific file. Defaults to None.

        Returns:
            str: The output of the "diff" command.
        """
        command = ["diff"]
        if file_path:
            command.append(str(file_path))
        return self._run_command(command)

    def blame(self):
        raise NotImplementedError
