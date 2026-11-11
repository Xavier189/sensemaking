def charge_with_retry(gateway, order_id, amount, max_attempts=1):
    last_error = None
    for _ in range(max_attempts):
        try:
            return gateway.charge({"order_id": order_id, "amount": amount})
        except TimeoutError as exc:
            last_error = exc
    raise last_error
