from pathlib import Path
import json
from unittest.mock import Mock
import httpx
from uqpay.http import HttpClient
from uqpay.resources.issuing import IssuingResource
from uqpay.resources.payment import PaymentResource
from uqpay.resources.banking import BankingResource
from uqpay.resources.connect import ConnectResource


def test_kyc_boundaries_paging_and_proxy_headers():
    captured = []
    def handler(request):
        captured.append(request)
        return httpx.Response(200, json={})
    token = Mock(account_context={})
    token.get_token.return_value = "offline-token"
    http = HttpClient("https://api-sandbox.example.test", token, "client")
    http._http.close()
    http._http = httpx.Client(transport=httpx.MockTransport(handler))
    try:
        issuing = IssuingResource(http, "https://api-sandbox.example.test")
        for provider in ["SUMSUB", "MYINFO", "JUMIO", "DIDIT", "SHUFTI", "REGTANK"]:
            for length in [9, 10, 64, 65]:
                for dob in ["2009-09-17", "2008-09-17", "1947-09-17", "1946-09-17"]:
                    fields = {"email": "test@example.test", "first_name": "Test", "last_name": "User", "country_code": "SG", "phone_number": "81234567", "date_of_birth": dob, "kyc_verification": {"method": "THIRD_PARTY", "kyc_proof": {"provider": provider, "reference_id": "r" * length}}}
                    issuing.cardholders.create(fields)
                    assert json.loads(captured[-1].content) == fields
                    update = {"date_of_birth": dob, "kyc_verification": fields["kyc_verification"]}
                    issuing.cardholders.update("holder-1", update)
                    assert json.loads(captured[-1].content) == update
                    issuing.cards.create({"cardholder_id": "holder-1", "card_currency": "SGD", "card_product_id": "product-1", "cardholder_required_fields": fields})
                    assert json.loads(captured[-1].content)["cardholder_required_fields"] == fields
        for size in [1, 10, 100]:
            issuing.cards.list({"page_size": size, "page_number": 1})
            assert captured[-1].url.params["page_size"] == str(size)
        payment = PaymentResource(http, "client")
        # D189-D196, with and without per-request delegation.
        routes = [
            ("/v2/payment/balances", lambda o: payment.balances.list({}, o)),
            ("/v2/payment/balances/USD", lambda o: payment.balances.retrieve('USD', o)),
            ("/v2/payment/bankaccount", lambda o: payment.bank_accounts.list({}, o)),
            ("/v2/payment/bankaccount/ba-1", lambda o: payment.bank_accounts.retrieve('ba-1', o)),
            ("/v2/payment/payout", lambda o: payment.payouts.list({}, o)),
            ("/v2/payment/payout/po-1", lambda o: payment.payouts.retrieve('po-1', o)),
            ("/v2/payment/settlements", lambda o: payment.settlements.list({}, o)),
            ("/v2/payment_intents/pi-1", lambda o: payment.payment_intents.retrieve('pi-1', o)),
        ]
        for path, call in routes:
            for account in ["sub-account", ""]:
                call({"on_behalf_of": account} if account else {})
                request = captured[-1]
                assert request.method == "GET" and request.url.path == path
                assert request.headers["x-client-id"] == "client"
                assert request.headers.get("x-on-behalf-of", "") == account
                assert "x-idempotency-key" not in request.headers
        key = "550e8400-e29b-41d4-a716-446655440000"
        payment.payment_intents.create({"amount": "1.00", "currency": "USD"}, {"idempotency_key": key})
        assert captured[-1].headers["x-idempotency-key"] == key
    finally:
        http.close()


def test_response_shapes_are_not_coerced():
    payloads = [
        {"entity_type": "COMPANY", "business_details": {"legal_entity_name": "Example"}},
        {"entity_type": "INDIVIDUAL", "person_details": {"first_name": "Test"}, "representatives": [{"other_documents": None}]},
        {"currency": "USD", "available_balance": "-12345678901234567890.12", "prepaid_balance": "0.00"},
        {"payer": {"payer_id": "0", "identification_type": ""}, "beneficiary": {"address": {"country": "SG", "city": "", "state": ""}}},
        {"metadata": None, "next_action": None, "latest_payment_attempt": None, "complete_time": ""},
        {"card_limit": "12345678901234567890.12345678", "metadata": '{"ref":"0001"}', "risk_controls": None},
    ]
    token = Mock(account_context={})
    token.get_token.return_value = "offline"
    current = {}
    http = HttpClient("https://api-sandbox.example.test", token, "client")
    http._http.close()
    requests = []
    def respond(request):
        requests.append(request)
        return httpx.Response(200, json=current)
    http._http = httpx.Client(transport=httpx.MockTransport(respond))
    try:
        operations = [
            lambda: ConnectResource(http).accounts.retrieve("account-1"),
            lambda: ConnectResource(http).accounts.retrieve("account-1"),
            lambda: BankingResource(http).balances.retrieve("USD"),
            lambda: BankingResource(http).payouts.retrieve("payout-1"),
            lambda: PaymentResource(http, "client").payment_intents.retrieve("pi-1"),
            lambda: IssuingResource(http, "https://api-sandbox.example.test").cards.retrieve("card-1"),
        ]
        for current, call in zip(payloads, operations):
            assert call() == current
        # Frozen account summaries/details and issuing money: all fixture fields.
        account = ConnectResource(http).accounts
        issuing = IssuingResource(http, 'https://api-sandbox.example.test')
        calls = {
            'accounts.list': lambda: account.list({'page_size': 10, 'page_number': 1}),
            'accounts.get': lambda: account.retrieve('account-1'),
            'transactions.get': lambda: issuing.transactions.retrieve('tx-1'),
            'transactions.list': lambda: issuing.transactions.list({'page_size': 10, 'page_number': 1}),
            'transfers.get': lambda: issuing.transfers.retrieve('transfer-1'),
        }
        for fixture in json.loads((Path(__file__).parent / 'fixtures/account-money.json').read_text()):
            current = fixture['body']
            assert calls[fixture['operation']]() == current
            assert requests[-1].method == 'GET' and requests[-1].url.path == fixture['path']
        calls = {
            'cards.list': lambda: issuing.cards.list({'page_size': 10, 'page_number': 1}),
            'cards.get': lambda: issuing.cards.retrieve('card-1'),
            'cardholders.list': lambda: issuing.cardholders.list({'page_size': 10, 'page_number': 1}),
            'cardholders.get': lambda: issuing.cardholders.retrieve('holder-1'),
            'products.list': lambda: issuing.products.list({'page_size': 10, 'page_number': 1}),
            'cards.status': lambda: issuing.cards.update_status('card-1', {'card_status': 'FROZEN'}),
        }
        for fixture in json.loads((Path(__file__).parent / 'fixtures/issuing-responses.json').read_text()):
            current = fixture['body']
            assert calls[fixture['operation']]() == current, (fixture['operation'], fixture['name'])
            assert requests[-1].url.path == fixture['path']
            assert requests[-1].method == ('POST' if fixture['operation'] == 'cards.status' else 'GET')
        for fixture in json.loads((Path(__file__).parent / 'fixtures/deposit-contract.json').read_text()):
            current = fixture['body']
            assert BankingResource(http).deposits.retrieve('deposit-1') == current, fixture['name']
            assert requests[-1].method == 'GET' and requests[-1].url.path == '/v1/deposit/deposit-1'
        beneficiaries = BankingResource(http).beneficiaries
        for fixture in json.loads((Path(__file__).parent / 'fixtures/beneficiary-contract.json').read_text()):
            current = fixture['body']
            calls = {'check': lambda: beneficiaries.check(fixture['request']),
                     'list': lambda: beneficiaries.list({'page_size': 10, 'page_number': 1}),
                     'get': lambda: beneficiaries.retrieve('beneficiary-1')}
            assert calls[fixture['operation']]() == current, fixture['name']
            assert requests[-1].url.path == fixture['path']
            assert requests[-1].method == ('POST' if fixture['operation'] == 'check' else 'GET')
            if fixture['operation'] == 'check':
                assert json.loads(requests[-1].content) == fixture['request']
        # D044/D094: detail-only status; missing detail is legacy robustness.
        transactions = IssuingResource(http, 'https://api-sandbox.example.test').transactions
        for status in ['UNKNOWN', 'UNSETTLED', 'SETTLED', 'NOT_APPLICABLE', None]:
            current = {'transaction_id': 'tx-1'}
            if status is not None:
                current['settlement_status'] = status
            assert transactions.retrieve('tx-1') == current
            assert requests[-1].method == 'GET' and requests[-1].url.path == '/v1/issuing/transactions/tx-1'
        current = {'data': [{'transaction_id': 'tx-1'}], 'total_pages': 1, 'total_items': 1}
        assert transactions.list({'page_size': 10, 'page_number': 1}) == current
        assert requests[-1].method == 'GET' and requests[-1].url.path == '/v1/issuing/transactions'
        # RFI list/detail and PIN order responses through the real HTTP client.
        fixtures = json.loads((Path(__file__).parent / 'fixtures/rfi-orders.json').read_text())
        rfis = ConnectResource(http).rfis
        for rfi in fixtures['rfis']:
            current = rfi
            assert rfis.retrieve(rfi['rfi_id']) == rfi
            assert requests[-1].method == 'GET'
            assert requests[-1].url.path == '/v1/rfis/' + rfi['rfi_id']
            current = {'data': [rfi], 'total_pages': 3, 'total_items': 21}
            assert rfis.list({'page_size': 10, 'page_number': 2, 'status': 'ACTION_REQUIRED'}) == current
            assert requests[-1].method == 'GET' and requests[-1].url.path == '/v1/rfis'
            assert dict(requests[-1].url.params) == {'page_size': '10', 'page_number': '2', 'status': 'ACTION_REQUIRED'}
        for current in fixtures['orders']:
            assert IssuingResource(http, 'https://api-sandbox.example.test').cards.retrieve_order(current['card_order_id']) == current
            assert requests[-1].method == 'GET'
            assert requests[-1].url.path == '/v1/issuing/cards/' + current['card_order_id'] + '/order'
        # AQ-RESPONSE: each operation preserves absent/null/empty values.
        payment = PaymentResource(http, "client")
        rest_cases = [
            (lambda: payment.attempts.retrieve("pa-1"), [{}, {"complete_time":"", "advice_code":"", "authentication_data":{"cvv_result":""}}, {"complete_time":"2026-09-17T00:00:00Z", "advice_code":"01", "authentication_data":{"cvv_result":"M"}}]),
            (lambda: payment.refunds.retrieve("re-1"), [{}, {"metadata":None}, {"metadata":{}}, {"metadata":{"ref":"0001"}}]),
            (lambda: payment.payouts.retrieve("po-1"), [{}, {"completed_time":""}, {"completed_time":"2026-09-17T00:00:00Z"}]),
            (lambda: payment.payment_intents.retrieve("pi-1"), [{}, {"metadata":None,"next_action":None,"latest_payment_attempt":None}, {"metadata":{"ref":"0001"},"next_action":{"redirect_to_url":{"return_url":""}},"latest_payment_attempt":{"advice_code":""}}]),
        ]
        for call, fixtures in rest_cases:
            for current in fixtures:
                assert call() == current
        # D122-D129: every field gets each distinct value, through both routes.
        fields = ["available_balance", "frozen_balance", "margin_balance", "prepaid_balance"]
        amounts = ["0.00", "1.23", "-0.01", "12345678901234567890.12", "-12345678901234567890.12", "0.12345678901234567890"]
        banking = BankingResource(http)
        for i in range(len(amounts)):
            balance = {"currency": "USD", **{field: amounts[(i+j) % len(amounts)] for j, field in enumerate(fields)}}
            current = balance
            assert banking.balances.retrieve("USD") == balance
            assert requests[-1].method == "GET" and requests[-1].url.path == "/v1/balances/USD"
            current = {"data": [balance], "total_pages": 1, "total_items": 1}
            assert banking.balances.list({"page_size": 10, "page_number": 1}) == current
            assert requests[-1].method == "GET" and requests[-1].url.path == "/v1/balances"
            assert requests[-1].url.params["page_size"] == "10"

    finally:
        http.close()
