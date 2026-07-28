let isEditing = false;
let isSubmitting = false;

document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector("#trade-builder-form");

    if(form){

        form.querySelectorAll("input,select").forEach(el=>{

            el.addEventListener("focus",()=>{

                isEditing = true;

            });

            el.addEventListener("blur",()=>{

                setTimeout(()=>{

                    isEditing = false;

                },300);

            });

        });

        form.addEventListener("submit",()=>{

            isSubmitting = true;

        });

    }

});

function refreshDashboard(){

    if(isEditing) return;

    if(isSubmitting) return;

    location.reload();

}

setInterval(refreshDashboard,3000);
