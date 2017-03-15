module.exports = {
    "env": {
        "browser": true,
        "jquery": true
    },
    "extends": "eslint:recommended",
    "globals": {
        "_": true,
        "crs_id": true,
        "Backbone": true,
        "deepEqual": true,
        "equal": true,
        "module": true,
        "test": true
    },
    "rules": {
        "indent": [
            "error",
            4
        ],
        "linebreak-style": [
            "error",
            "unix"
        ],
        "no-unused-vars": [
            "error",
            {"vars": "all", "args": "none"}
        ],
        "quotes": [
            "error",
            "single"
        ],
        "semi": [
            "error",
            "always"
        ]
    }
};
