from authorizer.application.usecases import transaction_manager


def build_response(account):
    return dict(account=account.to_json())


def transaction_handler(data, transaction_manager=transaction_manager):
    transaction = data["transaction"]
    account = transaction_manager.process(transaction)

    return build_response(account)
