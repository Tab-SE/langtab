from colorama import init, Fore, Style

init(autoreset=True) 

def print_welcome_message():
    ascii_art = """
██╗      █████╗ ███╗   ██╗ ██████╗████████╗ █████╗ ██████╗ 
██║     ██╔══██╗████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██╔══██╗
██║     ███████║██╔██╗ ██║██║  ███╗  ██║   ███████║██████╔╝
██║     ██╔══██║██║╚██╗██║██║   ██║  ██║   ██╔══██║██╔══██╗
███████╗██║  ██║██║ ╚████║╚██████╔╝  ██║   ██║  ██║██████╔╝
╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝╚═════╝ 
                                                           
    """
    print(Fore.GREEN + ascii_art)
    print(Fore.CYAN + "Welcome to LangTab")

def prompt_user_input(prompt_text):
    print(Fore.BLUE + Style.BRIGHT + "User: " + Style.RESET_ALL, end='')
    return input(prompt_text)

def print_agent_response(response_text):
    print(Fore.YELLOW + Style.BRIGHT + "Agent: " + Style.RESET_ALL + response_text)