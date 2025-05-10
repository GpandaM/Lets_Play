class CommandLineInterface:
    @staticmethod
    def display(message: str):
        print(message)
    
    @staticmethod
    def get_input(prompt: str = "") -> str:
        return input(prompt)