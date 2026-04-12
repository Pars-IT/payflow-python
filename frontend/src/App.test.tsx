// src/App.test.tsx

import { render, screen } from "@testing-library/react";
import App from "./App";
import { BrowserRouter } from "react-router-dom";
import * as api from "./api";
import { vi } from "vitest";

vi.mock("./api");

const mockedApi = vi.mocked(api, true);

test("loads gateways and selects default", async () => {
    mockedApi.getGateways.mockResolvedValue([
        { key: "ideal", name: "iDEAL", default: true },
    ]);

    mockedApi.getWallet.mockResolvedValue({ balance: 1000 });

    render(
        <BrowserRouter>
            <App />
        </BrowserRouter>
    );

    expect(await screen.findByText("iDEAL")).toBeInTheDocument();
});