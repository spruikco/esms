"""
Tactics management module for ESMS Python.
Based on the original C++ implementation from tactics.cpp.
"""

class TacticsManager:
    """
    Handles players' positions and team tactics, and their multipliers
    for probability calculations. Implemented as a Singleton.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TacticsManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        # Initialize default values
        self.tactics_names = []
        self.positions_names = ["DF", "DM", "MF", "AM", "FW"]
        self.skills_names = ["TK", "PS", "SH"]
        self.tactic_full_name = {}
        self.tact_matrix = {}
        self._initialized = True
    
    def init(self, filename):
        """Initialize tactics from the tactics.dat file"""
        try:
            with open(filename, 'r') as tactfile:
                lines = tactfile.readlines()
        except Exception as e:
            raise Exception(f"Failed to open {filename}: {str(e)}")
            
        # Parse tactics file
        found_tactics_line = False
        mult_lines = []
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            tokens = line.split()
            if len(tokens) == 0:
                continue
                
            # Declaring available tactics
            if tokens[0] == "TACTIC":
                found_tactics_line = True
                
                if len(tokens) < 2 or len(tokens) > 3:
                    raise Exception(f"Illegal TACTIC declaration in {filename}")
                    
                self.tactics_names.append(tokens[1])
                
                if len(tokens) == 3:
                    fullname = tokens[2].replace('_', ' ')
                    self.tactic_full_name[tokens[1]] = fullname
                else:
                    self.tactic_full_name[tokens[1]] = tokens[1]
                    
            # Defining multipliers
            elif tokens[0] in ["MULT", "BONUS"]:
                if not found_tactics_line:
                    raise Exception(f"TACTIC declarations must come first in {filename}")
                    
                mult_lines.append(line)
        
        # Make sure tactics names are unique
        self.tactics_names = list(set(self.tactics_names))
        
        # Initialize the tact_matrix
        self._init_tact_matrix()
        
        # Sort mult_lines - all MULTs must come before all BONUSes
        mult_lines.sort(key=lambda s: 0 if "MULT" in s else 1)
        
        # Set the multipliers from mult_lines
        self._set_multipliers(mult_lines)
        
        # Make sure all multipliers were initialized
        self._ensure_no_uninits()

    def _init_tact_matrix(self):
        """Initialize the tactics matrix with uninitiated values"""
        UNINIT = -1.0  # Uninitialized multiplier
        
        # Initialize a mult_matrix for all positions and skills
        for tactic1 in self.tactics_names:
            for tactic2 in self.tactics_names:
                key = (tactic1, tactic2)
                self.tact_matrix[key] = {}
                
                for pos in self.positions_names:
                    for skill in self.skills_names:
                        self.tact_matrix[key][(pos, skill)] = UNINIT

    def _set_multipliers(self, mult_lines):
        """Parse mult_lines and set multipliers in tact_matrix"""
        UNINIT = -1.0
        
        for line in mult_lines:
            tokens = line.split()
            
            # Handle a MULT line
            # MULT <tactic> <pos> <skill> <multiplier>
            if len(tokens) == 5 and tokens[0] == "MULT":
                tactic = tokens[1]
                position = tokens[2]
                skill = tokens[3]
                value = float(tokens[4])
                
                if tactic not in self.tactics_names:
                    raise Exception(f"In tactics file: In line: {line}\n{tactic} - tactic doesn't exist")
                
                if position not in self.positions_names:
                    raise Exception(f"In tactics file: In line: {line}\n{position} - position doesn't exist")
                
                if skill not in self.skills_names:
                    raise Exception(f"In tactics file: In line: {line}\n{skill} - skill doesn't exist")
                
                # As this is a MULT, assign the value against every tactic
                for tact in self.tactics_names:
                    self.tact_matrix[(tactic, tact)][(position, skill)] = value
            
            # Handle a BONUS line
            # BONUS <tactic> <opp_tactic> <pos> <skill> <bonus>
            elif len(tokens) == 6 and tokens[0] == "BONUS":
                tactic = tokens[1]
                opp_tactic = tokens[2]
                position = tokens[3]
                skill = tokens[4]
                value = float(tokens[5])
                
                if tactic not in self.tactics_names:
                    raise Exception(f"In tactics file: In line: {line}\n{tactic} - tactic doesn't exist")
                
                if opp_tactic not in self.tactics_names:
                    raise Exception(f"In tactics file: In line: {line}\n{opp_tactic} - tactic doesn't exist")
                
                if position not in self.positions_names:
                    raise Exception(f"In tactics file: In line: {line}\n{position} - position doesn't exist")
                
                if skill not in self.skills_names:
                    raise Exception(f"In tactics file: In line: {line}\n{skill} - skill doesn't exist")
                
                # As this is a BONUS, add the value to the designated value
                if self.tact_matrix[(tactic, opp_tactic)][(position, skill)] != UNINIT:
                    self.tact_matrix[(tactic, opp_tactic)][(position, skill)] += value
            
            # Error with arguments
            else:
                raise Exception(f"In tactics file, wrong number of arguments in line: {line}")

    def _ensure_no_uninits(self):
        """Make sure all multipliers have been initialized"""
        UNINIT = -1.0
        errors = []
        
        for tactic1 in self.tactics_names:
            for tactic2 in self.tactics_names:
                for pos in self.positions_names:
                    for skill in self.skills_names:
                        if self.tact_matrix[(tactic1, tactic2)][(pos, skill)] == UNINIT:
                            errors.append(f"{tactic1} {tactic2} {pos} {skill}")
        
        if errors:
            error_msg = "In tactics file, the following multipliers are missing:\n" + "\n".join(errors)
            raise Exception(error_msg)

    def get_mult(self, tactic, opp_tactic, pos, skill):
        """Get the multiplier for a tactic-opp_tactic-pos-skill combination"""
        assert self.tactic_exists(tactic), f"Tactic {tactic} does not exist"
        assert self.tactic_exists(opp_tactic), f"Tactic {opp_tactic} does not exist"
        assert self.position_exists(pos), f"Position {pos} does not exist"
        assert self.skill_exists(skill), f"Skill {skill} does not exist"
        
        return self.tact_matrix[(tactic, opp_tactic)][(pos, skill)]
    
    def tactic_exists(self, tactic):
        """Check if a tactic exists"""
        return tactic in self.tactics_names
    
    def position_exists(self, position):
        """Check if a position exists"""
        return position in self.positions_names
    
    def skill_exists(self, skill):
        """Check if a skill exists"""
        return skill in self.skills_names
    
    def get_tactic_full_name(self, name):
        """Get the full name of a tactic"""
        assert self.tactic_exists(name), f"Tactic {name} does not exist"
        return self.tactic_full_name[name]
    
    def get_positions_names(self):
        """Get the list of position names"""
        return self.positions_names

# Singleton instance
def tact_manager():
    """Get the singleton instance of TacticsManager"""
    return TacticsManager()
