console.log("Hello World")


var updateBtn = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtn.length; i++){
    updateBtn[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'Action', action )

        console.log('User:', user)
        if(user === 'AnonUser'){
            console.log('User not verified')
        }else
        {
            updateUserOrder(productId, action)
        }
  })
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
  })
}