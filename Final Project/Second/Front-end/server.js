// load the things we need
var express = require('express');
var app = express();
const bodyParser  = require('body-parser');
const fetch = require("node-fetch");

app.use(express.static("public"));
const axios = require('axios');
app.use(bodyParser.urlencoded({extended: true}));

// set the view engine to ejs
app.set('view engine', 'ejs');

// use res.render to load up an ejs view file

// index page 
app.get('/', function(req, res) {
    var mascots = [
        { name: 'Sammy', organization: "DigitalOcean", birth_year: 2012},
        { name: 'Tux', organization: "Linux", birth_year: 1996},
        { name: 'Moby Dock', organization: "Docker", birth_year: 2013}
    ];
    var tagline = "No programming concept is complete without a cute animal mascot.";

    res.render('pages/index', {
        mascots: mascots,
        tagline: tagline
    });
});

// home page
app.get('/home', function(req, res){
    var tagline = "Add Users! Enter Movies! Receive your random pick!";
    res.render('pages/home',
    {
        tagline: tagline
    });

});


// USER POINTS
// add user page
app.get('/useradd', function(req, res) {
    res.render("pages/useradd");
});

app.get('/userupdate', function(req, res) {
    res.render("pages/userupdate");
});

app.get('/userdelete', function(req, res) {
    res.render("pages/userdelete");
});
// USER POINTS END

app.get('/test', function(req, res) {
    // this will render our new example spage 
    res.render("pages/test");
});

//form  add user
app.post('/process_form', function(req, res){
    // create a variable to hold the username parsed from the request body
    var username = req.body.fname
    // create a variable to hold ....
    var password = req.body.lname

    // print variable username to console
    console.log(JSON.stringify(req.body));
    fetch('http://127.0.0.1:5000/api/db/adduser', { method: 'POST', headers: {'Content-Type':'application/json; charset=utf-8'}, body: JSON.stringify(req.body)})
    .then(function (res) {
        return res.text();
      })
    .then(data => console.log(data))
    .then(data => console.log(JSON.stringify(req.body)))
    .catch(error => console.log('ERROR'))
 
    
    res.render('pages/thanks.ejs', {body: req.body})
  
});

// RANDOM PICK POINTS START
// loads the randompick page
app.get('/randompick', function(req, res) {
    // this will render our new example spage 
    axios.get(`http://127.0.0.1:5000/api/friends/all`)
    .then((response) => {  
  
    var friend = response.data;

    //use res.render to load up an ejs view file
    res.render('pages/randompick', {
        user: friend
    });
    })
    .catch(error => console.log(error)); 
});

app.get('/randselec', function(req, res) {
    // this will render our new example spage 
    axios.get(`http://127.0.0.1:5000/api/friends/all`)
    .then((response) => {  
  
    var friend = response.data;

    //use res.render to load up an ejs view file
    res.render('pages/randselec', {
        user: friend
    });
    })
    .catch(error => console.log(error)); 
});


// Form that takes the data from the checkboxes for selecting users
app.post('/random_form', function(req, res){
    // create a variable to hold the username parsed from the request body
    var selection = req.body
    console.log(JSON.stringify(selection))
    // print variable username to console
    console.log(JSON.stringify(req.body));
    fetch('http://127.0.0.1:5000/api/movies/random', { method: 'POST', headers: {'Content-Type':'application/json; charset=utf-8'}, body: JSON.stringify(req.body)})
    .then(function (res) {
        return res.text();
      })
    .then(data => console.log(data))
    .then(data => console.log(JSON.stringify(req.body)))
    .catch(error => console.log('ERROR'))
 
    
    res.render('pages/thanks.ejs', {body: req.body})
  
});


// RANDOM PICK POINTS END


// MOVIE POINTS START
// add user page loads it up
app.get('/movieadd', function(req, res) {
    
    //get multiple service calls and combine the results in 1 function
    axios.get(`http://127.0.0.1:5000/api/friends/all`)
    .then((response) => {  
  
    var friend = response.data;
    var tagline = "Here is the data coming from my own API";

    //use res.render to load up an ejs view file
    res.render('pages/movieadd', {
        user: friend,
        tagline: tagline,
    });
    })
    .catch(error => console.log(error)); 
});
app.get('/movieupdate', function(req, res) {
    
    //get multiple service calls and combine the results in 1 function
    axios.get(`http://127.0.0.1:5000/api/friends/all`)
    .then((response) => {  
  
    var friend = response.data;
    var tagline = "Here is the data coming from my own API";

    //use res.render to load up an ejs view file
    res.render('pages/movieupdate', {
        user: friend,
        tagline: tagline,
    });
    })
    .catch(error => console.log(error)); 
});
app.get('/moviedelete', function(req, res) {
    
    //get multiple service calls and combine the results in 1 function
    axios.get(`http://127.0.0.1:5000/api/friends/all`)
    .then((response) => {  
  
    var friend = response.data;
    var tagline = "Here is the data coming from my own API";

    //use res.render to load up an ejs view file
    res.render('pages/moviedelete', {
        user: friend,
        tagline: tagline,
    });
    })
    .catch(error => console.log(error)); 
});



//MOVIE POINTS END
//  takes the data from teh add movies 
app.post('/processdynamicform', function(req, res){
    //go directly to thanks.ejs and show dynamic checkbox selection
    console.log(JSON.stringify(req.body))
    for (x in req.body) {
        var selectedName = x;
        console.log("selected name is: " + selectedName);
    }
    fetch('http://127.0.0.1:5000/api/movies/add', { method: 'POST', headers: {'Content-Type':'application/json; charset=utf-8'}, body: JSON.stringify(req.body)})
    .then(function (res) {
        return res.text();
      })
    .then(data => console.log(data))
    .then(data => console.log(JSON.stringify(req.body)))
    .catch(error => console.log('ERROR'))
    res.render('pages/thanks.ejs', {body: req.body})
  
});

app.listen(8080);
console.log('8080 is the magic port');
