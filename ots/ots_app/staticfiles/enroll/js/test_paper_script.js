// check all question checked or not

function dis(){
    alert("You can't Inspect this page for security purpose");
    return false;
}
document.getElementById('content').onkeydown = (e) => {
    return false;
};

function form_validate(){

    let main=document.getElementsByClassName('main-div')
    let check_1=document.getElementsByClassName('check-1')
    let check_2=document.getElementsByClassName('check-2')
    let check_3=document.getElementsByClassName('check-3')
    let check_4=document.getElementsByClassName('check-4')
  
    let i=0;
    let flag=0
   
    while(i<main.length){
        if(check_1[i*1].checked || check_2[i*1].checked || check_3[i*1].checked || check_4[i*1].checked){
            main[i].classList.remove('border-danger')
        }
        else{
            main[i].classList.add('border-danger')
            flag=1
        }
        i++;
        
    }

    if(flag)
    {
        window.scrollTo(0,0)
        return false;
    }
    else
        return true
}