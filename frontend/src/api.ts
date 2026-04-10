const API_BASE = import.meta.env.VITE_API_BASE_URL;

export async function getHealth() {
    const res = await fetch(`${API_BASE}/api/health`);
    return res.json();
}

export async function getGateways() {
    const res = await fetch(`${API_BASE}/api/gateways`);
    return res.json();
}

export async function getWallet(userId: number) {
    const res = await fetch(`${API_BASE}/api/wallets/${userId}`);
    return res.json();
}

export async function createPayment(data: {
    user_id: number;
    amount: number;
    gateway: string;
    idempotency_key: string;
}) {
    const body = new URLSearchParams();
    body.append("user_id", data.user_id.toString());
    body.append("amount", data.amount.toString());
    body.append("gateway", data.gateway);
    body.append("idempotency_key", data.idempotency_key);

    const res = await fetch(`${API_BASE}/api/payments`, {
        method: "POST",
        body,
    });

    return res.json();
}

export async function getPayment(paymentId: string) {
    const res = await fetch(`${API_BASE}/api/payments/${paymentId}`);
    return res.json();
}