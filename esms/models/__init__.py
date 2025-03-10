# esms/models/__init__.py
from extensions import db

# Import models to make them available from the package
# These imports will be uncommented as you implement each model
# from esms.models.user import User
from esms.models.team import Team
from esms.models.player import Player
from esms.models.match import Match