# Purpose: Create a combat action simulator for RPGs using user defined combat roles and tables.

The idea here is the game master has NPCs, player allies,
and other character on the field. These character have combat
roles by the GM, combat stances, and other combat-related
aspects that help provide greater nuance during battles or
when the party is trying to gain information.

Each of these aspects requires tables in specific formats.

## Data Files Required

There are three excel format or csv format datafiles required. Thare are:

- choices-tables.xlsx
- combat-tables.xlse
- primary-tables.xlsx

We will start with the format of the worksheets in Primary Tables.

# Primary Tables

This workbook must contain the following tables with names as typed below.

- Combat Outcomes
- Combat Targeting Summary
- Combat Roles
- Combat Role Variations
- Combat Stances

The following tables are optional:

- Combat Surges
- Combat Lulls

## Combat Outcomes

This worksheet requires two columns: Outcome, and Description. Both are composed
of text. The first column will be used to create a list of possible actions
any NPC will take in combat. The second is a description that will be displayed
to the user if they wish to view it.

Examples of Outcomes: Primary Attack (character uses their primary attack),
Secondary Attack (character uses their secondary attack), Ranged Attack
(character uses a ranged attack).

## Combat Targeting Summary

This worksheet has the same format, two columns: Outcome and Description. The
first column will be used to create a list of targets on the opposing side in a
fight, the second a description of what that targeting means in game terms.

Examples of Targeting Outcomes: Closest (character attacks closest target),
Closest Melee (character attacks the closest enemy engaged in melee attacks),
Maneuver (character moves on the battlefield to press their current attack),
Play Dead (character attempts to feign death), Flee (character runs from the
battlefield).

## Combat Roles

This worksheet has two columns: Role and Description. Both are text. The first
column is a list of categories of combatants, the second describing what the
GM means by the terms in the list. 

Examples of Combat Roles: Tank (primary melee fighter), Artillery (primary
ranged combat person), Lurker (character is primarily focuses on ambush tactics
or stealth attacks), Crowd Control (character has spells or abilities that can
control combatants or remove large numbers of them), Support (character has
abilities that heal, buff, or augment abilities of other characters).

## Combat Role Variants

These are more contextual options for combat. There are also two columns:
Role Variant and Description. Again, the first column is a list of possible
contextual variations to the principal combat roles. The second column is
there to clarify what this variation means.

Examples: Mindless (this being cannot plan combat reactions and can change
targets from moment to moment), Minion (this character works for someone
else who generally does the thinking and planning for them), Elite (this is
a special boss type character with greater planning ability and resources),
Rich (this character's special ability is wealth, power, and resources).

## Combat Stances

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

## Optional Item: Combat Surges and Lulls

Generally, RPGs do not allow for things that really can happen in combat.
These are moments when one side or the other surged with energy (surge) or seems to
lose momentum (lull). Usually, this is only one group within a "side" in the 
battle rather than the entire force. This also does not typically happen at
the start of a fight, except when a groups is Well-Fed (surge) or Exhausted
(lull) before the fight or encounter starts.

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
a major impact, escalating over the relative power of those involved.

Examples of Surges: bonuses to initiative rolls, damage bonuses, AC bonuses,
increased difficulty with saving throws for opponents, advantage on rolls

Examples of Lulls: penalties to initiative, reduced damage, disadvantage on
rolls (attack or saving), reduced difficult with saving throws for opponents,
complete fizzles or misses, terrain become difficult terrain for a few rounds.

The surges or lulls generally should impact a small group within a larger
force. They should be benefits of penalties for just that group.
