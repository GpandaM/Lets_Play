# class CommandLineInterface:
#     def display(self, message: str):
#         print(message)
    
#     def get_input(self) -> str:
#         user_input = input(">> ").strip()
#         return user_input if user_input else None
    

class CommandLineInterface:
    """Enhanced CLI with better input handling"""
    
    def display(self, message: str) -> None:
        """Display a message to the user"""
        if message:
            print(message, end='')
    
    def get_input(self, prompt: str = ">> ") -> str:
        """Get input from user with optional prompt"""
        try:
            return input(prompt).strip()
        except KeyboardInterrupt:
            print("\n\nGame interrupted by user.")
            return "quit"
        except EOFError:
            return "quit"
    
    def clear_screen(self) -> None:
        """Clear the screen (optional)"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')