module.exports = function(sequelize, DataTypes) {
    var User = sequelize.define('User', {
        name: { // not sure if it is name or username
            type: DataTypes.STRING,
            unique: true,
            validate: {
                notEmpty: true
            }
        },
        style: {
            type: DataTypes.STRING,
            validate: {
                notEmpty: true
            }
        }
    }, {
        dialect: 'sqlite'
    });

    return User;
};
