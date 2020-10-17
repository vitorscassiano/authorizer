from authorizer.application.usecases import account_usecase


def build_response(account):
    return dict(account=account.to_json())


def create_account_handler(data: dict, account_usecase=account_usecase):
    active_card = data["account"]["activeCard"]
    available_limit = data["account"]["availableLimit"]
    account = account_usecase.create(active_card, available_limit)

    return build_response(account)
