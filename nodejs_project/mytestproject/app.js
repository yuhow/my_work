// import module
var express = require('express');
var path = require('path');
var multer = require('multer');
var mongo = require('mongodb');
var monk = require('monk');

// Connect to MongoDB
var db = monk('localhost:27017/mytestproject'); //port27017 is the default port of MongoDB
var upload = multer({dest: './uploads/'});

// router
var routes = require('./routes/index');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'hjs');

// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(require('less-middleware')(path.join(__dirname, 'public')));
app.use(express.static(path.join(__dirname, 'public')));

// Allow router to access db
app.use(function(req, res, next){
    req.db = db;
    next();
});
 
app.use('/', routes);

// Uploade files
 // format of time
function zeroFill(i) {
    return (i < 10 ? '0' : '') + i;
}

var newFileInfo = {};

app.use(multer({dest: './uploads/',
    rename: function(fieldname, filename) {
        var date = new Date();
        return filename + '_'
                        + date.getFullYear()
                        + zeroFill(date.getMonth() + 1)
                        + zeroFill(date.getDate())
                        + zeroFill(date.getHours())
                        + zeroFill(date.getMinutes());
    },
    onFileUploadStart: function(file) {
        newFileInfo = file;
        console.log(file.originalname + ' is starting ...');
    },
    onFileUploadComplete: function(file) {
        console.log(file.fieldname + ' uploaded to ' + file.path);
    }
}));

app.get('/', function(req, res){
    res.sendFile(__dirname + '/views/index.hjs');
});

app.post('/', function(req, res){
    upload(req, res, function(err) {
        // Set our internal DB variable
        var db = req.db;
        
        // Get our form values. These rely on the "name" attributes
        var fieldName = newFileInfo.fieldname;
        var originalName = newFileInfo.originalname;
        var Name = newFileInfo.name;
        var Path = newFileInfo.path;
        var Extension = newFileInfo.extension;
        var Size = newFileInfo.size;
                         
        // Set our collection
        var collection = db.get('filecollection');
                             
        // Submit to the DB
        collection.insert({  
            "fieldname" : fieldName,
            "originalname" : originalName,
            "name" : Name,
            "path" : Path,
            "extension" : Extension,
            "size" : Size
        }, function (err, doc) {
            if (err) {
                // If it failed, return error
                res.send("There was a problem adding the information to the database.");
            }
            //else {
            //    // If it worked, set the header so the address bar doesn't still say /adduser
            //    res.location("back");
            //    // And forward to success page
            //    res.redirect("back");
            //}
        });

        if(err) {
            return res.end('Error uploading file.');
        }
        res.location("back");
        res.redirect("back");
    });
});

// error handlers
// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
  app.use(function(err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
      message: err.message,
      error: err
    });
  });
}

// production error handler
// no stacktraces leaked to user
app.use(function(err, req, res, next) {
  res.status(err.status || 500);
  res.render('error', {
    message: err.message,
    error: {}
  });
});


module.exports = app;
