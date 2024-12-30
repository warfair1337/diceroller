import random

def clear_screen():
    """
    Clear the terminal screen using ANSI escape codes.
    """
    # \033[2J = clear screen, \033[H = move cursor to home (top-left) position
    print("\033[2J\033[H", end="")

def roll_die(num_sides, dice_so_far, is_bad_gambler):
    """
    Roll a single die with possible 'Bad Gambler' skew:
      - If is_bad_gambler is False: normal roll in [1..num_sides].
      - If is_bad_gambler is True:
         (a) 30% chance: Force-match an existing die's value (if any dice exist).
         (b) Else 70% chance: pick from top half of [1..num_sides].
         (c) Else normal roll.
    """
    # If not a bad gambler, roll normally
    if not is_bad_gambler:
        return random.randint(1, num_sides)

    # Otherwise, do "Bad Gambler" logic:

    # (a) 30% chance to force-match an existing die’s value
    #     which boosts chances of forming dubs/trips/quads
    if dice_so_far and random.random() < 0.30:
        _, existing_val = random.choice(dice_so_far)
        return existing_val

    # (b) 70% chance to pick from the top half
    if random.random() < 0.70:
        lower_bound = (num_sides // 2) + 1
        if lower_bound <= num_sides:
            return random.randint(lower_bound, num_sides)
        else:
            # Edge case: if num_sides=1, just roll normally
            return random.randint(1, num_sides)

    # (c) Otherwise normal roll
    return random.randint(1, num_sides)

def print_dice_results(dice):
    """
    Print the dice results, applying color if we have Dubs, Trips, or Quads:

    Priority (highest to lowest):
      - Quads (Z=Y=X=W) -> blue
      - Trips (Z=Y=X)   -> red
      - Dubs  (Z=Y)     -> green

    If we achieve one of these, print the "You achieved ..." message
    in blinking yellow.
    """
    # Initialize a map from label -> color (None = no color)
    color_map = {}
    for (label, _) in dice:
        color_map[label] = None  # default

    # Grab potential values of Z, Y, X, W
    z_val = None
    y_val = None
    x_val = None
    w_val = None

    for (label, value) in dice:
        if label == 'Z':
            z_val = value
        elif label == 'Y':
            y_val = value
        elif label == 'X':
            x_val = value
        elif label == 'W':
            w_val = value

    # Decide which condition we meet (in priority order)
    achieved_msg = None

    # QUADS
    if (z_val is not None and y_val is not None and x_val is not None and w_val is not None
        and z_val == y_val == x_val == w_val):
        achieved_msg = "You got Quads!"
        for lbl in ['Z', 'Y', 'X', 'W']:
            color_map[lbl] = "\033[34m"  # Blue

    # TRIPS
    elif (z_val is not None and y_val is not None and x_val is not None
          and z_val == y_val == x_val):
        achieved_msg = "You got Trips!"
        for lbl in ['Z', 'Y', 'X']:
            color_map[lbl] = "\033[31m"  # Red

    # DUBS
    elif (z_val is not None and y_val is not None
          and z_val == y_val):
        achieved_msg = "You got Dubs!"
        for lbl in ['Z', 'Y']:
            color_map[lbl] = "\033[32m"  # Green

    # Print all dice with assigned colors
    for (label, roll_value) in dice:
        prefix = color_map[label] if color_map[label] else ""
        suffix = "\033[0m" if color_map[label] else ""
        print(f"{prefix}Dice {label}: {roll_value}{suffix}")

    # If we got a special message, print it in BLINKING YELLOW
    # \033[93m = bright yellow, \033[5m = blink
    # Combine them: \033[93;5m
    # Then reset at the end with \033[0m
    if achieved_msg:
        blink_yellow = "\033[93;5m"
        reset = "\033[0m"
        print(f"{blink_yellow}{achieved_msg}{reset}")

def main():
    # Clear the screen at program start
    clear_screen()

    # Ask the user how many dice
    num_dice = int(input("How many dice would you like to roll? "))

    # Ask the user how many sides
    num_sides = int(input("How many sides should each die have? "))

    # Ask if user wants "Bad Gambler" mode
    bg_input = input("Enable 'Bad Gambler' mode? (y/n): ").lower().strip()
    bad_gambler = (bg_input == 'y')

    # Create list of (label, roll_value)
    dice = []

    # Initial roll
    for i in range(num_dice):
        label = chr(ord('Z') - i)  # Label from 'Z' backward
        roll_value = roll_die(num_sides, dice, bad_gambler)
        dice.append((label, roll_value))

    # Print initial results
    print("\nInitial Roll Results:")
    print_dice_results(dice)

    # Allow user to reroll (individual or all)
    while True:
        cmd = input(
            "\nEnter a dice label to reroll it, "
            "type 'all' to reroll all dice, or 'done' to finish: "
        ).upper().strip()

        if cmd == "DONE":
            break
        elif cmd == "ALL":
            # Reroll all dice
            new_dice = []
            for label, _ in dice:
                new_roll = roll_die(num_sides, dice, bad_gambler)
                new_dice.append((label, new_roll))
            dice = new_dice

            print("\nAll dice have been rerolled.")
            print("\nCurrent Dice Results:")
            print_dice_results(dice)

        else:
            # Reroll a single die, if found
            for idx, (label, _) in enumerate(dice):
                if label == cmd:
                    new_roll = roll_die(num_sides, dice, bad_gambler)
                    dice[idx] = (label, new_roll)
                    print(f"\nDice {label} was rerolled. New result: {new_roll}")

                    print("\nCurrent Dice Results:")
                    print_dice_results(dice)
                    break
            else:
                print("No dice found with that label. Please try again.")

    # Print final results
    print("\nFinal Dice Results:")
    print_dice_results(dice)


if __name__ == "__main__":
    main()
