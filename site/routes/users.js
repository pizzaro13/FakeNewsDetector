var express = require('express');
var router = express.Router();
var db = require('../db');

/* GET users listing. */
router.get('/', function(req, res, next) {

    return db.User.findOne(
        {
            where: {
                name: req.query.name
            }
        }
    ).then((user) => {
        if (!user) {
            res.status(404).json({ error: "Not Found" });
        }

        return res.json(user);
    }).catch((err) => {
        res.status(404).json({ error: "Not Found" });
    });

  res.send('respond with a resource');
});

router.post('/', function(req, res, next) {
    const { name, style } = req.body;

    return db.User.find({where: { name }}).then(user => {
        if (user) {
            return res.status(400).json({ error: "User exist" });
        }

        db.User.create(
            {
                name,
                style
            }
        ).then( newuser => {
            return res.json(newuser);
        }).catch( err => {
            return res.status(404).json({ error: err });
        })
    }).catch( (err) => {
        return res.status(400).json({ error: err });
    });
    // post a user with info
});

module.exports = router;
