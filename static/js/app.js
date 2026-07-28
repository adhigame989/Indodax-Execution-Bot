let isEditing = false;

document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector("#trade-builder-form");

    if(form){

        form.querySelectorAll("input,select").forEach(el=>{

            el.addEventListener("focus",()=>{

                isEditing=true;

            });

            el.addEventListener("blur",()=>{

                isEditing=false;

            });

        });

    }

});

function refreshDashboard(){

    if(isEditing){

        return;

    }

    location.reload();

}

setInterval(refreshDashboard,3000);
