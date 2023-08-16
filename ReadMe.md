# Purpose: Create a combat action simulator for RPGs using user defined combat roles and tables.

The idea here is the game master has NPCs, player allies,
and other characters/beings on the field. These characters have combat
roles, combat stances, and other combat-related aspects assigned by the GM or
their "class" that nuance the choices the character would make
during battles.

Each of these aspects requires tables in specific formats.

## Data Files Required

There are two excel format workbooks required. These are:

- combat-tables.xlsx
- configuration-tables.xlsx

We will start with the format of the worksheets in Configuration Tables.

## Configuration Tables

This workbook must contain the following tables with names as typed below.

- Combat Outcomes
- Combat Targeting Summary
- Combat Roles
- Combat Stances

The following tables are optional:

- Combat Role Variations
- Combat Surges
- Combat Lulls

## Required Tables

### Combat Outcomes

This worksheet requires two columns: Outcome, and Description. Both are composed
of text. The first column will be used to create a list of possible actions
any NPC will take in combat. The second is a description that will be displayed
to the user if they wish to view it.

Examples of Outcomes: Primary Attack (character uses their primary attack),
Secondary Attack (character uses their secondary attack), Ranged Attack
(character uses a ranged attack).

### Combat Targeting Summary

This worksheet has the same format, two columns: Outcome and Description. The
first column will be used to create a list of targets on the opposing side in a
fight, the second a description of what that targeting means in game terms.

Examples of Targeting Outcomes: Closest (character attacks closest target),
Closest Melee (character attacks the closest enemy engaged in melee attacks),
Maneuver (character moves on the battlefield to press their current attack),
Play Dead (character attempts to feign death), Flee (character runs from the
battlefield), Disengage (character attempts to disengage from their current
foes).

### Combat Roles

This worksheet has two columns: Role and Description. Both are text. The first
column is a list of categories of combatants, the second describing what the
GM means by the terms in the list. 

Examples of Combat Roles: Tank (primary melee fighter), Artillery (primary
ranged combat person), Lurker (character is primarily focuses on ambush tactics
or stealth attacks), Crowd Control (character has spells or abilities that can
control combatants or remove large numbers of them), Support (character has
abilities that heal, buff, or augment abilities of other characters). Character
Class names are also valid combat role options, but that can increase the 
number of combat tables substantially (see Section: Combat Tables).

### Combat Stances

This is another contextual element of combat. It is intended to allow GMs to
handle how well rested characters are, their mental state, or their recent
actions. Again, this worksheet has two columns: Role and Description.

Examples: Well-Fed (character has full energy and even some bonuses due to rest
and eating well recently), Exhausted (character has been unable to rest),
Ambush (character has been waiting to ambush anyone who shows up), Unprepared
(character was trying to rest and is not in their primary armor, probably does
not have all their equipment immediately handy either), Mindless (character is 
a zombie or similar creature that requires no rest, but is not capable of 
thinking).

## Optional Configuration Tables

### Combat Role Variants

These are more contextual options for combat. That is also why they are optional
There are two columns: Role Variant and Description. Again, the first column is 
a list of possible contextual variations to the principal combat roles. The
second column is there to clarify what this variation means.

Examples: Mindless (this being cannot plan combat reactions and can change
targets from moment to moment), Minion (this character works for someone
else who generally does the thinking and planning for them), Elite (this is
a special boss type character with greater planning ability and resources),
Rich (this character's special ability is wealth, power, and resources).

### Combat Surges and Lulls

Generally, RPGs do not allow for things that really can happen in combat.
These are moments when one side or the other surged with energy (surge) or
loses momentum (lull). Usually, this is only a small subset within a "side"
in the battle rather than the entire force. This also does not typically 
happen at the start of a fight, except when a groups is Well-Fed (surge)
or Exhausted (lull) before the fight or encounter starts.

This two worksheets have nine columns. The first must be a copy of the Outcome
column from Combat Outcomes above. There are two sets of four columns that
are labeled as follows:

- Minor Low
- Minor Moderate
- Minor Advanced
- Minor Elite
- Major Low
- Major Moderate
- Major Advanced
- Major Elite

The first set are for minor surges or lulls. These should have some impact on 
combat, but not a huge effect. Low, Moderate, Advanced, and Elite are intended
to indicate how powerful these characters are relative to normal people in
game. The second set are for major surges or lulls. These effects should have
a major impact, escalating over the relative power of those involved. You can
define one of the four as "equivalent" to a party of PCs and use the other
three to define stronger or weaker. Reserve Elite for the boss NPCs (not all
of whom have to be villains).

__Note__: You can use roll for PCs Outcomes to see if a surge or lull is called
for, even though the character is not bound to follow the outcome. It might even
suggest their next actions if the surge or lull affects special abilities.

Examples of Surges: bonuses to initiative rolls, damage bonuses, AC bonuses,
increased difficulty with saving throws for opponents, advantage on rolls

Examples of Lulls: penalties to initiative, reduced damage, disadvantage on
rolls (attack or saving), reduced difficult with saving throws for opponents,
complete fizzles or misses, terrain become difficult terrain for a few rounds.

The surges or lulls generally should impact a small group within a larger
force. They should be benefits or penalties that only apply to the members of
the force who share the same Combat Role, Combat Role Variant, or Combat
Outcome. For PCs, use Combat Role.

# Combat Tables

## Basic Format of Each Table

Once you have decided on the required combat outcomes, targets, roles,
stances, and the optional items, role variants, surges and/or lulls, these
will dictate the Combat Table content. All of these tables require five
columns: A, B, C, D, and Outcome. 

### Dice Rolls (Columns A, B, C, and D)

The first four columns are labeled generically A, B, C, and D. This allows
the GM to scale their combat tables if they wish. For 5th ED D&D, this could
be by monster/creature Tier. For games that do not use levels, like Hero 
System, GURPS, or The Fantasy Trip, it could how many points went into
building the character.

The contents of a field in these four columns must be one of the following:

- a single integer
- a range of values, written 'low integer-high integer' without spaces
- a single dash. '-'

A dash is used to indicate that the option is not possible in the current
combination of contexts. For example, Ambushing Barbarian should not choose
to Flee or Disengage at the start of a fight. Integer values indicate how
likely the action will be chosen by the character in that context. Do not
overlap values, nor should you leave gaps. When the program reads the table,
it will calculate the minimum value and maximum value for the table column
before choosing a random number in that range. This roll will be based a 
uniform distribution for each integer value, like a d100.

__Note__: When the table is first loaded, it is validated and will display
an error message detailing what is wrong with its content. Dashes are not
considered "gaps" in values. Gaps occur when values in a column do not
cover all possible integers from the lowest to the highest value.

__Note__: If you do not wish to use scaling, use Column A for the numbers you
wish to use in the combat tables and leave dashes in the other columns. That is
not an invalid setup. The program will ignore as unused Columns B, C, or D if
they are all dashes. It will display a message indicating that it is ignoring
a column.

### Outcome (Column 5)

The fifth column must be Outcome. This should be contain the combat outcomes
defined the Combat Outcomes worksheet in configuration-tables.xlsx. If you
choose to use Combat Surges, repeat all of the outcomes once including Minor
Surge in the outcome. Do the same for Major Surge, Minor Lull and Major Lull
if you wish to include any of these variations.

## Naming Convention for Combat Tables

__Note__: Excel currently has a hard limit of 31 alphanumeric characters for
each worksheet name. You will need to truncate the name of the table
accordingly.  The program will handle find it with the truncated name.

The tables require a specific order of items in the title, each separated 
by a single space. Unless specified otherwise, the item is required.

1. Combat Role
2. Combat Role Variant (optional, active if table exists)
3. Combat Stance
4. Action or Targeting

Both an Action and a Targeting tables for each combination of combat role,
combat role variant, and combat stance should exist. Duplicate the worksheet
if you don't want to make each combination unique. If one of the variations
does not exist, this will not be reflected in the GUI.

Examples: Tank (role) Minion (variant) Well-Fed (stance) would be the
action table for a tank minion who ate food with a buff recently. Fighter
(role) Elite (variant) Bloodied (stance) could indicate an exceptional
fighter class boss who has suffered significant loss of hit points in the
fight thus far. The worksheet titles for both examples would appear as
indicated belows

- Tank Minion Well-Fed Action
- Tank Minion Well-Fed Targeting
- Fighter Elite Bloodied Action
- Fighter Elite Bloodied Targetin

The targeting table for the exceptional fighter boss had to be truncated to
31 characters, hence the missing 'g'.
