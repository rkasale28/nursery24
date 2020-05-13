const template3 = document.createElement('template')
template3.innerHTML = `
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<link rel="stylesheet" href="https://opensource.keycdn.com/fontawesome/4.7.0/font-awesome.min.css" integrity="sha384-dNpIIXE8U05kAbPhy3G1cz+yZmTzA6CY8Vg/u2L9xRnHjJiAK76m2BIEaSEV+/aU" crossorigin="anonymous">
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
        
        <div class="btn-group mr-2" role="group" aria-label="Second group">
            <button type="button" id="compare" class="btn btn-primary">Compare Price</button>
        </div>

        <div class="btn-group mr-2" role="group" aria-label="First group">
            <button type="button" class="btn btn-success" id = "inc">+</button>
            <button type="button" class="btn btn-outline-secondary disabled" id = "result">0</button>
            <button type="button" class="btn btn-success" id = "dec">-</button>
        </div>
    </div>
    
    <div class="progress" style="height: 20px;">
        <div class="progress-bar bg-warning" id="progress" role="progressbar" aria-valuemin="0" aria-valuemax="100">
        <span style="display:inline;" id="label"></span>
    </div>
</div>
</div>`

class ComparePriceItemCard extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' })
        this.shadowRoot.appendChild(template3.content.cloneNode(true))
        this.shadowRoot.querySelector('h5').innerText = this.getAttribute('name')
        this.shadowRoot.querySelector('#price').innerText = this.getAttribute('price')
        this.shadowRoot.querySelector('#image').src = this.getAttribute('image')
        
        var avg_rating=this.getAttribute('rating')
        console.log(avg_rating)

        this.shadowRoot.querySelector('#progress').style.width=avg_rating+'%'
        this.shadowRoot.querySelector('#progress').setAttribute('aria-valuenow',avg_rating)
        this.shadowRoot.querySelector('#label').innerText = avg_rating+' %'
               
        // this.shadowRoot.querySelector('#direct').addEventListener('click',()=>{
        //     location.href='/consumer/compareprices?id='+this.getAttribute('id')
        // })
        // console.log(this.getAttribute('i').providers);
        console.log(this.getAttribute('provider'));
        var btn = this.shadowRoot.querySelector('#compare')

        btn.onclick = (event) => {
            location.href = '/consumer/compareprices?id=' + this.getAttribute('id')
        }
        //this.innerHTML=`${this.getAttribute('name')}`
        let decodedCookie = decodeURIComponent(document.cookie).split(';');
        if (decodedCookie.find(item => item.includes("product="))) {
            let productString = decodedCookie.find(item => item.includes("product="));
            //console.log(productString); success
            let productStringSplit = productString.split('=');
            let product = JSON.parse(productStringSplit[1]);
            if (product.find(item => item.id)) {
                if (product.find(item => item.id == this.getAttribute('id'))) {
                    let thisProduct = product.find(item => item.id == this.getAttribute('id'));
                    this.shadowRoot.querySelector("#result").innerHTML = thisProduct.providers[0].quantity;
                    this.shadowRoot.querySelector("#price").innerHTML = thisProduct.providers[0].perPrice;
                    console.log(thisProduct);
                    if (!thisProduct.img) {
                        product = product.filter(item => item.id != this.getAttribute('id'));
                        thisProduct.img = this.getAttribute('image');
                        thisProduct.name = this.getAttribute('name');
                        product = [...product, thisProduct];
                        document.cookie = 'product=' + JSON.stringify(product);
                    }

                }
            }

        }

    }


    connectedCallback() {

        let name = this.shadowRoot.querySelector('h5').innerHTML;
        let price = this.shadowRoot.querySelector('#price').innerHTML;
        let id = this.getAttribute('id');
        let provider = this.getAttribute('provider');
        let img = this.shadowRoot.querySelector('#image').src
        console.log(this.getAttribute('id'));
        //increments product in cookie
        this.shadowRoot.querySelector("#inc").addEventListener('click', () => {

            let decodedCookie = decodeURIComponent(document.cookie).split(';');

            //console.log(price,name,decodedCookie);
            if (!decodedCookie.find(item => item.includes("product="))) {
                let product = [{ name: name, providers: [{ providerName: provider, quantity: 1, perPrice: price, price: price }], img: img, id: id }];
                //console.log(product);
                document.cookie = 'product=' + JSON.stringify(product);
                //console.log(document.cookie);
                this.shadowRoot.querySelector("#result").innerHTML = 1;

                console.log(product);
            }
            else {
                let productString = decodedCookie.find(item => item.includes("product="));
                //console.log(productString); success
                let productStringSplit = productString.split('=');
                let product = JSON.parse(productStringSplit[1]);
                // console.log(product);// success
                if (!product.find(item => item.name == name)) {
                    let newProduct = { name: name, providers: [{ providerName: provider, quantity: 1, perPrice: price, price: price }], img: img, id: id };

                    this.shadowRoot.querySelector("#result").innerHTML = newProduct.providers[0].quantity;

                    product = [...product, newProduct];
                    console.log(product);
                    document.cookie = 'product=' + JSON.stringify(product);
                }
                else {
                    let thisProduct = product.find(item => item.name == name);
                    product = product.filter(item => item.name != name);
                    thisProduct.providers[0].quantity += 1;
                    thisProduct.providers[0].price = thisProduct.providers[0].perPrice * thisProduct.providers[0].quantity;
                    this.shadowRoot.querySelector("#result").innerHTML = thisProduct.providers[0].quantity;
                    product = [...product, thisProduct];
                    console.log(product);
                    document.cookie = 'product=' + JSON.stringify(product);
                }
            }

        });
        //decrements product in cookie
        this.shadowRoot.querySelector("#dec").addEventListener('click', () => {
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
            if (decodedCookie.find(item => item.includes("product="))) {
                let productString = decodedCookie.find(item => item.includes("product="));
                let productStringSplit = productString.split('=');
                let product = JSON.parse(productStringSplit[1]);
                if (product != []) {
                    if (product.find(item => item.name == name)) {
                        if (product.find(item => item.name == name).providers[0].quantity != 0) {

                            let thisProduct = product.find(item => item.name == name);
                            product = product.filter(item => item.name != name);
                            thisProduct.providers[0].quantity -= 1;
                            thisProduct.providers[0].price = thisProduct.providers[0].perPrice * thisProduct.providers[0].quantity;
                            this.shadowRoot.querySelector('#result').innerHTML = thisProduct.providers[0].quantity;
                            if (thisProduct.providers[0].quantity != 0) {
                                product = [...product, thisProduct];
                            }
                            console.log(product);
                            document.cookie = 'product=' + JSON.stringify(product);
                        }
                    }
                }
            }


        });
    }

}

window.customElements.define('compare-price-item-card', ComparePriceItemCard)
