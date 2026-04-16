import { useEffect, useState } from "react";
import { getGateways, getWallet, createPayment } from "./api";
import { useNavigate } from "react-router-dom";

type Gateway = {
  key: string;
  name: string;
  default: boolean;
};

function App() {
  const [gateways, setGateways] = useState<Gateway[]>([]);
  const [selectedGateway, setSelectedGateway] = useState("");
  const [amount, setAmount] = useState(1);
  const [credit, setCredit] = useState<string>("...");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  // load gateways
  useEffect(() => {
    getGateways().then((data) => {
      setGateways(data);
      const def = data.find((g: Gateway) => g.default);
      if (def) setSelectedGateway(def.key);
    });
  }, []);

  // load wallet
  useEffect(() => {
    const load = async () => {
      const data = await getWallet(1);
      const euro = (data.balance / 100).toFixed(2);
      setCredit(euro);
    };

    load();

    const interval = setInterval(load, 5000);

    return () => clearInterval(interval);
  }, []);

  const handlePay = async (e: React.SyntheticEvent) => {
    e.preventDefault();
    setLoading(true);

    const cents = Math.round(amount * 100);

    const res = await createPayment({
      user_id: 1,
      amount: cents,
      gateway: selectedGateway,
      idempotency_key: "web-" + Date.now(),
    });

    navigate(`/payments/${res.id}`);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 dark:bg-slate-900">
      <div className="w-full max-w-md bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-6 space-y-5">

        {/* Title */}
        <h2 className="text-xl font-semibold text-center text-blue-600">
          Python Payflow v1.0
        </h2>

        {/* Credit */}
        <div className="text-center text-sm text-gray-500 dark:text-gray-300">
          Your credit: <span className="font-semibold">€{credit}</span>
        </div>

        {/* Form */}
        <form onSubmit={handlePay} className="space-y-4">

          {/* Gateway */}
          <div>
            <label className="text-sm block mb-1">Gateway</label>
            <select
              className="w-full p-2 rounded-lg border dark:bg-slate-900 dark:text-white dark:border-slate-700 focus:ring-2 focus:ring-blue-500 outline-none"
              value={selectedGateway}
              onChange={(e) => setSelectedGateway(e.target.value)}
            >
              {gateways.map((g) => (
                <option key={g.key} value={g.key}>
                  {g.name}
                </option>
              ))}
            </select>
          </div>

          {/* Amount */}
          <div>
            <label className="text-sm block mb-1">Amount (€)</label>
            <input
              type="number"
              step="0.01"
              className="w-full p-2 rounded-lg border dark:bg-slate-900 dark:text-white dark:border-slate-700 focus:ring-2 focus:ring-blue-500 outline-none"
              value={amount}
              onChange={(e) => setAmount(parseFloat(e.target.value))}
            />
          </div>

          {/* Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {loading && (
              <div className="h-4 w-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            )}
            {loading ? "Processing..." : "Pay"}
          </button>

        </form>
      </div>
    </div>
  );
}

export default App;