from sqlalchemy import or_, and_
from loguru import logger

from app.core.db_model import TransactionHistory

# def get_transaction_history_by_email(email, db_session):
#     session_transaction_history = db_session.query(TransactionHistory).filter(TransactionHistory.email==email)
#     result_transaction_history = []
#     for i in session_transaction_history:
#         x = transaction_history_base_model(**i.__dict__)
#         result_transaction_history.append(x)

#     return session_transaction_history, result_transaction_history


def fill_create_transaction_history(today, payload):
    
    item_transaction_history = TransactionHistory(
        transaction_history_uuid = payload["transaction_history_uuid"],
        create_date = today,
        profile_name_uuid = payload["profile_name_uuid"],
        transaction_name = payload["transaction_name"],
        transaction_detail = payload["transaction_detail"],
        transaction_return = payload["transaction_return"]
    )

    return item_transaction_history