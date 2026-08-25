const API_BASE_URL = "/api";

async function getMonitors() {
    const response = await fetch(`${API_BASE_URL}/monitors`);

    if (!response.ok) {
        throw new Error("Failed to fetch monitors");
    }

    return await response.json();
}


async function createMonitor(name, url, interval) {
    const response = await fetch(`${API_BASE_URL}/monitors`, {
        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            name,
            url,
            interval: Number(interval)
        })
    });

    if (!response.ok) {
        const error = await response.json();

        throw new Error(
            error.detail || "Failed to create monitor"
        );
    }

    return await response.json();
}


async function getMonitorHistory(monitorId) {
    const response = await fetch(
        `${API_BASE_URL}/monitors/${monitorId}/history`
    );

    if (!response.ok) {
        throw new Error("Failed to fetch monitor history");
    }

    return await response.json();
}
