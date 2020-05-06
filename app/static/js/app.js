Vue.component('app-header', {
    template: `
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
        <a id="photogram" class="navbar brand" href="#"><img src="camera-icon.png"></img>Photogram</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav mr-auto">                
                <li class="nav-item active">
                    <router-link id="home">Home<span class="sr-only">(current)</span></router-link>
                </li>
                <li class="nav-item active">
                    <router-link id="explore">Explore<span class="sr-only">(current)</span></router-link>
                </li>
                <li class="nav-item active">
                    <router-link id="profile">My Profile<span class="sr-only">(current)</span></router-link>
                </li>
                <li class="nav-item active">
                    <router-link id="logout">Logout<span class="sr-only">(current)</span></router-link>
                </li>
            </ul>
        </div>
    </nav>
    `,

    data: function() {
        return {

        }
    },
});

Vue.component('app-footer', {
    template: `
    <footer>
        <div class="container-fluid">
            <p class="card-text">Copyright &copy; Flask Inc.</p>
        </div>
    </footer>
    `
});

const loginPage = Vue.component('/login', {
    template: `
    <div id="login">
        <h2>Login<h2><br>
        <div id="loginFormBox">
            <form id="loginForm">
                <label>Username</label>
                <input type="text"></input><br><br>
                <label>Password</label>
                <input type="password"></input><br><br>
                <button id="loginButton" type="submit" name="login">Login</button>
            </form>
        </div>
    </div>
    `
});

const newPostPage = Vue.component('/new_post', {
    template: `
    <div id="new_post">
        <h2>New Post<h2><br>
        <div id="newPostFormBox">
            <form id="newPostForm">
                <label>Photo</label>
                <input id="photo" type="file"></input><br><br>
                <label>Caption</label>
                <input id="caption" type="text" placeholder="Write a caption..."></input><br><br>
                <button id="newPostSubmitButton" type="submit" name="login">Submit</button>
            </form>
        </div>
    </div>
    `
});

const homePage = Vue.component('/home', {
    template: `
    <div id="home">
        <div id="mainBox>
            <p id="photogramLabel"><img src="camera-icon.png"></img>Photogram</p>
            <hr>
            <p>Share photos of your favourite moments with friends, famiy and the world.</p><br><br>
            <button id="login_button" type="submit">Login</button>
            <button id="register_button" type="submit">Register</button>
        </div>            
        <img id="homeImage" src="Document.png"></img>
    </div>
    `
});

const newUserPage = Vue.component('/new_user', {
    template: `
    <div id="new_user">
        <h2>Register</h2>
        <div id="newUserFormBox">
            <form>
                <label>Username</label><br>
                <input id="username" type="text" name="username"></input><br><br>
                <label>Password</label><br>
                <input id="password" type="password" name="password"></input><br><br>
                <label>First Name</label><br>
                <input id="first_name" type="text" name="first_name"></input><br><br>
                <label>Last Name</label><br>
                <input id="last_name" type="text" name="last_name"></input><br><br>
                <label>Email</label><br>
                <input id="email" type="email" name="email"></input><br><br>
                <label>Location</label><br>
                <input id="location" type="text" name="location"></input><br><br>
                <label>Biography</label><br>
                <input id="biography" type="text" name="biography"></input><br><br>
                <label>Photo</label><br>
                <input id="photo" type="file" name="photo"></input><br><br>
                <button id=registerButton type="submit"></button>
            </form>
        </div>
    </div>
    `
});

const explorePage = Vue.component('/explore', {
    template: `
    <div id="explore">
        <div ="rightButtonDiv>
            <button id="new_postButton" type="button">New Post</button>
        </div>
        <div id="exploreMainBox">
            <p id="user_name"><img id="profilePic"></img></p>
            <img id="imagePosted"></img>< br>
            <p id="imageCaption"></p><br><br>
            <p id="datePosted"></p>
            <p id="likes"><img id="likeIcon" src="heart-icon.png"></img></p>
        </div>        
    </div>
    `
});