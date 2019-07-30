"""
Author      Nicolas Peschke
Date        30.07.2019
"""


def check_input(user_input, possibilities: list, name: str):
    """
    Input checking
    :param user_input: Input by the user
    :param possibilities: List of possibilities
    :param name: Name of the checked parameter
    :return: True if input is valid
    """
    if user_input not in possibilities:
        raise AttributeError(f"Your specified {name} ({user_input}) is not in the list of possible {name}s ({possibilities})!")
    else:
        return True
