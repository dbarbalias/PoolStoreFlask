
class Cart{
    constructor(){
        let temp_cart = JSON.parse(localStorage.getItem('cart'));
        if(typeof temp_cart == "undefined" || temp_cart === null) {
            //create cart if it doenst exist and reference the obj
            localStorage.setItem('cart', JSON.stringify({})); //creates an empty cart
        }
        Cart.count_inv();
    }
    static add_item(inv_id, run_toggle_cart=true){
        
        let temp_cart = JSON.parse(localStorage.getItem('cart')); //refrence local storage
        if(typeof temp_cart == "undefined" || temp_cart === null) {
            console.log('in if')
            //create cart if it doenst exist and reference the obj
            localStorage.setItem('cart', JSON.stringify({})); //creates an empty cart
            temp_cart = {};
        }
        if(temp_cart.hasOwnProperty(inv_id)){
            temp_cart[inv_id] += 1;
        }
        else{
            temp_cart[inv_id] = 1;
        }
        localStorage.setItem('cart', JSON.stringify(temp_cart)); 
        Cart.count_inv();
        if (run_toggle_cart){
            Cart.toggle_cart(); //display what you added
        }
        cartCode();
      
        
    }
    static delete_item(inv_id){
        let temp_cart = JSON.parse(localStorage.getItem('cart')); //refrence local storage
        if(typeof temp_cart == "undefined" || temp_cart === null) {
            //create cart if it doenst exist and reference the obj
            localStorage.setItem('cart', JSON.stringify({})); //creates an empty cart
            temp_cart = {};
        }
        if(temp_cart.hasOwnProperty(inv_id)){ //check if it exists

            delete temp_cart[inv_id]; //delete if youre going from 1 to zero
        }
        localStorage.setItem('cart', JSON.stringify(temp_cart)); 
        Cart.count_inv();
        cartCode();
       
    }
    static remove_item(inv_id){
        let temp_cart = JSON.parse(localStorage.getItem('cart')); //refrence local storage
        if(typeof temp_cart == "undefined" || temp_cart === null) {
            //create cart if it doenst exist and reference the obj
            localStorage.setItem('cart', JSON.stringify({})); //creates an empty cart
            temp_cart = {};
        }
        if(temp_cart.hasOwnProperty(inv_id)){ //check if it exists
            if(temp_cart[inv_id] == 1){
                delete temp_cart[inv_id]; //delete if youre going from 1 to zero
            }
            else{
                temp_cart[inv_id] -=1;
            }
        }
        localStorage.setItem('cart', JSON.stringify(temp_cart)); 
        Cart.count_inv();
        cartCode();
       
    }
    static count_inv(){
        let counter = 0;
        let temp_cart = JSON.parse(localStorage.getItem('cart'));
        for(let i in temp_cart)
        { 
            counter += temp_cart[i];
        }
        //change the inner html in the banner
        let cartItems = document.getElementById('cart-items');
        cartItems.innerHTML = counter; //need to find the cartItems 
    }
    static toggle_cart(){
        let nav_class_list = document.getElementsByClassName('navbar')[0].classList;
        console.log(nav_class_list);
        document.getElementsByClassName('cart-layout')[0].style.visibility
        console.log(status);
        if (nav_class_list['value'].includes('sticky-top')){
            cartCode();
            document.getElementsByClassName('cart-layout')[0].style.visibility = 'visible';
            nav_class_list.remove('sticky-top');

        }else{
            document.getElementsByClassName('cart-layout')[0].style.visibility = 'hidden';
            nav_class_list.add('sticky-top');
        }

    }
}


document.addEventListener("DOMContentLoaded", () => {
    //localStorage.setItem('inventory',JSON.stringify({{ product_json|tojson }}));
    //localStorage.setItem('cart', JSON.stringify({}));
    new Cart();
});


function cartCode()
{
    let tempCart = JSON.parse(localStorage.getItem('cart'));
    let tempInventory = JSON.parse(localStorage.getItem('inventory'));
    let cartHTML = document.getElementById('cart-content');
    let cartItems = document.getElementById('cart-items');

    if(typeof tempCart == "undefined" || tempCart === null || cartItems.innerHTML == 0) {
      
        let cartBody =  `<h4>No Items In Cart</h4><br><br>`
        let footer = `<div class="cart-footer">
        <div class="row">
                <h5 class="col-8 float-left">Merchandise Subtotal: </h5>
                <h5 class="cart-total col-4">$0.00</h5>            
            </div>
        <button class='btn inv-btn btn-md btn-primary' onclick='Cart.toggle_cart();' src='#'>Back to Store</button>
        </div>`;
        cartHTML.innerHTML = cartBody + footer;

    }
    else
    {
        let total = 0;
        let cartBody = '';
        for(let i in tempCart){
            try {
                total += parseFloat(tempInventory[i]['price']) * parseInt(tempCart[i]); //to fixed rounds the number to two decimal places
                let img_path = `${tempInventory[i]['img_file']}`;
                cartBody += `
                    <div style="background: rgb(231, 226, 221);" class='row mb-4'>
                        <img class="col float-left" style='width:15%; height:auto;' src="static/images/${img_path}" alt="">
                        <div class="col">
                            <h5>${tempInventory[i]['name']}</h5>
                            <p>$${tempInventory[i]['price']}</p>
                            <p class="remove-item" onclick='Cart.delete_item(${i});' id="remove-${i}">remove</p>
                        </div>
                        <div class='col float-right'>
                           
                        <i onclick='Cart.add_item(${i}, run_toggle_cart=false);' class="fas fa-chevron-up"></i>
                            <br>
                            <span class="item-amount">
                            ${tempCart[i]}
                            </span>
                            <br>
                            
                            <i onclick='Cart.remove_item(${i});' class="fas fa-chevron-down"></i>
                            
                        </div>

                    </div>

                `;
                
              }
              catch(error) {
                console.log(error);
                // expected output: ReferenceError: nonExistentFunction is not defined
                // Note - error messages will vary depending on browser
              }

        };
        let footer = `<div class="cart-footer">
            <div class="row">
                <h5 class="col-7 float-right">&emsp;Merchandise Subtotal: </h5>
                <h5 class="cart-total col-4 float-left">$${total.toFixed(2)}</h5>            
            </div>
            <a><button class='btn inv-btn btn-md btn-primary' src='#'>Check Out</button></a>
                                </div>`;
        cartHTML.innerHTML = cartBody + footer;
    }
}  