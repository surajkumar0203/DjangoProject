function f1(){
  
    let msg=document.getElementsByTagName('textarea')[0].value;
   
    if(msg.length>500){
      document.getElementById('message-textarea').innerHTML="Maximum 500 Characters are allowed";
      return false
    
    }
  return true
  }