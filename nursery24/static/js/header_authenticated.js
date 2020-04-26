const template1=document.createElement('template')
template1.innerHTML=`
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    <nav class="navbar navbar-expand-lg navbar-light bg-warning">
        <a class="navbar-brand" href="#">
        <img src='../static/images/logo.png' width="100"
                style="margin-left:10"></a>

        <form  class="form-inline my-2 my-lg-0" action = "search" style="margin-left: 100px;">
            <input class="form-control mr-sm-2" size="80" type="search" placeholder="Search" aria-label="Search" name ="search">
            <button class="btn btn-success my-2 my-sm-0" type="submit">Search</button>
        </form>
        
        
        <form class="ml-auto">
            <button formaction="myprofile" class="btn btn-primary">My Profile</button>
        </form>

        <form class="ml-auto mr-3">
            <button id = "logout" class="btn btn-primary">Logout</button>
        </form>
                        
        
    </nav>`

class HeaderAuthenticated extends HTMLElement{
    constructor(){
        super();
        this.attachShadow({mode: 'open'})
        this.shadowRoot.appendChild(template1.content.cloneNode(true))
    }
    connectedCallback(){

    this.shadowRoot.querySelector("#logout").addEventListener('click',()=>{
        document.cookie = 'product=; expires=Thu, 01 Jan 1970 00:00:00 UTC'
        console.log("Button pressed");
        window.location.href = 'logout'
        disconnect();

    })
}

}

window.customElements.define('authenticated-header',HeaderAuthenticated)
let disconnect = () => {
    document.querySelector('authenticated-header').remove(); // 'disconnected from the DOM'
}