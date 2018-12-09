var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Myriam' });
});

/* GET Hello World page. */
router.get('/helloworld', function(req, res) {
  res.render('helloworld', { title: 'Hello, World!' });
});

/* GET Userlist page. */
router.get('/userlist', function(req, res) {
  var db = req.db;
  var users = db.get('usercollection');
  users.find({}).each((user, {close, pause, resume}) => {
      console.log(user);
      res.render('userlist', {
          "user" : user
      }).then(() => {
        console.log("No more users");
      });
  });
});

module.exports = router;
