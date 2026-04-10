import redis
import json
from app.config import settings

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)


class RedisPaymentService:
    def state_key(self, payment_id):
        return f"payment:state:{payment_id}"

    def lock_key(self, payment_id):
        return f"payment:lock:{payment_id}"

    # ---------------- STATE ----------------

    def set_payment_state(self, payment_id, state, ttl=300):
        try:
            r.setex(self.state_key(payment_id), ttl, json.dumps(state))
        except Exception:
            pass  # best effort

    def get_payment_state(self, payment_id):
        try:
            data = r.get(self.state_key(payment_id))
            return json.loads(data) if data else None
        except Exception:
            return None

    # ---------------- LOCK ----------------

    def with_lock(self, payment_id, callback):
        lock = r.lock(self.lock_key(payment_id), timeout=30)

        if lock.acquire(blocking=False):
            try:
                callback()
            finally:
                lock.release()
        else:
            # fallback
            callback()
