import re


SIGN_ACTION = {
    "++": lambda a, b: a + b,
    "--": lambda a, b: a - b,
    ">": lambda a, b: a > b,
    "<": lambda a, b: a < b,
    ">=": lambda a, b: a >= b,
    "<=": lambda a, b: a <= b,
    "==": lambda a, b: b,
    "===": lambda a, b: a == b
}


def on_choice_action(user: dict, choice_expression: str):
    if choice_expression == "0":
        return
    choices_list = choice_expression.split("&")
    for choice in choices_list:
        param_name = re.search("[a-z]+", choice).group()
        if param_name in user:
            exp_sign = re.search("[+|=|-]+", choice).group()
            exp_value = re.search("[0-9]+", choice).group()
            user[param_name] = SIGN_ACTION[exp_sign](
                user[param_name], int(exp_value))
        else:
            raise Exception(f"User doesn't have '{param_name}' param")


def check_args(user, choice_expression):
    if choice_expression == "0":
        return True
    choices_list = choice_expression.split("&")
    check_result = []
    for choice in choices_list:
        param_name = re.search("[a-z]+", choice).group()
        if param_name in user:
            exp_sign = re.search("[=|<|>]+", choice).group()
            exp_value = re.search("[0-9]+", choice).group()
            check_result.append(SIGN_ACTION[exp_sign](
                user[param_name], int(exp_value)))
        else:
            raise Exception(f"User doesn't have '{param_name}' param")
    return all(check_result)
