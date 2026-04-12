import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getPayment } from "./api";

function StatusPage() {
    const { id } = useParams();
    const [status, setStatus] = useState("Loading...");
    const [type, setType] = useState<"pending" | "success" | "failed">("pending");
    const [failureReason, setFailureReason] = useState("");

    useEffect(() => {
        if (!id) return;

        const interval = setInterval(async () => {
            const payment = await getPayment(id);

            if (payment.checkout_url && payment.status === "pending") {
                setStatus("Redirecting to bank...");
                setType("pending");
                clearInterval(interval);
                window.location.href = payment.checkout_url;
                return;
            }

            if (payment.status === "pending") {
                setStatus("Processing payment...");
                setType("pending");
                return;
            }

            clearInterval(interval);

            if (payment.status === "success") {
                setStatus("Payment successful");
                setType("success");
            } else {
                setStatus("Payment failed");
                setType("failed");
                if (payment.failure_reason) {
                    setFailureReason(payment.failure_reason);
                }
            }
        }, 1500);

        return () => clearInterval(interval);
    }, [id]);

    const color =
        type === "success"
            ? "text-green-500"
            : type === "failed"
                ? "text-red-500"
                : "text-yellow-500";

    const bg =
        type === "success"
            ? "bg-green-100 dark:bg-green-900/30"
            : type === "failed"
                ? "bg-red-100 dark:bg-red-900/30"
                : "bg-yellow-100 dark:bg-yellow-900/30";

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100 dark:bg-slate-900">
            <div className="w-full max-w-md bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-6 space-y-6 text-center">

                {/* Title */}
                <h2 className="text-xl font-semibold text-blue-600">
                    Payment Status
                </h2>

                {/* Status Box */}
                <div className={`p-4 rounded-xl ${bg}`}>
                    <p className={`text-lg font-semibold ${color}`}>
                        {status}
                    </p>
                </div>

                {type === "failed" && failureReason && (
                    <p className="text-sm text-red-400 mt-2">
                        Reason: {failureReason}
                    </p>
                )}

                {/* Spinner */}
                {type === "pending" && (
                    <div className="flex justify-center">
                        <div className="h-8 w-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                    </div>
                )}


                {/* Button */}
                <a
                    href="/"
                    className="block w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition"
                >
                    New Payment
                </a>

            </div>
        </div>
    );
}

export default StatusPage;