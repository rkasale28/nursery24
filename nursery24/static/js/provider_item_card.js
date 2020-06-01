const template4=document.createElement('template')
template4.innerHTML=`
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
    <div class="card mr-3" style="width: 255px">
    <img class="card-img-top" id='image' style="{width: 100%,height: 15vw,object-fit: cover;}">

    <div class="card-body">
        <h5 class="card-title"></h5>
        <h6 class="card-subtitle text-muted">Rs. <span id='price'></span></h6>
    </div>
    <h3></h3>
    
    <div class="sticky-bottom float-left ml-2 mb-2">
    <form action="updateprice" method="post">
        <input name="csrfmiddlewaretoken" type="hidden">
        <input name="id" type="hidden">
        <input name="proid" type="hidden">   
        <button type="submit" class="btn btn-primary">Update Price</button>         
    </form>    
    </div>

    <div class="sticky-bottom float-right mr-2 mb-2">
        <form action="removeitemsubmit" method="post">
        <input name="csrfmiddlewaretoken" id="csrf" type="hidden">
        <input name="id" id="id" type="hidden">
        <input name="proid" id="proid" type="hidden">
        <button type="submit" class="btn btn-danger ml-1">Delete</button>            
    </form>
    </div>
</div>
  

<script src="https://code.jquery.com/jquery-3.4.1.slim.min.js"
integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n"
crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"
integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo"
crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"
integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6"
crossorigin="anonymous"></script>
`
        
class ProviderItemCard extends HTMLElement{
    constructor(){
        super();
        this.attachShadow({mode: 'open'})
        this.shadowRoot.appendChild(template4.content.cloneNode(true))
        this.shadowRoot.querySelector('h5').innerText=this.getAttribute('name')
        this.shadowRoot.querySelector('#price').innerText=this.getAttribute('price')
        this.shadowRoot.querySelector('#image').src=this.getAttribute('image')
        
        this.shadowRoot.querySelector('input[name="csrfmiddlewaretoken"]').value=this.getAttribute('token')
        this.shadowRoot.querySelector('input[name="id"]').value=this.getAttribute('id')
        this.shadowRoot.querySelector('input[name="proid"]').value=this.getAttribute('proid')

        this.shadowRoot.querySelector('#csrf').value=this.getAttribute('token')
        this.shadowRoot.querySelector('#id').value=this.getAttribute('id')
        this.shadowRoot.querySelector('#proid').value=this.getAttribute('proid')

        
    }

}

window.customElements.define('provider-item-card',ProviderItemCard)
