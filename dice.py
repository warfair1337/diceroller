import random

def clear_screen():
    """
    Clear the terminal screen using ANSI escape codes.
    """
    print("\033[2J\033[H", end="")

def roll_die(num_sides, dice_so_far, is_bad_gambler):
    """
    Roll a single die with possible 'Bad Gambler' skew:
      - If is_bad_gambler is False: normal roll in [1..num_sides].
      - If is_bad_gambler is True:
         (a) 30% chance: Force-match an existing die's value (if any dice exist).
         (b) Else 70% chance: pick from the top half of [1..num_sides].
         (c) Else normal roll.
    """
    if not is_bad_gambler:
        return random.randint(1, num_sides)

    # "Bad Gambler" logic
    # (a) 30% chance to force-match a random existing die’s value
    if dice_so_far and random.random() < 0.30:
        _, existing_val = random.choice(dice_so_far)
        return existing_val

    # (b) 70% chance to pick from the top half
    if random.random() < 0.70:
        lower_bound = (num_sides // 2) + 1
        if lower_bound <= num_sides:
            return random.randint(lower_bound, num_sides)
        else:
            # Edge case if num_sides=1 or similar
            return random.randint(1, num_sides)

    # (c) Otherwise normal roll
    return random.randint(1, num_sides)

def print_dice_results(dice):
    """
    Print the dice results in alphabetical order (A -> Z).
    Apply color if we have Dubs, Trips, or Quads (checked for Z, Y, X, W).

    Priority: Quads > Trips > Dubs
    - Quads = Z=Y=X=W (blue)
    - Trips = Z=Y=X   (red)
    - Dubs  = Z=Y     (green)

    Achievement message is in blinking yellow (\033[93;5m).
    """
    # Initialize color map: label -> escape code or None
    color_map = {}
    for (label, _) in dice:
        color_map[label] = None

    # Identify values of Z, Y, X, W if they exist
    z_val = y_val = x_val = w_val = None
    for (label, val) in dice:
        if label == 'Z':
            z_val = val
        elif label == 'Y':
            y_val = val
        elif label == 'X':
            x_val = val
        elif label == 'W':
            w_val = val

    # Determine if we have Quads, Trips, or Dubs
    achieved_msg = None

    # QUADS
    if (z_val is not None and y_val is not None and x_val is not None and w_val is not None
        and z_val == y_val == x_val == w_val):
        achieved_msg = "You got Quads!"
        for lbl in ['Z', 'Y', 'X', 'W']:
            color_map[lbl] = "\033[34m"  # blue

    # TRIPS
    elif (z_val is not None and y_val is not None and x_val is not None
          and z_val == y_val == x_val):
        achieved_msg = "You got Trips!"
        for lbl in ['Z', 'Y', 'X']:
            color_map[lbl] = "\033[31m"  # red

    # DUBS
    elif (z_val is not None and y_val is not None
          and z_val == y_val):
        achieved_msg = "You got Dubs!"
        for lbl in ['Z', 'Y']:
            color_map[lbl] = "\033[32m"  # green

    # Sort dice by label (alphabetical order) and print
    # (A -> Z, e.g. A, B, C, ... X, Y, Z)
    for label, roll_value in sorted(dice, key=lambda x: x[0]):
        prefix = color_map[label] if color_map[label] else ""
        suffix = "\033[0m" if color_map[label] else ""
        print(f"{prefix}Dice {label}: {roll_value}{suffix}")

    # If there's an achievement, print in blinking yellow
    if achieved_msg:
        print(f"\033[93;5m{achieved_msg}\033[0m")

def main():
    # Clear the screen at the start
    clear_screen()

    # Ask user inputs
    num_dice = int(input("How many dice would you like to roll? "))
    num_sides = int(input("How many sides should each die have? "))

    # "Bad Gambler"?
    bg_input = input("Enable 'Bad Gambler' mode? (y/n): ").lower().strip()
    bad_gambler = (bg_input == 'y')

    # Create our dice list
    dice = []
    # Label dice from Z backward (Z, Y, X, W, V...) but we can still
    # display them in alphabetical order when printing
    for i in range(num_dice):
        label = chr(ord('Z') - i)
        roll_val = roll_die(num_sides, dice, bad_gambler)
        dice.append((label, roll_val))

    # Print initial results
    print("\nInitial Roll Results:")
    print_dice_results(dice)

    # Reroll loop
    while True:
        cmd = input(
            "\nEnter a dice label to reroll it, "
            "'all' to reroll all dice, or 'done' to finish: "
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
            # Reroll a single die if found
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

    # Final results
    print("\nFinal Dice Results:")
    print_dice_results(dice)

if __name__ == "__main__":
    main()
