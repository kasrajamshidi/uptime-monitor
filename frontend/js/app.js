const monitorsContainer =
    document.getElementById("monitors-container");

const totalMonitors =
    document.getElementById("total-monitors");

const upMonitors =
    document.getElementById("up-monitors");

const downMonitors =
    document.getElementById("down-monitors");

const modal =
    document.getElementById("modal");

const monitorForm =
    document.getElementById("monitor-form");

const formError =
    document.getElementById("form-error");


async function loadMonitors() {

    try {

        const monitors = await getMonitors();

        renderMonitors(monitors);

    } catch (error) {

        console.error(error);

        monitorsContainer.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">⚠️</div>

                <h2>Failed to load monitors</h2>

                <p>
                    Could not connect to the API.
                </p>
            </div>
        `;
    }
}


function renderMonitors(monitors) {

    totalMonitors.textContent = monitors.length;

    const up =
        monitors.filter(
            monitor => monitor.status === "up"
        ).length;

    const down =
        monitors.filter(
            monitor => monitor.status === "down"
        ).length;

    upMonitors.textContent = up;
    downMonitors.textContent = down;


    if (monitors.length === 0) {

        monitorsContainer.innerHTML = `
            <div class="empty-state">

                <div class="empty-icon">
                    📡
                </div>

                <h2>No monitors yet</h2>

                <p>
                    Add your first monitor to start
                    tracking uptime.
                </p>

                <button
                    class="primary-button"
                    onclick="openAddMonitor()"
                >
                    + Add Monitor
                </button>

            </div>
        `;

        return;
    }


    monitorsContainer.innerHTML =
        monitors.map(createMonitorCard).join("");
}


function createMonitorCard(monitor) {

    let statusClass = "status-unknown";
    let statusText = "UNKNOWN";

    if (monitor.status === "up") {

        statusClass = "status-up";
        statusText = "UP";

    } else if (monitor.status === "down") {

        statusClass = "status-down";
        statusText = "DOWN";
    }


    return `
        <div
            class="monitor-card"
            onclick="openMonitor('${monitor.id}')"
            style="cursor: pointer;"
        >

            <div class="monitor-info">

                <span
                    class="status-dot ${statusClass}"
                ></span>

                <div>

                    <div class="monitor-name">
                        ${escapeHtml(monitor.name)}
                    </div>

                    <div class="monitor-url">
                        ${escapeHtml(monitor.url)}
                    </div>

                </div>

            </div>


            <div class="monitor-meta">

                <div class="monitor-status">
                    ${statusText}
                </div>

                <div class="monitor-response">
                    ${statusText === "UP"
                        ? "Online"
                        : "—"}
                </div>

                <div class="monitor-interval">
                    Every ${monitor.interval}s
                </div>

            </div>

        </div>
    `;
}


function openAddMonitor() {

    formError.textContent = "";

    monitorForm.reset();

    modal.classList.remove("hidden");
}


function closeAddMonitor() {

    modal.classList.add("hidden");
}


monitorForm.addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();

        formError.textContent = "";


        const name =
            document.getElementById("name").value.trim();

        const url =
            document.getElementById("url").value.trim();

        const interval =
            document.getElementById("interval").value;


        try {

            await createMonitor(
                name,
                url,
                interval
            );

            closeAddMonitor();

            await loadMonitors();

        } catch (error) {

            console.error(error);

            formError.textContent =
                error.message;
        }
    }
);


function openMonitor(monitorId) {

    window.location.href =
        `monitor.html?id=${monitorId}`;
}


function escapeHtml(value) {

    const div = document.createElement("div");

    div.textContent = value;

    return div.innerHTML;
}


loadMonitors();
