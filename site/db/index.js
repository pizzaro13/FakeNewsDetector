const fs = require('fs'),
    path = require('path'),
    nconf = require('nconf'),
    dbinfo = nconf.get('dbinfo')
    Sequelize = require('sequelize'),
    sequelize = new Sequelize({
        dialect: 'sqlite',
        storage: 'db.sqlite'
    });
    db = {};

sequelize
    .authenticate()
    .then(function() {
        console.log("Sequelize authenticated");
        return;
    })
    .catch((err) => {
        console.log("err in sequelize authenticate");
        throw Error(err);
    });

fs
    .readdirSync(__dirname)
    .filter(function(file) {
        return (file.indexOf('.') !== 0) && (file !== 'index.js');
    })
    .forEach(function(file) {
        const model = sequelize.import(path.join(__dirname, file));
        db[model.name] = model;
    });

Object.keys(db).forEach(function(modelName) {
  if ("associate" in db[modelName]) {
    db[modelName].associate(db);
  }
});

db.sequelize = sequelize;
db.Sequelize = Sequelize;

module.exports = db;
