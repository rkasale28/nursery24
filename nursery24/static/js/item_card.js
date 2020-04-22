const template2=document.createElement('template')
template2.innerHTML=`
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<style>
        .card {
            display: inline-block;
        }

        .card-img-top {
            width: 100%;
            height: 15vw;
            object-fit: cover;
        }

        .d-block {
            height: 20vw;
            object-fit: cover;
        }

        li {
            list-style-type: none;
        }
    </style>
<div class="card mr-3" style="width: 255px;">
    <img class="card-img-top" id='image' style="{width: 100%,height: 15vw,object-fit: cover;}">

    <div class="card-body">
        <h5 class="card-title"><span id='name'></span></h5>
        <h6 class="card-subtitle text-muted">Rs. <span id='price'></span></h6>

    </div>

    <div class="btn-toolbar ml-1 mb-2" role="toolbar" aria-label="Toolbar with button groups">
        
        <div class="btn-group ml-auto mr-2" role="group" aria-label="First group">
            <button type="button" class="btn btn-success" id = "inc">+</button>
            <button type="button" class="btn btn-outline-secondary disabled" id = "result">0</button>
            <button type="button" class="btn btn-success" id = "dec">-</button>
        </div>
    </div>
            
</div>`
        
class ItemCard extends HTMLElement{
    constructor(){
        super();
        this.attachShadow({mode: 'open'})
        this.shadowRoot.appendChild(template2.content.cloneNode(true))
        this.shadowRoot.querySelector('h5').innerText=this.getAttribute('name')
        this.shadowRoot.querySelector('#price').innerText=this.getAttribute('price')
        this.shadowRoot.querySelector('#image').src=this.getAttribute('image')
        //this.innerHTML=`${this.getAttribute('name')}`
        let decodedCookie = decodeURIComponent(document.cookie).split(';');
        if(decodedCookie.find(item => item.includes("product="))){
                let productString = decodedCookie.find(item => item.includes("product="));
                //console.log(productString); success
                let productStringSplit = productString.split('=');
                let product = JSON.parse(productStringSplit[1]);
                
                if(product.find(item=> item.name == this.getAttribute('name'))){
                    this.shadowRoot.querySelector("#result").innerHTML = product.find(item=> item.name == this.getAttribute('name')).price;
                }
            }
    }

    connectedCallback(){

        
        let name = this.shadowRoot.querySelector('h5').innerHTML;
        let price = this.shadowRoot.querySelector('#price').innerHTML;
        let img = this.shadowRoot.querySelector('#image').src;
        //increments product in cookie
        this.shadowRoot.querySelector("#inc").addEventListener('click',()=>{
            
            let decodedCookie = decodeURIComponent(document.cookie).split(';');
        
            //console.log(price,name,decodedCookie);
            if(!decodedCookie.find(item => item.includes("product="))){
                let product = [{name: name, quantity: 1,perPrice: price,price: price,img: img}]
                //console.log(product);
                document.cookie = 'product=' + JSON.stringify(product);
                //console.log(document.cookie);
                this.shadowRoot.querySelector("#result").innerHTML = price;
                console.log(product);
            }
            else{
                let productString = decodedCookie.find(item => item.includes("product="));
                //console.log(productString); success
                let productStringSplit = productString.split('=');
                let product = JSON.parse(productStringSplit[1]);
               // console.log(product);// success
                if(!product.find(item=> item.name == name)){
                    let newProduct = {name: name,quantity: 1, perPrice: price, price: price, img: img};
                    this.shadowRoot.querySelector("#result").innerHTML = price;
                    product = [...product,newProduct];
                    console.log(product);
                    document.cookie = 'product=' + JSON.stringify(product);
                }
                else
                {let thisProduct = product.pop(item => item.name == name);
                thisProduct.quantity += 1;
                thisProduct.price = thisProduct.perPrice * thisProduct.quantity;
                this.shadowRoot.querySelector("#result").innerHTML = thisProduct.price;
                product = [...product,thisProduct];
                console.log(product);
                document.cookie = 'product=' + JSON.stringify(product);  
                }
            }
            
            //decrements product in cookie
            this.shadowRoot.querySelector("#dec").addEventListener('click', async ()=>{
               let decodedCookie = await decodeURIComponent(document.cookie).split(';');
                //console.log(decodedCookie.find(item=> item.includes("product=")))
               if(decodedCookie.find(item=> item.includes("product="))){
                   let productString = decodedCookie.find(item => item.includes("product="));
                  // console.log(productString);
                   let productStringSplit = productString.split('=');
                let product = JSON.parse(productStringSplit[1]);
                if(product.find(item=> item.name == name)){
                    let thisProduct = product.find(item=> item.name==name);

                    product = product.filter(item=> item.name != name);
                    document.cookie = 'product=' + JSON.stringify(product);
                    console.log('product',product)
                    console.log('thisProduct',thisProduct)
                thisProduct.quantity -= 1;
                console.log('thisProduct.quantity',thisProduct.quantity)

                thisProduct.price = thisProduct.perPrice * thisProduct.quantity;
                console.log('thisProduct.price',thisProduct.price)
                console.log('thisProduct',thisProduct)
                this.shadowRoot.querySelector('#result').innerHTML = thisProduct.price;
                if(thisProduct.quantity!= 0){
                    product = [...product,thisProduct];
                    console.log(product);
                }  
                document.cookie = 'product=' + JSON.stringify(product);
                }
                
                    }
                // let result = this.shadowRoot.querySelector('#result').innerHTML;
                // console.log(result);
                // if(result != 0){
                // let decodedCookie = decodeURIComponent(document.cookie).split(';');
                
                // console.log(productString); success
                
                
                
                // console.log('result',result)

                
               
                //}
            });
        });
    }

}

window.customElements.define('item-card',ItemCard)
