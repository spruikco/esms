"""
Script to copy tactics.dat and language.dat files to the correct location
"""
import os
import shutil

def main():
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Source files
    source_tactics = os.path.join(script_dir, "samples", "tactics.dat")
    source_language = os.path.join(script_dir, "samples", "language.dat")
    
    # Destination files
    dest_tactics = os.path.join(script_dir, "tactics.dat")
    dest_language = os.path.join(script_dir, "language.dat")
    
    # Create samples directory if it doesn't exist
    os.makedirs(os.path.join(script_dir, "samples"), exist_ok=True)
    
    # Copy tactics.dat and language.dat to samples directory
    try:
        # Write tactics.dat to samples directory
        if not os.path.exists(source_tactics):
            with open(source_tactics, 'w') as f:
                # Copy the content from the document you provided
                f.write("""# All tactics must be first defined here.
# Later, the full set of multipliers must be set for each tactic
TACTIC N Normal
TACTIC D Defensive
TACTIC A Attacking
TACTIC C Counter_Attack
TACTIC L Long_Ball
TACTIC P Passing


# N - Normal
MULT N DF TK 1.0
MULT N DF PS 0.5
MULT N DF SH 0.3

MULT N DM TK 0.85
MULT N DM PS 0.75
MULT N DM SH 0.3

MULT N MF TK 0.3
MULT N MF PS 1.0
MULT N MF SH 0.3

MULT N AM TK 0.3
MULT N AM PS 0.85
MULT N AM SH 0.85

MULT N FW TK 0.3
MULT N FW PS 0.3
MULT N FW SH 1.0



# D - Defensive
MULT D DF TK 1.25
MULT D DF PS 0.5
MULT D DF SH 0.25

MULT D DM TK 1.13
MULT D DM PS 0.68
MULT D DM SH 0.25

MULT D MF TK 1.0
MULT D MF PS 0.75
MULT D MF SH 0.25

MULT D AM TK 0.75
MULT D AM PS 0.65
MULT D AM SH 0.5

MULT D FW TK 0.5
MULT D FW PS 0.25
MULT D FW SH 0.75

BONUS D L DF TK 0.25



# A - Attacking
MULT A DF TK 1.0
MULT A DF PS 0.5
MULT A DF SH 0.5

MULT A DM TK 0.5
MULT A DM PS 0.75
MULT A DM SH 0.68

MULT A MF TK 0.0
MULT A MF PS 1.0
MULT A MF SH 0.75

MULT A AM TK 0.0
MULT A AM PS 0.87
MULT A AM SH 1.13

MULT A FW TK 0.0
MULT A FW PS 0.75
MULT A FW SH 1.5



# C - Counter attack
MULT C DF TK 1.0
MULT C DF PS 0.5
MULT C DF SH 0.25

MULT C DM TK 0.85
MULT C DM PS 0.85
MULT C DM SH 0.25

MULT C MF TK 0.5
MULT C MF PS 1.0
MULT C MF SH 0.25

MULT C AM TK 0.5
MULT C AM PS 0.85
MULT C AM SH 0.65

MULT C FW TK 0.5
MULT C FW PS 0.5 
MULT C FW SH 1.0

BONUS C A MF SH 0.5
BONUS C A DF PS 0.25
BONUS C A DF SH 0.25
BONUS C P MF SH 0.5
BONUS C P DF PS 0.25
BONUS C P DF SH 0.25



# L - Long ball
MULT L DF TK 1.0
MULT L DF PS 0.25
MULT L DF SH 0.25

MULT L DM TK 0.75
MULT L DM PS 0.85
MULT L DM SH 0.38

MULT L MF TK 0.5
MULT L MF PS 1.0
MULT L MF SH 0.5 

MULT L AM TK 0.45
MULT L AM PS 0.85
MULT L AM SH 0.9

MULT L FW TK 0.25
MULT L FW PS 0.5 
MULT L FW SH 1.3

BONUS L C DF TK 0.25
BONUS L C DF PS 0.5



# P - Passing
MULT P DF TK 1.0
MULT P DF PS 0.75
MULT P DF SH 0.3 

MULT P DM TK 0.87
MULT P DM PS 0.87
MULT P DM SH 0.28

MULT P MF TK 0.25
MULT P MF PS 1.0
MULT P MF SH 0.25

MULT P AM TK 0.25
MULT P AM PS 0.87
MULT P AM SH 0.68

MULT P FW TK 0.25
MULT P FW PS 0.75
MULT P FW SH 1.0

BONUS P L MF SH 0.5
BONUS P L MF TK 0.5
BONUS P L FW SH 0.25""")
            print(f"Created tactics.dat in samples directory")
        
        # Write language.dat to samples directory (adding just a small part for brevity)
        if not os.path.exists(source_language):
            with open(source_language, 'w') as f:
                # Add a small subset of the language file
                f.write("""| A scoring chance
| 1st %s - game minute
| 2nd %s - team abbrevation
| 3rd %s - player name

[CHANCE] {\\nMin. %s :(%s) %s with the dribble}
[CHANCE] {\\nMin. %s :(%s) %s takes possesion}
[CHANCE] {\\nMin. %s :(%s) %s cuts through the defense}
[CHANCE] {\\nMin. %s :(%s) %s finds a hole in the defense}

| A shot to goal
| 1st %s - player name

[SHOT] {\\n          ...  A powerful shot by %s !}
[SHOT] {\\n          ...  %s tries to beat the keeper !}
[SHOT] {\\n          ...  %s with the strike !}

| A goal was scored

[GOAL] {\\n          ...  GOAL !!}

| A save (by the goalkeeper)
| 1st %s - goalkeeper name

[SAVE] {\\n          ...  Saved by %s}
[SAVE] {\\n          ...  %s gathers it comfortably}
[SAVE] {\\n          ...  %s makes a comfortable save}

| Various statistic and informational lines

[COMM_KICKOFF]  {\\n*************  KICK OFF  *****************}
[COMM_HALFTIME] {\\n*************  HALF TIME  ****************}
[COMM_FULLTIME] {\\n*************  FULL TIME  ****************}""")
            print(f"Created language.dat in samples directory")
    
        # Copy files to main directory
        if os.path.exists(source_tactics):
            shutil.copy(source_tactics, dest_tactics)
            print(f"Copied tactics.dat to {dest_tactics}")
        
        if os.path.exists(source_language):
            shutil.copy(source_language, dest_language)
            print(f"Copied language.dat to {dest_language}")
        
        print("Configuration files copied successfully")
    
    except Exception as e:
        print(f"Error copying configuration files: {str(e)}")
        
if __name__ == "__main__":
    main()
