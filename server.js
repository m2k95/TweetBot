const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
const serveIndex = require('serve-index');
const app = express();
const logsPath = path.join(__dirname, 'logs/');

app.use(cors());
app.use(express.static('public'))

app.get('/', (req, res) => {
    res.json({
        message: "Hello Wolrd!"
    })
})

app.use('/logs', serveIndex(logsPath));

app.use('/logs', (req, res) => {
    var fullURL = req.protocol + '://' + req.get('host') + req.originalUrl;
    var r = fullURL.split('/').reverse();

    fs.readFile(`./logs/${r[1]}/${r[0]}`, (e, data) => {
        if (e) throw e;
        res.send(data.toString());
    });
});

app.listen(3000, () => {
    console.log('Server started at port http://0.0.0.0:3000');
});