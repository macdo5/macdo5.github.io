// requires nodejs and npm to connect to Mongo.
// >npm install mongodb
var MongoClient = require('mongodb').MongoClient;
var assert = require('assert');
var ObjectId = require('mongodb').ObjectID;
var url = "mongodb://10.118.0.84:27017/local";

var findTest = function(db, callback) {
  var cursor =db.collection('startup_log').find( );
  cursor.each(function(err, doc) {
     assert.equal(err, null);
     if (doc != null) {
        console.dir(doc);
     } else {
        callback();
     }
  });
};

MongoClient.connect(url, function(err, db) {
  assert.equal(null, err);
  findTest(db, function() {
      db.close();
  });
});