from pynput import keyboard, mouse  # Import pynput for handling keyboard and mouse input
import time                         # Import time to handle delays and timestamps
import os                           # Import os for interacting with the operating system (file operations)

# File names for storing high scores
KEYBOARD_HIGH_SCORE_FILE = "keyboard_high_score.txt"  # File to store the highest score for keyboard input
MOUSE_HIGH_SCORE_FILE = "mouse_high_score.txt"        # File to store the highest score for mouse clicks

# Base class for handling input events
class InputHandler:
    def __init__(self):
        self.data = []          # List to store input event data
        self.start_time = None  # Variable to record the start time of input

    def save_to_file(self, filename, additional_info=""):
        """Save the collected data to a file with optional additional information."""
        try:
            with open(filename, 'w') as file:
                if additional_info:
                    file.write(f"{additional_info}\n")  # Write additional information if provided
                for entry in self.data:
                    file.write(f"{entry}\n")            # Write each data entry to the file
            print(f"Data saved to {filename}")          # Notify user that data has been successfully saved
        except Exception as e:
            print(f"Error saving file: {e}")            # Print an error message if there is an issue saving the file

    def start_input(self):
        """Start the input collection process."""
        self.start_time = time.time()                   # Record the current time as the start time

    def stop_input(self):
        """Stop the input collection process and calculate the elapsed time."""
        elapsed_time = time.time() - self.start_time    # Calculate the total time taken for input
        return elapsed_time                             # Return the elapsed time

# Subclass for handling keyboard input events
class KeyboardListener(InputHandler):
    def __init__(self):
        super().__init__()                                          # Initialize the base class
        self.input_detected = False                                 # Flag to indicate if input has been detected
        self.listener = keyboard.Listener(on_press=self.on_press)   # Create a keyboard listener with a callback function

    def on_press(self, key):
        """Callback function to handle key press events."""
        if not self.input_detected:
            self.input_detected = True                          # Set flag to true on the first key press
            try:
                self.data.append(f"Key {key.char} pressed")     # Log the key press (for regular keys)
            except AttributeError:
                self.data.append(f"Special key {key} pressed")  # Log special key presses (e.g., shift, ctrl)
            self.listener.stop()                                # Stop listening for input once detected

    def start_input(self):
        """Start listening to keyboard events."""
        super().start_input()           # Call base class method to start input collection
        self.listener.start()           # Start the keyboard listener to begin capturing input

    def stop_input(self):
        """Stop listening to keyboard events and return the elapsed time."""
        self.listener.join()            # Wait for the listener to stop
        return super().stop_input()     # Call base class method to stop input collection and get elapsed time

# Subclass for handling mouse click events
class MouseListener(InputHandler):
    def __init__(self):
        super().__init__()              # Initialize the base class
        self.input_detected = False     # Flag to indicate if input has been detected
        self.listener = mouse.Listener(on_click=self.on_click)  # Create a mouse listener with a callback function

    def on_click(self, x, y, button, pressed):
        """Callback function to handle mouse click events."""
        if pressed and not self.input_detected:
            self.input_detected = True          # Set flag to true on the first mouse click
            self.data.append(f"Mouse clicked at ({x}, {y}) with {button}")  # Log the mouse click position and button
            self.listener.stop()                # Stop listening for input once detected

    def start_input(self):
        """Start listening to mouse events."""
        super().start_input()                   # Call base class method to start input collection
        self.listener.start()                   # Start the mouse listener to begin capturing input

    def stop_input(self):
        """Stop listening to mouse events and return the elapsed time."""
        self.listener.join()                    # Wait for the listener to stop
        return super().stop_input()             # Call base class method to stop input collection and get elapsed time

def countdown(seconds):
    """Display a countdown to the user before starting the input collection."""
    print("Get ready...")               # Notify user that the countdown is starting
    for i in range(seconds, 0, -1):
        print(f"{i}...")                # Print the countdown number
        time.sleep(1)                   # Wait for 1 second before the next countdown number
    print("Go!")                        # Notify user that the input collection is starting

def read_high_score(filename):
    """Read the high score from the specified file."""
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return float(file.read().strip())   # Read and return the high score from the file
    return float('inf')                         # Return a default high score of infinity if the file does not exist

def write_high_score(filename, score):
    """Write the new high score to the specified file."""
    with open(filename, 'w') as file:
        file.write(f"{score:.2f}")              # Write the new high score to the file

def main():
    """Main function to control the program flow and user interaction."""
    print("Welcome to Benchmarker!")  # Greet the user
    print("Disclaimer: Due to the polling loop method, there may be slight inaccuracies in timing.")  # Notify about potential timing inaccuracies
    
    print("1. Start Keyboard Input")            # Option to start keyboard input benchmark
    print("2. Start Mouse Click Benchmark")     # Option to start mouse click benchmark
    print("3. Exit")                            # Option to exit the program

    choice = input("Enter your choice: ")       # Get user choice from input

    if choice == '1':
        countdown(5)                            # Countdown for 5 seconds before starting keyboard input
        kb_listener = KeyboardListener()        # Create an instance of KeyboardListener
        kb_listener.start_input()               # Start listening for keyboard input

        # Polling loop to detect input
        while not kb_listener.input_detected:
            time.sleep(0.01)                    # Short sleep to avoid busy-waiting

        elapsed_time = kb_listener.stop_input()                             # Stop input collection and get elapsed time
        kb_listener.save_to_file("keyboard_input.txt", f"Keyboard input time: {elapsed_time:.2f} seconds")  # Save input data to file
        print(f"Time taken for keyboard input: {elapsed_time:.2f} seconds") # Display elapsed time to user
        
        high_score = read_high_score(KEYBOARD_HIGH_SCORE_FILE)          # Read the current high score
        if elapsed_time < high_score:
            print("New high score!")                                    # Notify user of a new high score
            write_high_score(KEYBOARD_HIGH_SCORE_FILE, elapsed_time)    # Update the high score file
        else:
            print(f"High score remains: {high_score:.2f} seconds")      # Notify user of the existing high score
        
    elif choice == '2':
        countdown(5)                                                # Countdown for 5 seconds before starting mouse click benchmark
        mouse_listener = MouseListener()                            # Create an instance of MouseListener
        mouse_listener.start_input()                                # Start listening for mouse clicks

        # Polling loop to detect input
        while not mouse_listener.input_detected:
            time.sleep(0.01)                                                # Short sleep to avoid busy-waiting

        elapsed_time = mouse_listener.stop_input()                          # Stop input collection and get elapsed time
        mouse_listener.save_to_file("mouse_clicks.txt", f"Mouse click time: {elapsed_time:.2f} seconds")  # Save input data to file
        print(f"Time taken for mouse clicks: {elapsed_time:.2f} seconds")  # Display elapsed time to user

        high_score = read_high_score(MOUSE_HIGH_SCORE_FILE)             # Read the current high score
        if elapsed_time < high_score:
            print("New high score!")                                    # Notify user of a new high score
            write_high_score(MOUSE_HIGH_SCORE_FILE, elapsed_time)       # Update the high score file
        else:
            print(f"High score remains: {high_score:.2f} seconds")      # Notify user of the existing high score

    elif choice == '3':
        print("Exiting program")                                        # Notify user that the program is exiting
    else:
        print("Invalid choice")                                         # Notify user of invalid choice

if __name__ == "__main__":
    main()                                                              # Run the main function if this script is executed
