import random
from datetime import datetime
from extensions import db
from enhanced_app import app
from models import Team, Player, TeamPlayer, User

# Lists of sample names and nationalities for random generation
first_names = [
    "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles",
    "Daniel", "Matthew", "Anthony", "Mark", "Donald", "Steven", "Paul", "Andrew", "Joshua", "Kenneth",
    "Kevin", "Brian", "George", "Timothy", "Ronald", "Jason", "Edward", "Jeffrey", "Ryan", "Jacob",
    "Gary", "Nicholas", "Eric", "Stephen", "Jonathan", "Larry", "Justin", "Scott", "Brandon", "Benjamin",
    "Liam", "Noah", "Oliver", "Elijah", "Lucas", "Mason", "Logan", "Ethan", "Jackson", "Aiden"
]

last_names = [
    "Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor",
    "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson",
    "Clark", "Rodriguez", "Lewis", "Lee", "Walker", "Hall", "Allen", "Young", "Hernandez", "King",
    "Wright", "Lopez", "Hill", "Scott", "Green", "Adams", "Baker", "Gonzalez", "Nelson", "Carter",
    "Mitchell", "Perez", "Roberts", "Turner", "Phillips", "Campbell", "Parker", "Evans", "Edwards", "Collins"
]

nationalities = [
    "England", "Spain", "Germany", "France", "Italy", "Netherlands", "Belgium", "Portugal", "Argentina", "Brazil",
    "Uruguay", "Colombia", "Chile", "Mexico", "United States", "Denmark", "Sweden", "Norway", "Switzerland", "Croatia",
    "Serbia", "Poland", "Ukraine", "Russia", "Senegal", "Ivory Coast", "Nigeria", "Ghana", "Egypt", "Cameroon",
    "Japan", "South Korea", "Australia", "Canada", "Turkey", "Austria", "Czech Republic", "Scotland", "Wales", "Ireland"
]

def get_position_attributes(position):
    """Generate realistic attributes for a player based on their position"""
    # Base attributes - will be modified based on position
    attributes = {
        'speed': random.randint(8, 14),
        'stamina': random.randint(8, 14),
        'technique': random.randint(8, 14),
        'passing': random.randint(8, 14),
        'shooting': random.randint(8, 14),
        'tackling': random.randint(8, 14),
        'heading': random.randint(8, 14),
        'goalkeeper': random.randint(2, 6),  # Low for non-GKs
        'positioning': random.randint(8, 14)
    }
    
    # Position-specific attribute modifiers
    if position == 'GK':  # Goalkeeper
        attributes['goalkeeper'] = random.randint(14, 18)
        attributes['positioning'] = random.randint(12, 16)
        attributes['shooting'] = random.randint(2, 6)
    
    elif position in ['CB', 'LB', 'RB']:  # Defenders
        attributes['tackling'] = random.randint(14, 18)
        attributes['heading'] = random.randint(12, 17) if position == 'CB' else random.randint(8, 14)
        attributes['positioning'] = random.randint(13, 17)
        attributes['shooting'] = random.randint(4, 9)
        
    elif position in ['DM', 'CM']:  # Defensive/Central Midfielders
        attributes['passing'] = random.randint(12, 16)
        attributes['stamina'] = random.randint(13, 17)
        attributes['tackling'] = random.randint(11, 16) if position == 'DM' else random.randint(9, 14)
        
    elif position in ['LM', 'RM', 'AM']:  # Midfielders
        attributes['passing'] = random.randint(13, 18)
        attributes['technique'] = random.randint(13, 17)
        attributes['speed'] = random.randint(12, 16) if position in ['LM', 'RM'] else random.randint(9, 15)
        
    elif position in ['LW', 'RW']:  # Wingers
        attributes['speed'] = random.randint(14, 18)
        attributes['technique'] = random.randint(13, 17)
        attributes['shooting'] = random.randint(11, 16)
        
    elif position in ['ST', 'CF']:  # Strikers
        attributes['shooting'] = random.randint(14, 18)
        attributes['heading'] = random.randint(13, 17)
        attributes['speed'] = random.randint(11, 17)
        attributes['tackling'] = random.randint(5, 9)
        
    return attributes

def create_user_if_needed(username="admin", email="admin@example.com"):
    """Create a user if none exists"""
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username, email=email)
            user.set_password("password")
            db.session.add(user)
            db.session.commit()
            print(f"Created user: {username}")
        return user

def create_team_with_players(team_name="Arsenal FC", user_id=1):
    """Create a team with 25 players of various positions"""
    with app.app_context():
        # Check if user exists, create if needed
        user = User.query.get(user_id)
        if not user:
            user = create_user_if_needed()
            user_id = user.id
            
        # Create the team
        team = Team(name=team_name, user_id=user_id, formation="4-3-3")
        db.session.add(team)
        db.session.flush()  # Get the team ID before committing
        
        # Define the positions we need (for a complete squad)
        positions = {
            'GK': 3,        # 3 goalkeepers
            'CB': 4,        # 4 center backs
            'LB': 2,        # 2 left backs
            'RB': 2,        # 2 right backs
            'DM': 2,        # 2 defensive midfielders
            'CM': 3,        # 3 central midfielders
            'LM': 1,        # 1 left midfielder
            'RM': 1,        # 1 right midfielder
            'AM': 1,        # 1 attacking midfielder
            'LW': 2,        # 2 left wingers
            'RW': 2,        # 2 right wingers
            'ST': 2         # 2 strikers
        }
        
        player_count = 0
        # Create players for each position
        for position, count in positions.items():
            for i in range(count):
                player_count += 1
                # Generate player details
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
                full_name = f"{first_name} {last_name}"
                age = random.randint(18, 35)
                nationality = random.choice(nationalities)
                
                # Get position-appropriate attributes
                attributes = get_position_attributes(position)
                
                # Create the player
                player = Player(
                    first_name=first_name,
                    last_name=last_name,
                    name=full_name,
                    age=age,
                    nationality=nationality,
                    primary_position=position,
                    **attributes
                )
                
                db.session.add(player)
                db.session.flush()  # Get the player ID
                
                # Assign the player to the team with their position
                team_player = TeamPlayer(
                    team_id=team.id,
                    player_id=player.id,
                    position=position
                )
                db.session.add(team_player)
                
                print(f"Created player {player_count}/25: {full_name} ({position})")
        
        # Commit all changes
        db.session.commit()
        
        print(f"Created team '{team_name}' with 25 players")
        return team

def create_sample_teams():
    """Create multiple sample teams"""
    teams = [
        "Arsenal FC",
        "Manchester United",
        "Liverpool FC",
        "Chelsea FC"
    ]
    
    for team_name in teams:
        create_team_with_players(team_name)

if __name__ == "__main__":
    # You can customize the team name or create multiple teams
    create_team_with_players("Arsenal FC")
    # Uncomment to create multiple teams:
    # create_sample_teams()