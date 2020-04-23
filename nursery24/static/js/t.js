const template2=document.createElement('template')
template2.innerHTML=`
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
        integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
    <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">


    <tbody>
                
                
    <td class = "ml-3"><span id = 'provider'></span></td>
    <td><span id = 'price'></span></td>
    <td><span id = 'addr'></span></td>
    <td class = "float-left  ">
        <div  class="btn-toolbar ml-1 mb-2" role="toolbar" aria-label="Toolbar with button groups">

            <div class="btn-group ml-auto mr-2" role="group" aria-label="First group">
                <button type="button" class="btn btn-success" id = "inc">+</button>
                <button type="button" class="btn btn-outline-secondary disabled" id = "result">0</button>
                <button type="button" class="btn btn-success" id = "dec">-</button>
            </div>
        </div>
    </td>
    <br>
    
</tbody>`

class Row extends HTMLElement{

    constructor(){
        super();
        this.attachShadow({mode: 'open'});
        this.shadowRoot.appendChild(template2.content.cloneNode(true));
        this.shadowRoot.querySelector('#provider').innerHTML = this.getAttribute('provider');
        
        this.shadowRoot.querySelector('#price').innerHTML = this.getAttribute('price');
        this.shadowRoot.querySelector('#addr').innerHTML = this.getAttribute('addr');

    }


}
window.customElements.define('across-row',Row);


{/* <script defer>
let name = '';
let decodedCookie = decodeURIComponent(document.cookie).split(';');
        if(decodedCookie.find(item => item.includes("product="))){
            let productString = decodedCookie.find(item => item.includes("product="));
            //console.log(productString); success
            let productStringSplit = productString.split('=');
            let product = JSON.parse(productStringSplit[1]);
            
            if(product.find(item=> item.name == this.getAttribute('name'))){
                if(!product.providers){
                    this.shadowRoot.querySelector("#result").innerHTML = product.find(item=> item.name == this.getAttribute('name')).quantity;
                }
                else{
                    thisProduct = product.find(item=> item.name == name)
                    this.shadowRoot.querySelector("#result").innerHTML = thisProduct.providers.reduce((subtotal,item)=>{return item.quantity + subtotal},0);
                }
            }
        }


        </script> */}