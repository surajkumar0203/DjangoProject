let hamburger = document.getElementById('hamburger');
let flag=0;
hamburger.addEventListener('click',function(){
    let ul=document.getElementsByClassName("buttons-container")[0];
    let temp=document.getElementsByClassName("line");
    let line1=temp[0];
    let line2=temp[1];
    let line3=temp[2];
    
    
    if(flag==0){
        ul.style.transform='translateX(0%)';
        flag=1;
        
        line1.style.rotate="45deg"
        line2.style.display="none"
        line3.style.rotate="-45deg"
        
    }
    else{
        ul.style.transform='translateX(-100%)';
        flag=0;
        line1.style.rotate="0deg"
        line2.style.display="block"
        line3.style.rotate="0deg"

        
    }



})

