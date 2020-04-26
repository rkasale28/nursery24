const cartTwoTemplate=document.createElement('template')
cartTwoTemplate.innerHTML=`
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
        
        
        <div class="btn-group mr-2" role="group" aria-label="First group">
            <button type="button" class="btn btn-success" id = "inc">+</button>
            <button type="button" class="btn btn-outline-secondary disabled" id = "result">0</button>
            <button type="button" class="btn btn-success" id = "dec">-</button>
        </div>
    </div>
    <div>Total = <span id = "total"></span>
    </div>
</div>`
        
class CartTwo extends HTMLElement{
    constructor(){
        super();
        this.attachShadow({mode: 'open'})
        this.shadowRoot.appendChild(cartTwoTemplate.content.cloneNode(true))
        this.shadowRoot.querySelector('h5').innerText=this.getAttribute('name')
        this.shadowRoot.querySelector('#price').innerText=this.getAttribute('price')
        this.shadowRoot.querySelector('#image').src=this.getAttribute('image')
        // this.shadowRoot.querySelector('#direct').addEventListener('click',()=>{
        //     location.href='/consumer/compareprices?id='+this.getAttribute('id')
        // })
        
        var btn=this.shadowRoot.querySelector('#compare')

        
        //this.innerHTML=`${this.getAttribute('name')}`
        let decodedCookie = decodeURIComponent(document.cookie).split(';');
        if(decodedCookie.find(item => item.includes("product="))){
            let productString = decodedCookie.find(item => item.includes("product="));
            //console.log(productString); success
            let productStringSplit = productString.split('=');
            let product = JSON.parse(productStringSplit[1]);
            
            if(product.find(item=> item.id)){
                if(product.find(item=> item.id == this.getAttribute('id'))){
                    let thisProduct = product.find(item=> item.id == this.getAttribute('id'));
                    this.shadowRoot.querySelector('#result').innerHTML = thisProduct.providers[0].quantity;
                    this.shadowRoot.querySelector('#price').innerHTML = thisProduct.providers[0].perPrice;
                    this.shadowRoot.querySelector('#total').innerHTML = thisProduct.providers[0].price;

                    console.log(thisProduct);
                }
                else{
                    let newProduct = {name: this.getAttribute('name'), img: this.getAttribute('image'), id: this.getAttribute('id'),
                    
                    providers:[
                        {
                            providerName : 'default',
                            quantity: 0,
                            perPrice: this.getAttribute('price'),
                            price: 0
                        }
                    ]
                    
                };
                product = [...product,newProduct];
                document.cookie = "product=" + JSON.stringify(product);
                console.log(product);
                }
            }


            
        }
        else{
            
                    let product = [{name: this.getAttribute('name'), img: this.getAttribute('image'), id: this.getAttribute('id'),
                    
                    providers:[
                        {
                            providerName : 'default',
                            quantity: 0,
                            perPrice: this.getAttribute('price'),
                            price: 0
                        }
                    ]
                    
                }]
         
                document.cookie = 'product=' + JSON.stringify(product);
                console.log(product);
        }
        
    }


    connectedCallback(){

        let name = this.shadowRoot.querySelector('h5').innerHTML;
        let price = this.shadowRoot.querySelector('#price').innerHTML;
        console.log(this.getAttribute('id'));
        //increments product in cookie
        this.shadowRoot.querySelector("#inc").addEventListener('click',()=>{
            
            let decodedCookie = decodeURIComponent(document.cookie).split(';');
            
                let productString = decodedCookie.find(item => item.includes("product="));
                //console.log(productString); success
                let productStringSplit = productString.split('=');
                let product = JSON.parse(productStringSplit[1]);
                
                    let thisProduct = product.find(item=> item.name == name);
                    product = product.filter(item=> item.name!= name);

                   thisProduct.providers[0].quantity += 1;
                   thisProduct.providers[0].price = thisProduct.providers[0].quantity * price;
                   this.shadowRoot.querySelector('#result').innerHTML = thisProduct.providers[0].quantity;
                   this.shadowRoot.querySelector('#total').innerHTML = thisProduct.providers[0].price;

                   product = [...product,thisProduct];console.log(product)
                document.cookie = "product=" + JSON.stringify(product);
                    
            
        });
            //decrements product in cookie
            this.shadowRoot.querySelector("#dec").addEventListener('click', ()=>{
                // let decodedCookie = decodeURIComponent(document.cookie).split(';');
                
                // let productString = decodedCookie.find(item => item.includes("product="));
                // let productStringSplit = productString.split('=');
                // let product = JSON.parse(productStringSplit[1]);

                        
                //             let thisProduct = product.find(item=> item.name == name);
                //             if(thisProduct.providers[0].quantity != 0){
                //                 product = product.filter(item=> item.name != name);
                //                 thisProduct.providers[0].quantity -= 1;
                //     thisProduct.providers[0].price = thisProduct.providers[0].quantity * thisProduct.providers[0].perPrice;
                //     this.shadowRoot.querySelector('#result').innerHTML = thisProduct.providers[0].quantity;
                //     product = [...product,thisProduct];console.log(product);
                //             }
                        
                //             decodedCookie = "product=" + JSON.stringify(product);

                let decodedCookie = decodeURIComponent(document.cookie).split(';');
                let disconnect = () => {
                    document.querySelector('cart-two').remove(); // 'disconnected from the DOM'
                }
                if(decodedCookie.find(item => item.includes("product="))){
                let productString = decodedCookie.find(item => item.includes("product="));
                let productStringSplit = productString.split('=');
                let product = JSON.parse(productStringSplit[1]);
                if(product != []){
                    if(product.find(item=> item.name == name)){
                        if(product.find(item=> item.name == name).providers[0].quantity != 0){
                            
                        let thisProduct = product.find(item=> item.name == name);
                        product = product.filter(item=> item.name != name);
                        thisProduct.providers[0].quantity -= 1;
                        thisProduct.providers[0].price = thisProduct.providers[0].perPrice * thisProduct.providers[0].quantity;
                        this.shadowRoot.querySelector('#result').innerHTML = thisProduct.providers[0].quantity;
                        this.shadowRoot.querySelector('#total').innerHTML = thisProduct.providers[0].price;

                        if(thisProduct.providers[0].quantity!= 0){
                            product = [...product,thisProduct];
                        }
                        else{
                            //disconnect();

                            location.reload("true");
                           disconnect();

                        }
                        document.cookie = 'product=' + JSON.stringify(product);
                        location.reload("true");
                        }
                    }
                }
                }

             
            });
    }

    disconnectedCallback() {
        // rerender();
        console.log('disconnected ...');
     }

     
    
}

window.customElements.define('cart-two',CartTwo)
