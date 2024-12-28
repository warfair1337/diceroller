import random

def main():
    # Ask the user how many dice
    num_dice = int(input("How many dice would you like to roll? "))
    
    # Ask the user how many sides each die should have
    num_sides = int(input("How many sides should each die have? "))
    
    # Roll each die and display the result with labels from 'Z' backward to 'A'
    for i in range(num_dice):
        # Calculate the label by moving backward from 'Z'
        label = chr(ord('Z') - i)
        
        # Roll the die
        roll_result = random.randint(1, num_sides)
        
        # Print the result
        print(f"{label}: {roll_result}")

if __name__ == "__main__":
    main()
