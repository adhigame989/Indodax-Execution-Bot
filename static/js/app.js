async function loadPartial(id,url){

    try{

        const res=await fetch(url);

        const html=await res.text();

        document.getElementById(id).innerHTML=html;

    }catch(e){

        console.log(e);

    }

}

async function refreshDashboard(){

    await Promise.all([

        loadPartial("summary-card","/partial/summary"),

        loadPartial("position-card","/partial/position"),

        loadPartial("wallet-card","/partial/wallet"),

        loadPartial("config-card","/partial/config")

    ]);

}

refreshDashboard();

setInterval(refreshDashboard,2000);
