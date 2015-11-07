var fs = require('fs');
var express = require('express');
var router = express.Router();

router.get('/', function(req, res, next) {
    var db = req.db;
    var collection = db.get('filecollection');
    collection.find({}, {}, function(e, docs) {
        var name = [];
        var objkey = Object.keys(docs);
        objkey.forEach(function(objectid) {
            var items = Object.keys(docs[objectid]);
            items.forEach(function(itemkey) {
                var itemvalue = docs[objectid][itemkey];
                console.log(objectid + ': ' + itemkey + ' = ' + itemvalue);
                if (itemkey == "name") {
                    name.push(itemvalue);
                }
            })
        })
        console.log(name);
        res.render('index', {
            "fileNameList" : name,
        });
    });
});

router.get('/:file(*)', function(req, res, next){ // this routes all types of file
    var path = require('path');
    var file = req.params.file;
    var path = path.resolve(".")+'/uploads/'+file;

     res.download(path); // magic of download fuction
});

module.exports = router;
