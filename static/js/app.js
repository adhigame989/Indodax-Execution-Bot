async function updateDashboard(){

    try{

        const res = await fetch("/api/status");

        const data = await res.json();

        console.log(data);

    }catch(e){

        console.log(e);

    }

}

updateDashboard();

setInterval(updateDashboard,2000);
