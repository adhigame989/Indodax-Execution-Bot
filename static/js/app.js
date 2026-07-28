async function updateDashboard() {

    try {

        const res = await fetch("/api/status");

        if (!res.ok) return;

        console.log(await res.json());

    } catch (e) {

        console.log(e);

    }

}

updateDashboard();

setInterval(() => {

    location.reload();

}, 3000);
