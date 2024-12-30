import tkinter as tk
from tkinter import messagebox, ttk
import random

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


def analyze_dice_for_color_map(dice):
    """
    Given the dice list (label, value), determine if we have Quads, Trips, or Dubs
    and return a color_map: label -> color-string or "" if no color.
    Also returns any achievement message (e.g. "You got Dubs!").
    """
    color_map = {label: "" for (label, _) in dice}

    # Identify values for special labels
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

    achieved_msg = None

    # QUADS
    if (z_val is not None and y_val is not None and x_val is not None and w_val is not None
        and z_val == y_val == x_val == w_val):
        achieved_msg = "You got Quads!"
        for lbl in ['Z', 'Y', 'X', 'W']:
            color_map[lbl] = "blue"

    # TRIPS
    elif (z_val is not None and y_val is not None and x_val is not None
          and z_val == y_val == x_val):
        achieved_msg = "You got Trips!"
        for lbl in ['Z', 'Y', 'X']:
            color_map[lbl] = "red"

    # DUBS
    elif (z_val is not None and y_val is not None
          and z_val == y_val):
        achieved_msg = "You got Dubs!"
        for lbl in ['Z', 'Y']:
            color_map[lbl] = "green"

    return color_map, achieved_msg


class DiceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dice Roller GUI")

        # Data-related fields
        self.dice = []  # list of (label, value)
        self.num_dice = tk.IntVar(value=4)
        self.num_sides = tk.IntVar(value=6)
        self.is_bad_gambler = tk.BooleanVar(value=False)

        # ------------- GUI Layout -------------
        # Top Frame for user inputs
        input_frame = tk.LabelFrame(root, text="Setup")
        input_frame.pack(fill="x", padx=5, pady=5)

        tk.Label(input_frame, text="Number of Dice:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(input_frame, textvariable=self.num_dice, width=5).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Sides per Die:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(input_frame, textvariable=self.num_sides, width=5).grid(row=1, column=1, padx=5, pady=5)

        tk.Checkbutton(input_frame, text="Enable 'Bad Gambler' mode?", variable=self.is_bad_gambler)\
            .grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Buttons to roll and to finish
        self.roll_button = tk.Button(input_frame, text="Roll Dice", command=self.roll_initial_dice)
        self.roll_button.grid(row=0, column=2, rowspan=2, padx=10, pady=5, sticky="ns")

        self.done_button = tk.Button(input_frame, text="Finish", command=self.finish)
        self.done_button.grid(row=2, column=2, padx=10, pady=5, sticky="e")

        # Middle Frame to display dice results
        results_frame = tk.LabelFrame(root, text="Dice Results")
        results_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.results_container = tk.Frame(results_frame)
        self.results_container.pack(fill="both", expand=True, padx=5, pady=5)

        # Re-roll controls
        reroll_frame = tk.LabelFrame(root, text="Re-roll Controls")
        reroll_frame.pack(fill="x", padx=5, pady=5)

        tk.Label(reroll_frame, text="Select Dice Label:").grid(row=0, column=0, padx=5, pady=5)
        self.selected_label = tk.StringVar(value="")
        self.label_dropdown = ttk.Combobox(reroll_frame, textvariable=self.selected_label, values=[], width=5)
        self.label_dropdown.grid(row=0, column=1, padx=5, pady=5)

        self.reroll_one_button = tk.Button(reroll_frame, text="Reroll Selected", command=self.reroll_one)
        self.reroll_one_button.grid(row=0, column=2, padx=5, pady=5)

        self.reroll_all_button = tk.Button(reroll_frame, text="Reroll All", command=self.reroll_all)
        self.reroll_all_button.grid(row=0, column=3, padx=5, pady=5)

        # A label to display achievements (Dubs, Trips, Quads)
        self.achievement_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
        self.achievement_label.pack(pady=5)

    def roll_initial_dice(self):
        """
        Creates the dice list, labeling from Z downward, 
        and displays initial results in the results container.
        """
        # Validate user input
        nd = self.num_dice.get()
        ns = self.num_sides.get()
        if nd < 1 or ns < 1:
            messagebox.showwarning("Invalid Input", "Number of dice and sides must both be >= 1.")
            return

        # Clear current dice
        self.dice = []
        # Create dice labeled from Z backward
        for i in range(nd):
            label = chr(ord('Z') - i)
            roll_val = roll_die(ns, self.dice, self.is_bad_gambler.get())
            self.dice.append((label, roll_val))

        self.update_dice_display()

    def update_dice_display(self):
        """
        Clear and rebuild the dice display in alphabetical order.
        Also update the label dropdown and detect Dubs/Trips/Quads for coloring.
        """
        # Clear old widgets in results container
        for w in self.results_container.winfo_children():
            w.destroy()

        # Sort dice by label (alphabetically)
        sorted_dice = sorted(self.dice, key=lambda x: x[0])

        # Determine color mapping (for quads, trips, dubs)
        color_map, achieved_msg = analyze_dice_for_color_map(sorted_dice)

        row_count = 0
        for label, roll_value in sorted_dice:
            fg_color = color_map[label]  # e.g. "blue", "red", "green" or ""
            display_text = f"Dice {label}: {roll_value}"
            lbl = tk.Label(self.results_container, text=display_text, font=("Arial", 12))
            if fg_color:
                lbl.configure(fg=fg_color)
            else:
                lbl.configure(fg="black")

            lbl.grid(row=row_count, column=0, sticky="w", pady=2)
            row_count += 1

        # Update combo box with current labels
        all_labels = [d[0] for d in sorted_dice]
        self.label_dropdown.configure(values=all_labels)

        # Update achievement label
        if achieved_msg:
            self.achievement_label.config(text=achieved_msg, fg="gold")
        else:
            self.achievement_label.config(text="", fg="black")

    def reroll_all(self):
        """
        Reroll all dice in the current dice list.
        """
        if not self.dice:
            return
        new_dice = []
        ns = self.num_sides.get()
        for label, _ in self.dice:
            new_roll = roll_die(ns, self.dice, self.is_bad_gambler.get())
            new_dice.append((label, new_roll))
        self.dice = new_dice
        self.update_dice_display()

    def reroll_one(self):
        """
        Reroll a single die given by the selected_label in the dropdown.
        """
        if not self.dice:
            return

        target_label = self.selected_label.get()
        if not target_label:
            return

        ns = self.num_sides.get()
        for idx, (label, _) in enumerate(self.dice):
            if label == target_label:
                new_roll = roll_die(ns, self.dice, self.is_bad_gambler.get())
                self.dice[idx] = (label, new_roll)
                break

        self.update_dice_display()

    def finish(self):
        """
        Show a final message or do final actions before closing.
        """
        if not self.dice:
            messagebox.showinfo("Dice Roller", "No dice to finalize.")
        else:
            # Just display a final message with dice
            sorted_dice = sorted(self.dice, key=lambda x: x[0])
            final_results = "\n".join([f"{label} -> {val}" for (label, val) in sorted_dice])
            messagebox.showinfo("Final Dice Results", final_results)

        # Optionally, close the application
        self.root.quit()


def main():
    root = tk.Tk()
    app = DiceApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

