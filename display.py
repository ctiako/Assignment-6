# CS305 Park University
# Assignment #6 
# By Cyrille Tekam Tiako
# 15 Sep 2024

# display.py - A simple way to trace the intermediate steps of algorithms.
# AIFCA Python3 code Version 0.9.4 Documentation at http://aipython.org
# Download the zip file and read aipython.pdf for documentation

# Artificial Intelligence: Foundations of Computational Agents http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017-2022.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

class Displayable:
    """
    A class for controlled display of algorithm messages based on verbosity levels.
    The `max_display_level` attribute controls the detail of output.
    """

    max_display_level = 1  # Default display level, can be changed in subclasses

    def display(self, level, *args, **kwargs):
        """
        Prints messages if the specified `level` is less than or equal to `max_display_level`.
        
        Parameters:
        - level: An integer specifying the importance or verbosity level of the message.
        - *args: Positional arguments to be passed to the print function.
        - **kwargs: Keyword arguments passed to the print function.
        """
        if level <= self.max_display_level:
            print(*args, **kwargs)  # Python 3 print statement


def visualize(func):
    """
    A decorator for adding interactive visualization (if required).
    Currently, it just returns the function as-is. 
    
    Placeholder for possible future visualization logic.
    """
    return func


# Example subclass demonstrating how to use the Displayable class
class ExampleAlgorithm(Displayable):
    """
    An example class showing how the `Displayable` class can be used in an algorithm.
    """

    max_display_level = 2  # Set verbosity level for this example

    def step1(self):
        self.display(1, "Step 1: Initializing the algorithm.")
        # Code for step 1...

    def step2(self):
        self.display(2, "Step 2: Executing detailed computations.")
        # Code for step 2...

    def step3(self):
        self.display(3, "Step 3: This message appears only if max_display_level >= 3.")
        # Code for step 3...

    @visualize  # Decorator applied to the main execution
    def run(self):
        """
        Runs the algorithm, displaying steps based on verbosity level.
        """
        self.step1()
        self.step2()
        self.step3()


# Usage example:
if __name__ == "__main__":
    algorithm = ExampleAlgorithm()
    algorithm.run()


