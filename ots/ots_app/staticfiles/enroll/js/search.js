let search = document.getElementById('search')
  search.addEventListener('input', () => {
    let search_value = search.value.toLowerCase()
    let div_box=document.getElementById('div-box')
    let p_box=div_box.getElementsByTagName('p')
    let col=document.getElementsByClassName('col')
    let flag=1
    for(let i=0;i<p_box.length;i++){
      let text_value=p_box[i].innerText
      if(text_value.toLowerCase().match(search_value)){
        col[i].style.display='block'
        flag=0
      }
      else{
        col[i].style.display='None'
      }
    }
    if(flag){
      document.getElementById('faild-search').style.display='block'
    }
    else{
      document.getElementById('faild-search').style.display='none'
    }

})