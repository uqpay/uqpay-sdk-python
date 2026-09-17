"""Run with mypy --follow-imports=silent --warn-unused-ignores on this file."""
from uqpay.types.issuing import ResetPinParams
from uqpay.types.connect import RfiAnswerItem
from uqpay.types.simulator import SimulateDepositCreationParams

pin: ResetPinParams = {"card_id": "card-1", "pin": "135790", "type": "UPDATE", "old_pin": "024680"}
text: RfiAnswerItem = {"key": "note", "type": "TEXT", "text": "source of funds"}
attachment: RfiAnswerItem = {"key": "document", "type": "ATTACHMENT", "attachments": ["file-1"]}
deposit: SimulateDepositCreationParams = {"account_id": "account-1", "amount": 10, "currency": "SGD", "sender_swift_code": "WELGBE22"}
missing_account: SimulateDepositCreationParams = {"amount": 10, "currency": "SGD", "sender_swift_code": "WELGBE22"}  # type: ignore[typeddict-item]
invalid_action: ResetPinParams = {"card_id": "card-1", "pin": "135790", "type": "INVALID"}  # type: ignore[typeddict-item]
