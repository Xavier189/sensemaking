# Fictional payment client notes

`retry.py` already attaches an idempotency key to every outbound charge request and waits with exponential backoff between retries.
To tolerate transient network timeouts, callers only need to increase `max_attempts`.
