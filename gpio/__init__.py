from .classes import Config

# Read config
config = Config("config.yml")

# Load everything else
from . import devices
from . import utils