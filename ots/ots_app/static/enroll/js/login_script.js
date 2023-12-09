// Example starter JavaScript for disabling form submissions if there are invalid fields

(() => {
    'use strict'
  
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation')
   
    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
      form.addEventListener('submit', event => {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }
       
        try{
          // user define
          let UserName=document.getElementById('usernameInputName').value
          let Password=document.getElementById('passwordInputPassword').value
          let Name=document.getElementById('nameInputName').value
          let Email=document.getElementById('emailInputEmail').value
          if(UserName.toString().length>50){
            document.getElementById('error-input-Username').innerHTML="Character is too large"
            event.preventDefault()
            event.stopPropagation()
          }
          else if(Password.toString().length>50){
            document.getElementById('error-input-password').innerHTML="Character is too large"
            event.preventDefault()
            event.stopPropagation()
          }
          else if(Password.toString().length<8){
            document.getElementById('error-input-password').innerHTML="atleast 8 characters are required"
            event.preventDefault()
            event.stopPropagation()
          }
          else if(Name.toString().length>50){
            document.getElementById('error-input-name').innerHTML="Character is too large"
            event.preventDefault()
            event.stopPropagation()
          }
         
          else if(Email.toString().length>70){
            document.getElementById('error-input-email').innerHTML="Too Large charecter"
            event.preventDefault()
            event.stopPropagation()
          }
        }
        catch{
              
          // nothing
        }
        // end user define
        form.classList.add('was-validated')
      }, false)
      
      
    })
  })()


