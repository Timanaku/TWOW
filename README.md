# Arcane Missile Haste & DPS Calculator

This calculator helps you determine the effective cast time, number of missiles fired, and other related metrics for an Arcane-based spell scenario with varying haste values and buffs.

## Overview

The calculation simulates the casting of a channeled spell (e.g., Arcane Missiles) with:
- A base cast time of 5 seconds, plus a fixed extra 1 second from a special belt (for a total of 6 seconds before haste).
- Haste scaling affects both the initial 5-second portion of the cast and the missile-firing intervals.
- The 1-second portion added by the belt is unaffected by haste.

By combining:
- Selected buffs (which have multiplicative haste factors)
- Gear haste percentages (entered by the user)
  
The calculator computes:
- **Total Cast Time:** The hasted cast duration (5/H + 1, where H is total haste multiplier).
- **Missile Intervals:** Adjusted by haste, each missile fires faster as haste increases.
- **Missiles Fired:** How many missiles fire in total, both floored (as actually occurs) and unfloored (theoretical fractional count).
- **Deadzone:** The leftover fraction of the cast time after the last missile is fired.

## How the Calculations Work

1. **Haste Calculation:**
   - Start with a base haste value of 1.0 (no haste).
   - For each selected buff, multiply the total haste by that buff’s haste factor.
   - For each gear piece, convert its haste percent into a multiplier (e.g., 3% = 1.03) and multiply it into the total haste.
   
   Example: If you have Berserking (1.10) and Accelerated Arcana (1.05), and gear with 3% and 2% haste, total haste = 1.0 * 1.10 * 1.05 * 1.03 * 1.02.

2. **Cast Time & Intervals:**
   - Total Cast Time = `(5 / H) + 1`
   - Missile Interval = `(0.95 / H)`

3. **Missile Counts & Deadzone:**
   - Floored Missiles = `floor((5 + H) / 0.95)`
   - Unfloored Missiles = `(5 + H) / 0.95`
   - Deadzone = `Total Cast Time - (Missiles_Floored * Missile_Interval)`

## How to Use the Calculator

1. **Run the Program:**
    - Run the arcanecalc.exe

2. **Select Buffs:**
   - The UI presents checkboxes for available buffs (e.g., Berserking, Arcane Power, etc.).
   - Check the buffs you have active.

3. **Enter Gear Haste:**
   - Enter your gear haste values in the provided field as comma-separated percentages.
   - For example: `3, 2, 5` means you have one piece with 3% haste, another with 2%, and a third with 5%.

4. **Calculate:**
   - Click the "Calculate" button.
   - The results will display:
     - Your total haste percentage
     - Total cast time
     - Floored and unfloored missile counts
     - The deadzone in seconds

5. **Experiment:**
   - Try changing buffs or gear haste values to see how they affect your total haste, missile numbers and missile deadzone

