'use strict';

const header = document.querySelector("[data-header]");
const navToggleBtn = document.querySelector("[data-nav-toggle-btn]");

navToggleBtn.addEventListener("click", function () {
  header.classList.toggle("nav-active");
  this.classList.toggle("active");
});

 
const navbarLinks = document.querySelectorAll("[data-nav-link]");

for (let i = 0; i < navbarLinks.length; i++) {
  navbarLinks[i].addEventListener("click", function () {
    header.classList.toggle("nav-active");
    navToggleBtn.classList.toggle("active");
  });
}

const backTopBtn = document.querySelector("[data-back-to-top]");

window.addEventListener("scroll", function () {
  if (window.scrollY >= 100) {
    header.classList.add("active");
    backTopBtn.classList.add("active");
  } else {
    header.classList.remove("active");
    backTopBtn.classList.remove("active");
  }
  
});

 
const form = document.getElementById('contact-form');
const responseMessage = document.getElementById('response-message');

form.addEventListener('submit', async (event) => {
    event.preventDefault();  

    Swal.fire({
      title : "Envoie en cours ..." , 
      text : "Veillez patienter" , 
      allowOutsideClick : false , 
      didOPen: () => {
        Swal.showLoading() ;
      },
    }) ;
  
    const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        message: document.getElementById('message').value,
    };

    try {
        const response = await fetch('https://portfolio-master-kuci.onrender.com/api/send-mail', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        });

        console.log('response : ' , response)

        const result = await response.json();
        console.log("result : "  ,result)

        if (response.ok) { 
            console.log(result.message)
            Swal.fire({
              icon: "success" ,
              title : "Votre méssage a bien été envoyé" , 
              text : result.message , 
              showConfirmButton : false ,              
            })

            form.reset(); 
        } else {
            console.log("erreur:" , result.error)
            Swal.fire({
              icon: "error",
              title: "Oops...",
              text: result.error , 
              footer: '<a href="#">Why do I have this issue?</a>'
            });
            
        }
    } catch (error) {
        responseMessage.textContent = "Erreur lors de l'envoi du message.";
        responseMessage.style.color = 'red';
        
    }
});



 