import logging
from pathlib import Path
from rich.traceback import install
from rich.logging import RichHandler
from subverted import display_info, display_header, SubversionConnector, display_logs

FORMAT = "%(message)s"
logging.basicConfig(format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])

log = logging.getLogger()
log.setLevel(logging.ERROR)
install(show_locals=True)

home_dir = Path.home()
working_dir = Path("/home/cloud/python/Test")

svn = SubversionConnector(working_dir)

display_header(svn)
display_info(svn)
display_logs(svn)


# Print out the "branches" for the repo
# svn = SubversionConnector(working_dir)
# svn.info()
# svn.status()
