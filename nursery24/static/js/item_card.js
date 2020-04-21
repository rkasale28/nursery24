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
    }

    connectedCallback(){
        let name = this.shadowRoot.querySelector('h5').innerHTML;
        let price = this.shadowRoot.querySelector('#price').innerHTML;
        this.shadowRoot.querySelector("#inc").addEventListener('click',()=>{
            let result = this.shadowRoot.querySelector("#result");
            let decodedCookie = decodeURIComponent(document.cookie).split(';');
        
            console.log(price,name,decodedCookie);
            //console.log(decodedCookie.find(item => item.name == name))
            
            result.innerHTML = price;
        });
    }

}

window.customElements.define('item-card',ItemCard)
