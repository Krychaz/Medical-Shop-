console.log("Hello World")


var updateBtn = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtn.length; i++){
    updateBtn[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'Action', action )

        console.log('USER:', user)
        if(user == 'AnonymousUser'){
            addCookieItem(productId, action)
        }else
        {
            updateUserOrder(productId, action)
        }
  })
}

function addCookieItem(productId, action){
  console.log("User SUCCESS")
 
}

function updateUserOrder(productId, action){
  console.log('user is authenticated')
  var url = '/update_item/'

  fetch(url, {
    method: 'POST',
    headers:{
      'Content-Type': 'application/json',
      'X-CSRFtoken':csrftoken
    },
    body:JSON.stringify({'productId': productId, 'action': action})
  })
    .then((response) =>{
      return response.json()
  })
    .then((data) =>{
      console.log('data: ', data)
      location.reload()
  })
}