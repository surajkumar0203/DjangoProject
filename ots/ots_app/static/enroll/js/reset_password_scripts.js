// password and conform password are same or not and also check password atleast

function validate_password(){
    let password=document.getElementById('passwordInputPassword').value
    let conform_password=document.getElementById('conform_usernameInputPassword').value

    if(password.toString().length<8){
        
        let c=document.getElementById('error-input-password');
        c.innerHTML='At list 8 charecter required';
        c.style.color="red";
      
        return false;
    }
    console.log(password.toString())
    console.log(conform_password.toString())
    if(password.toString()!=conform_password.toString()){
        let c=document.getElementById('error-input-password');
        c.innerHTML="Password and conform password must be same";
        c.style.color="red";
        return false;
    }
    return true
}