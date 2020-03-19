const template=document.createElement('template')
template.innerHTML=`
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    <nav class="navbar navbar-expand-lg navbar-light" style="background-color:#85EF50">
        <a class="navbar-brand" href="#">
        <img src='../static/images/logo.png' 
        width="100"
                style="margin-left:10"></a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>

        <form class="form-inline my-2 my-lg-0" style="margin-left: 100px;">
            <input class="form-control mr-sm-2" size="80" type="search" placeholder="Search" aria-label="Search">
            <button class="btn btn-success my-2 my-sm-0" type="submit">Search</button>
        </form>

        <button type="button" class="btn btn-primary ml-auto" style="margin-right: 10px;">Login</button>
    </nav>`

class Header extends HTMLElement{
    constructor(){
        super();
        this.attachShadow({mode: 'open'})
        this.shadowRoot.appendChild(template.content.cloneNode(true))
        //this.shadowRoot.querySelector('h3').innerText=this.getAttribute('name')
    }

}

window.customElements.define('header-file',Header)
