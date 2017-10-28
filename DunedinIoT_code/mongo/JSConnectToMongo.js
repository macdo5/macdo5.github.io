// requires nodejs and npm to connect to Mongo.
// >npm install mongodb
var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://localhost:27017/duniot_database";

MongoClient.connect(url, function(err, db) {
  if (err) throw err;
  db.node_data.find().toArray(function(err, result) {
    if (err) throw err;
    console.log(result);
    db.close();
  });
});