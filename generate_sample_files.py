import os

# Create sample directories if they don't exist
os.makedirs('samples', exist_ok=True)

# Define file contents
files = {
    "samples/home_roster.txt": """[Manchester United]
David De Gea, GK, 8, 10, 9, 12, 5, 5, 6, 18, 16
Luke Shaw, LB, 14, 13, 11, 12, 8, 15, 12, 5, 14
Harry Maguire, CB, 9, 13, 8, 9, 8, 15, 16, 5, 14
Raphael Varane, CB, 12, 12, 10, 10, 7, 16, 15, 5, 16
Aaron Wan-Bissaka, RB, 15, 14, 10, 10, 6, 17, 11, 5, 14
Casemiro, DM, 10, 15, 13, 14, 9, 16, 14, 5, 15
Bruno Fernandes, CM, 12, 14, 16, 17, 14, 10, 11, 5, 13
Christian Eriksen, CM, 9, 12, 15, 17, 13, 8, 10, 5, 12
Marcus Rashford, LW, 17, 14, 15, 13, 15, 8, 10, 5, 12
Jadon Sancho, RW, 15, 13, 16, 14, 13, 7, 8, 5, 11
Cristiano Ronaldo, ST, 14, 13, 16, 11, 18, 6, 16, 5, 14
Mason Greenwood, ST, 15, 12, 14, 10, 16, 7, 12, 5, 12
Antony, RW, 16, 13, 15, 13, 14, 8, 9, 5, 11
Scott McTominay, CM, 12, 15, 11, 12, 11, 14, 13, 5, 13
Fred, CM, 13, 16, 12, 13, 10, 13, 10, 5, 12
Victor Lindelof, CB, 11, 12, 10, 11, 7, 14, 14, 5, 13
Alex Telles, LB, 13, 12, 12, 13, 9, 12, 11, 5, 12
Dean Henderson, GK, 10, 11, 8, 11, 5, 5, 7, 16, 15""",

    "samples/home_teamsheet.txt": """[Manchester United]
[A]
GK: David De Gea
LB: Luke Shaw
CB: Harry Maguire
CB: Raphael Varane
RB: Aaron Wan-Bissaka
DM: Casemiro
CM: Bruno Fernandes
CM: Christian Eriksen
LW: Marcus Rashford
RW: Jadon Sancho
ST: Cristiano Ronaldo""",

    "samples/away_roster.txt": """[Barcelona FC]
Marc-Andre ter Stegen, GK, 9, 11, 12, 15, 5, 5, 7, 17, 16
Jordi Alba, LB, 16, 14, 14, 14, 10, 13, 10, 5, 13
Ronald Araujo, CB, 13, 14, 10, 10, 7, 16, 15, 5, 15
Andreas Christensen, CB, 12, 13, 11, 12, 7, 15, 15, 5, 15
Jules Kounde, RB, 15, 13, 13, 13, 8, 15, 14, 5, 14
Sergio Busquets, DM, 8, 13, 15, 16, 8, 14, 12, 5, 16
Frenkie de Jong, CM, 14, 15, 16, 16, 11, 12, 11, 5, 13
Pedri, CM, 13, 14, 17, 17, 12, 11, 10, 5, 14
Ansu Fati, LW, 17, 12, 16, 13, 15, 7, 10, 5, 12
Ousmane Dembele, RW, 18, 13, 15, 13, 14, 7, 9, 5, 11
Robert Lewandowski, ST, 13, 15, 16, 12, 18, 8, 16, 5, 15
Gavi, CM, 14, 16, 15, 15, 11, 12, 9, 5, 13
Ferran Torres, RW, 15, 13, 14, 12, 15, 8, 11, 5, 12
Raphinha, LW, 16, 14, 15, 14, 15, 8, 10, 5, 12
Franck Kessie, CM, 13, 16, 12, 13, 12, 14, 13, 5, 13
Eric Garcia, CB, 11, 12, 12, 13, 6, 14, 13, 5, 14
Hector Bellerin, RB, 16, 13, 12, 12, 7, 13, 11, 5, 13
Inaki Pena, GK, 10, 10, 9, 11, 5, 5, 6, 15, 14""",

    "samples/away_teamsheet.txt": """[Barcelona FC]
[P]
GK: Marc-Andre ter Stegen
LB: Jordi Alba
CB: Ronald Araujo
CB: Andreas Christensen
RB: Jules Kounde
DM: Sergio Busquets
CM: Frenkie de Jong
CM: Pedri
LW: Ansu Fati
RW: Ousmane Dembele
ST: Robert Lewandowski""",

    "samples/liverpool_roster.txt": """[Liverpool FC]
Alisson Becker, GK, 11, 12, 10, 14, 5, 5, 8, 18, 17
Andrew Robertson, LB, 16, 16, 14, 15, 10, 14, 11, 5, 14
Virgil van Dijk, CB, 13, 14, 12, 12, 9, 18, 17, 5, 17
Ibrahima Konate, CB, 14, 15, 10, 10, 8, 16, 16, 5, 15
Trent Alexander-Arnold, RB, 14, 13, 15, 17, 13, 12, 12, 5, 13
Fabinho, DM, 12, 14, 13, 14, 10, 16, 14, 5, 16
Thiago Alcantara, CM, 11, 12, 18, 18, 12, 11, 10, 5, 14
Jordan Henderson, CM, 12, 16, 13, 15, 11, 14, 13, 5, 15
Luis Diaz, LW, 17, 15, 16, 13, 15, 9, 11, 5, 13
Mohamed Salah, RW, 17, 15, 17, 14, 17, 8, 12, 5, 14
Darwin Nunez, ST, 16, 15, 13, 11, 16, 8, 15, 5, 13
Diogo Jota, ST, 15, 14, 15, 12, 16, 9, 13, 5, 14
Roberto Firmino, CF, 14, 14, 16, 15, 15, 11, 12, 5, 15
Harvey Elliott, CM, 14, 13, 15, 14, 12, 10, 9, 5, 12
James Milner, CM, 11, 15, 13, 14, 11, 13, 12, 5, 15
Joe Gomez, CB, 15, 13, 11, 11, 7, 15, 14, 5, 14
Kostas Tsimikas, LB, 14, 13, 13, 14, 9, 13, 11, 5, 13
Caoimhin Kelleher, GK, 11, 10, 9, 12, 5, 5, 7, 15, 14""",

    "samples/liverpool_teamsheet.txt": """[Liverpool FC]
[N]
GK: Alisson Becker
LB: Andrew Robertson
CB: Virgil van Dijk
CB: Ibrahima Konate
RB: Trent Alexander-Arnold
DM: Fabinho
CM: Thiago Alcantara
CM: Jordan Henderson
LW: Luis Diaz
RW: Mohamed Salah
ST: Darwin Nunez""",

    "samples/bayern_roster.txt": """[Bayern Munich]
Manuel Neuer, GK, 10, 12, 13, 16, 5, 5, 8, 19, 18
Alphonso Davies, LB, 19, 15, 15, 13, 11, 13, 11, 5, 13
Dayot Upamecano, CB, 14, 14, 11, 11, 7, 16, 16, 5, 15
Matthijs de Ligt, CB, 12, 14, 12, 12, 9, 17, 17, 5, 16
Benjamin Pavard, RB, 13, 13, 12, 13, 9, 15, 14, 5, 14
Joshua Kimmich, DM, 13, 15, 16, 17, 12, 15, 13, 5, 16
Leon Goretzka, CM, 14, 16, 14, 15, 14, 13, 15, 5, 14
Thomas Muller, AM, 13, 15, 15, 15, 15, 10, 13, 5, 16
Leroy Sane, LW, 18, 14, 16, 14, 15, 8, 10, 5, 13
Serge Gnabry, RW, 17, 14, 15, 14, 16, 9, 12, 5, 13
Sadio Mane, ST, 17, 15, 16, 13, 16, 10, 13, 5, 15
Kingsley Coman, LW, 18, 14, 15, 13, 14, 8, 11, 5, 12
Jamal Musiala, AM, 16, 13, 17, 16, 14, 9, 10, 5, 14
Marcel Sabitzer, CM, 13, 14, 14, 15, 13, 12, 12, 5, 13
Ryan Gravenberch, CM, 14, 15, 15, 14, 12, 13, 13, 5, 13
Lucas Hernandez, CB, 13, 14, 11, 12, 8, 15, 14, 5, 14
Noussair Mazraoui, RB, 15, 13, 13, 13, 8, 14, 12, 5, 13
Sven Ulreich, GK, 9, 10, 8, 10, 5, 5, 7, 14, 13""",

    "samples/bayern_teamsheet.txt": """[Bayern Munich]
[A]
GK: Manuel Neuer
LB: Alphonso Davies
CB: Dayot Upamecano
CB: Matthijs de Ligt
RB: Benjamin Pavard
DM: Joshua Kimmich
CM: Leon Goretzka
AM: Thomas Muller
LW: Leroy Sane
RW: Serge Gnabry
ST: Sadio Mane"""
}

# Create updated language.dat with enhanced commentary templates
files["language.dat"] = """# Enhanced commentary templates

[goal]
GOAL! {player} scores in the {minute}th minute!
{player} finds the back of the net! What a strike!
{player} scores! The goalkeeper had no chance!
Fantastic finish by {player}!
{player} smashes it into the net!
Brilliant goal by {player}!
What a goal from {player}!
{player} slots it home coolly!
Clinical finish from {player}!
{player} with a moment of magic to score!

[goal_with_assist]
GOAL! {player} scores after a brilliant assist from {assist}!
{player} finishes off a lovely move started by {assist}!
Great vision from {assist} to set up {player} for the goal!
{player} taps it in after excellent work from {assist}!
{assist} with a perfect pass for {player} to finish!
{player} converts after a pinpoint cross from {assist}!
Magnificent team goal! {assist} with the setup, {player} with the finish!
{player} gets on the end of {assist}'s delivery to score!
{assist} finds {player} who makes no mistake with the finish!
Lovely combination between {assist} and {player} for the goal!

[early_game]
An early goal from {player} in the {minute}th minute!
{player} gives his team an early lead!
What a start! {player} scores early on!
{player} wastes no time in getting on the scoresheet!
Early breakthrough for {player}'s team!

[late_game]
A late goal from {player} in the {minute}th minute!
{player} might have just won it with that late strike!
Dramatic late goal from {player}!
{player} scores what could be a crucial goal at this late stage!
{player} with a goal that could change everything in the dying minutes!

[equalizer]
EQUALIZER! {player} levels the score!
{player} brings the teams level with that goal!
Game on! {player} with the equalizing goal!
{player} ties the game with a crucial strike!
All square now thanks to {player}'s goal!

[go_ahead]
{player} puts his team in front with that goal!
{player} gives his team the lead!
Breakthrough goal from {player} to take the lead!
{player} scores what could be the winning goal!
{player} delivers when it matters most to take the lead!

[extend_lead]
{player} extends the lead further!
Another goal, this time from {player}!
{player} puts the game beyond doubt with that goal!
{player} adds to the tally!
{player} with a goal to seal the victory!

[save]
Great save by {goalkeeper} to deny {player}!
{goalkeeper} keeps it out with a fantastic stop!
Brilliant reflexes from {goalkeeper} to stop {player}'s effort!
{player} is denied by an excellent save from {goalkeeper}!
{goalkeeper} gets down well to keep out {player}'s shot!
Magnificent goalkeeping from {goalkeeper}!
{player} can't believe {goalkeeper} kept that one out!
Superb save! {goalkeeper} shows his quality!
{goalkeeper} with a save that keeps his team in the game!
What a stop by {goalkeeper} from {player}'s attempt!

[miss]
{player} puts the shot wide of the target!
Close but not close enough from {player}!
{player} should have done better with that chance!
Off target from {player}!
{player} fails to hit the target with that attempt!
{player} blazes the shot over the bar!
{player} misses a golden opportunity!
{player} can't keep the shot down!
{player} drags his effort wide!
{player} sends the ball into the stands!

[cross]
{player} delivers a dangerous cross towards {target}!
Great ball in from {player} looking for {target}!
{player} whips in a cross for {target}!
{player} with an inviting delivery towards {target}!
{player} sends in a teasing cross for {target} to attack!
{player} bends in a beautiful cross towards {target}!
Excellent delivery from {player} aiming for {target}!
{player} with a pinpoint cross for {target}!
{target} is the target as {player} delivers the cross!
{player} floats a cross into the area for {target}!

[failed_cross]
{player}'s cross is intercepted by {defender}!
{defender} clears the cross from {player}!
Poor delivery from {player}, easily dealt with by {defender}!
{player}'s cross doesn't beat the first man, {defender}!
{defender} heads away {player}'s cross!
{player} overhits the cross and {defender} clears!
{defender} reads {player}'s cross well and cuts it out!
{player}'s delivery is too close to {defender} who clears!
{defender} makes an important interception from {player}'s cross!
{player}'s cross is blocked by {defender}!

[through_ball]
Brilliant through ball from {player} to {target}!
{player} threads a pass through to {target}!
{player} with a defense-splitting pass for {target}!
Excellent vision from {player} to find {target}!
{player} picks out {target} with a perfect through ball!
{player} slides a pass between defenders for {target} to run onto!
{target} is through on goal thanks to {player}'s pass!
{player} with a delightful ball for {target} to chase!
{player} unlocks the defense with a pass to {target}!
Great awareness from {player} to spot {target}'s run!

[failed_through_ball]
{player}'s through ball is cut out by {defender}!
{defender} reads {player}'s intentions and intercepts!
{player} tries to find a teammate but {defender} is alert to the danger!
{defender} steps in to cut out {player}'s pass!
{player}'s attempted through ball is blocked by {defender}!
{defender} makes a crucial interception to stop {player}'s pass!
{player} overplays the pass and {defender} clears!
{defender} anticipates {player}'s through ball!
{player}'s pass is too ambitious and {defender} intercepts!
{defender} shows good defensive awareness to cut out {player}'s pass!

[dribble]
{player} dribbles past {defender} with ease!
Lovely skill from {player} to beat {defender}!
{player} leaves {defender} trailing with a great piece of skill!
{defender} can't keep up with {player}'s quick feet!
{player} shows great control to get past {defender}!
Brilliant dribbling by {player}, making {defender} look silly!
{player} glides past {defender} with a silky move!
{defender} is beaten all ends up by {player}!
{player} with a wonderful piece of skill to beat {defender}!
{player} shows his class to dance past {defender}!

[tackle]
Strong tackle from {defender} to win the ball from {player}!
{defender} with a crunching challenge on {player}!
Great defensive work by {defender} to dispossess {player}!
{defender} times the tackle perfectly to take the ball from {player}!
{player} is stopped in his tracks by {defender}'s challenge!
{defender} shows his defensive quality with that tackle on {player}!
{player} loses out to a firm but fair challenge from {defender}!
{defender} with a clean tackle to win possession from {player}!
Excellent tackle by {defender} to stop {player}'s advance!
{defender} reads the situation well to tackle {player}!

[interception]
{defender} intercepts the pass from {player}!
Good anticipation by {defender} to cut out {player}'s pass!
{defender} reads the play well to intercept {player}'s pass!
{player}'s pass is too predictable and {defender} steps in!
{defender} cuts out the intended pass from {player}!
{defender} shows good awareness to intercept {player}'s ball!
{player}'s sloppy pass is picked off by {defender}!
{defender} positions himself well to intercept {player}'s pass!
{player} gives the ball away and {defender} intercepts!
Quick thinking from {defender} to step in front of {player}'s pass!

[pass]
{player} finds {target} with a neat pass!
Good ball from {player} to {target}!
{player} keeps possession moving with a pass to {target}!
{player} picks out {target} with precision!
{target} receives the ball from {player}!
Calm and composed pass from {player} to {target}!
{player} looks up and finds {target} in space!
{player} switches the play to {target}!
{target} is found by a measured pass from {player}!
{player} feeds the ball to {target}!

[foul]
{player} commits a foul on {victim}!
Free kick awarded after {player} fouled {victim}!
{player} brings down {victim} - that's a foul!
The referee penalizes {player} for a challenge on {victim}!
{victim} is fouled by {player}!
{player} catches {victim} late and concedes a free kick!
{player} with a clumsy challenge on {victim}!
{victim} goes down under {player}'s challenge!
{player} doesn't time the tackle right and fouls {victim}!
{victim} wins a free kick after being fouled by {player}!

[yellow_card]
YELLOW CARD! {player} is booked for the foul on {victim}!
{player} goes into the referee's book for that challenge on {victim}!
{player} receives a yellow card for the foul on {victim}!
The referee shows {player} a yellow card!
{player} is cautioned after bringing down {victim}!
Yellow card for {player} after that rash tackle on {victim}!
{player} can have no complaints about the yellow card for that foul on {victim}!
{player} is walking a tightrope now after being booked for the foul on {victim}!
{victim} stays down and {player} is shown a yellow card!
The referee reaches for his pocket and shows {player} a yellow card!

[red_card]
RED CARD! {player} is sent off for the foul on {victim}!
{player} receives his second yellow and is OFF!
The referee shows {player} a straight red card!
{player} is dismissed after a terrible challenge on {victim}!
Early shower for {player} as he sees red for the foul on {victim}!
{player} can have no complaints about the red card for that horror tackle on {victim}!
{player} leaves his team with 10 men after being sent off!
Disaster for {player}'s team as he's shown a red card!
The referee has no choice but to send {player} off for that!
{player} will play no further part in this match after receiving a red card!"""

# Create simple tactics.dat file
files["tactics.dat"] = """# Simple tactics definitions
# Format: [TACTIC_CODE], TACTIC_NAME, EFFECT1:VALUE, EFFECT2:VALUE, ...

[N], Normal, attacking_boost:0, defensive_boost:0, attacking_penalty:0, defensive_penalty:0
[A], Attacking, attacking_boost:2, defensive_boost:0, attacking_penalty:0, defensive_penalty:1
[D], Defensive, attacking_boost:0, defensive_boost:2, attacking_penalty:1, defensive_penalty:0
[P], Possession, passing_boost:2, counter_bonus:0, attacking_penalty:0, defensive_penalty:0
[C], Counter, counter_bonus:2, attacking_penalty:1, defensive_boost:1, passing_boost:0"""

# Write all files
print("Creating sample files...")
for filename, content in files.items():
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {filename}")

print("\nAll sample files created successfully!")
print("\nTo use these files in your ESMS simulation, you can:")
print("1. Run '/sample' route to use home_roster.txt and away_roster.txt automatically")
print("2. Upload these files manually through the web interface")
print("3. Copy them to appropriate locations in your project structure")