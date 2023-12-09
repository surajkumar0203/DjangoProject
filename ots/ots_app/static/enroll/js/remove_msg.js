let msg=document.getElementsByClassName('msg')[0]
msg.classList.add('index');
let info=document.getElementById('values').innerText

if (info[info.length-1] == '.') {
    document.getElementById('toast-box').classList.add('error')
}

setInterval(() => {
    // we have use index class bcz last me class likha hota hai uska precedence high hota hai
    document.getElementsByClassName('index')[0].remove()
}, 5000)