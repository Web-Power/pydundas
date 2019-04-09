__version__ = '1.3.1'

# Nicer namespace for the caller
from .dundas import Session, creds_from_yaml
from .rest.api import Api as Api
