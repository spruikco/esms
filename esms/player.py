class Player:
    def __init__(self, name, age=25, nationality="UNK", preferred_side="C",
                 st=1, tk=10, ps=10, sh=10, sm=50, ag=50,
                 kab=100, tab=100, pab=100, sab=100,
                 games=0, saves=0, ktk=0, kps=0, shots=0, goals=0, assists=0,
                 dp=0, injury=0, suspension=0, fitness=100):
        self.name = name
        self.age = age
        self.nationality = nationality
        self.preferred_side = preferred_side
        
        # Skills
        self.st = st  # Shot stopping (GK)
        self.tk = tk  # Tackling
        self.ps = ps  # Passing
        self.sh = sh  # Shooting
        self.sm = sm  # Stamina
        self.ag = ag  # Aggression
        
        # Abilities (potential for skill improvement)
        self.kab = kab  # Shot stopping ability
        self.tab = tab  # Tackling ability
        self.pab = pab  # Passing ability
        self.sab = sab  # Shooting ability
        
        # Statistics
        self.games = games
        self.saves = saves
        self.ktk = ktk  # Key tackles
        self.kps = kps  # Key passes
        self.shots = shots
        self.goals = goals
        self.assists = assists
        
        # Status
        self.dp = dp  # Disciplinary points
        self.injury = injury
        self.suspension = suspension
        self.fitness = fitness
        
        # Match-specific
        self.position = None
        self.side = None
        self.in_game = False
        self.cards = []
        self.subbed_out = False
        
    @classmethod
    def from_roster_line(cls, line):
        """Parse a player from a roster file line"""
        parts = line.strip().split()
        if len(parts) < 21:  # Minimal required fields
            raise ValueError(f"Invalid roster line format: {line}")
        
        name = parts[0]
        age = int(parts[1])
        nationality = parts[2]
        preferred_side = parts[3]
        st = int(parts[4])
        tk = int(parts[5])
        ps = int(parts[6])
        sh = int(parts[7])
        sm = int(parts[8])
        ag = int(parts[9])
        kab = int(parts[10])
        tab = int(parts[11])
        pab = int(parts[12])
        sab = int(parts[13])
        games = int(parts[14])
        saves = int(parts[15])
        ktk = int(parts[16])
        kps = int(parts[17])
        shots = int(parts[18])
        goals = int(parts[19])
        assists = int(parts[20])
        dp = int(parts[21])
        injury = int(parts[22])
        suspension = int(parts[23])
        fitness = int(parts[24])
        
        return cls(
            name=name, age=age, nationality=nationality, preferred_side=preferred_side,
            st=st, tk=tk, ps=ps, sh=sh, sm=sm, ag=ag,
            kab=kab, tab=tab, pab=pab, sab=sab,
            games=games, saves=saves, ktk=ktk, kps=kps, shots=shots, goals=goals, assists=assists,
            dp=dp, injury=injury, suspension=suspension, fitness=fitness
        )
    
    def __str__(self):
        if self.position:
            return f"{self.name} ({self.position})"
        return self.name