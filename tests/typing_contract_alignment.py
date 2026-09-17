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

from uqpay.types.banking import CheckBeneficiaryParams
iban_check: CheckBeneficiaryParams = {"entity_type": "COMPANY", "payment_method": "LOCAL", "currency": "EUR", "iban": "DE89370400440532013000"}
country_check: CheckBeneficiaryParams = {"entity_type": "COMPANY", "payment_method": "LOCAL", "currency": "CNH", "account_number": "12345", "bank_country_code": "CN", "clearing_system": "LOCAL"}

from uqpay.types.issuing import UpdateCardParams
art_update: UpdateCardParams = {"card_art_id": "art-1", "name_on_card": "Test"}
