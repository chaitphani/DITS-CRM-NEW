class TemplateTypes(object):
    USER_SIGNUP = 1
    AGENT_SIGNUP = 2
    USER_CHANGE_PASSWORD = 3
    # USER_OPEN_LIVE_ACCOUNT = 4
    # USER_OPEN_DEMO_ACCOUNT = 5
    # USER_DEPOSIT_AMOUNT = 6
    # USER_WITHDRAW_AMOUNT = 7
    # USER_VERIFY = 8


    CHOICES = (
        # (USER_VERIFY, "User Verify"),
        (USER_SIGNUP, "User Signup"),
        (AGENT_SIGNUP, "Agent Signup"),
        (USER_CHANGE_PASSWORD, "User change password")
        # (USER_OPEN_LIVE_ACCOUNT, "User Open Live Account")
        # (USER_OPEN_DEMO_ACCOUNT, "User Open Demo Account")
        # (USER_DEPOSIT_AMOUNT, "User Deposit Amount")
        # (USER_WITHDRAW_AMOUNT, "User Withdraw Amount")




    )
