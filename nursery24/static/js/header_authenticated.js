const template1=document.createElement('template')
template1.innerHTML=`
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    <nav class="navbar navbar-expand-lg navbar-light" style="background-color:#85EF50">
        <a class="navbar-brand" href="#">
        <img src='../static/images/logo.png' width="100"
                style="margin-left:10"></a>

        <form class="form-inline my-2 my-lg-0" style="margin-left: 100px;">
            <input class="form-control mr-sm-2" size="80" type="search" placeholder="Search" aria-label="Search">
            <button class="btn btn-success my-2 my-sm-0" type="submit">Search</button>
        </form>
        
        
        <form class="ml-auto">
            <button formaction="myprofile" class="btn btn-primary">My Profile</button>
        </form>

        <form class="ml-auto mr-3">
            <button formaction="logout" class="btn btn-primary">Logout</button>
        </form>
                        
        
    </nav>`

class HeaderAuthenticated extends HTMLElement{
    constructor(){
        super();
        this.attachShadow({mode: 'open'})
        this.shadowRoot.appendChild(template1.content.cloneNode(true))
        // this.shadowRoot.querySelector('h3').innerText=this.getAttribute('name')
        //this.innerHTML=`${this.getAttribute('name')}`
    }

}

window.customElements.define('authenticated-header',HeaderAuthenticated)
