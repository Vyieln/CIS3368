// load the things we need
var express = require('express');
var app = express();
const bodyParser  = require('body-parser');
const fetch = require("node-fetch");

app.use(express.static("public"));

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

app.get('/user', function(req, res){
    var tagline = "Add Users! Enter Movies! Receive your random pick!";
    res.render('pages/user',
    {
        tagline: tagline
    });

});

// about page
app.get('/about', function(req, res) {
    res.render('pages/about');
});

// examples page 
app.get('/examples', function(req, res) {
    // this will render our new example spage 
    res.render("pages/examples");
});
app.get('/test', function(req, res) {
    // this will render our new example spage 
    res.render("pages/test");
});

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
  
  })

app.listen(8080);
console.log('8080 is the magic port');
