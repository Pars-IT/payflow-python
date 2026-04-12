import { render, screen, act } from "@testing-library/react";
import StatusPage from "./StatusPage";
import * as api from "./api";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { vi } from "vitest";

vi.mock("./api");

const mockedApi = vi.mocked(api, true);

test("shows success status", async () => {
    vi.useFakeTimers();

    mockedApi.getPayment.mockResolvedValue({
        status: "success",
    });

    render(
        <MemoryRouter initialEntries={["/payments/1"]}>
            <Routes>
                <Route path="/payments/:id" element={<StatusPage />} />
            </Routes>
        </MemoryRouter>
    );

    // execute interval
    await act(async () => {
        vi.advanceTimersByTime(1500);
    });

    expect(screen.getByText(/Payment successful/i)).toBeInTheDocument();

    vi.useRealTimers();
});