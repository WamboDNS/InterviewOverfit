# Game Configuration

This directory contains the data-driven configuration for the game mechanics.

## Files

### `gameConfig.json`
The main configuration file containing all game mechanics:

- **initialStats**: Starting values for HP, time, combo
- **damage**: Damage calculation parameters
- **scoring**: Score calculation multipliers
- **combo**: Combo system thresholds
- **starCalculation**: Star rating calculation
- **timing**: Game timing settings

### `types.ts`
TypeScript interfaces for type safety.

### `loader.ts`
Configuration loader utility.

## Usage

The configuration is automatically loaded when the GameBattle component initializes. All game mechanics are now driven by this configuration file.

## Customization

To modify game mechanics, simply edit the values in `gameConfig.json`:

- Change `initialStats.userHp` to modify starting player health
- Adjust `damage.minDamage` and `damage.maxDamage` for damage range
- Modify `scoring.damageMultiplier` to change score calculation
- Update `timing.gameEndDelay` to change game end delay

No code changes required - just update the JSON file!
