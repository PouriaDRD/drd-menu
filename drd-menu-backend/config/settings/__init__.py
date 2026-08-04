from ..app_config import config

if config.app.debug:
    from .development import *
else:
    from .production import *
