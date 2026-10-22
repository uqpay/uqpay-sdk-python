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

from uqpay.types.issuing._create_card_params import CreateCardParamsCardholderRequiredFields
inline_holder: CreateCardParamsCardholderRequiredFields = {"email": "test@example.test", "first_name": "Test", "last_name": "User", "country_code": "SG"}


# The current contract permits Business default holders and supporting-only updates.
from uqpay.types.issuing import CreateCardParams, AssignCardParams, UpdateCardholderParams
from uqpay.types.payment import CapturePaymentIntentParams
business_card: CreateCardParams = {"card_currency": "USD", "card_product_id": "product-1"}
assign_default: AssignCardParams = {"card_number": "synthetic", "card_currency": "USD", "card_mode": "SINGLE"}
supporting_update: UpdateCardholderParams = {"identity": {"proof_of_address": "cGRm", "proof_of_address_issue_date": "2026-10-01", "proof_of_address_issuing_country": "SG", "identity_verification": "a3lj"}}
capture: CapturePaymentIntentParams = {"amount_to_capture": "6.00", "merchant_capture_order_id": "capture-1", "final_capture": True}
numeric_capture: CapturePaymentIntentParams = {"amount_to_capture": 6.0}  # type: ignore[typeddict-item]
non_final_capture: CapturePaymentIntentParams = {"final_capture": False}  # type: ignore[typeddict-item]
card_check: CheckBeneficiaryParams = {"entity_type": "INDIVIDUAL", "payment_method": "CARD", "currency": "USD", "account_number": "synthetic"}
