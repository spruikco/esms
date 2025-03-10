# esms/models/__init__.py
from extensions import db

# Import models to make them available from the package
from esms.models.team import Team
from esms.models.player import Player
from esms.models.match import Match
from esms.models.formation import Formation  # Add this line