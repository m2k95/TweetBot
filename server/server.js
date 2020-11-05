const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
const serveIndex = require('serve-index');
const app = express();
const logsPath = path.join(__dirname, '../logs/');

app.use(cors());
app.use('/', express.static('public'))
app.use('/logs', serveIndex(logsPath));

app.use('/logs', (req, res) => {
    var fullURL = req.protocol + '://' + req.get('host') + req.originalUrl;
    var r = fullURL.split('/').reverse();

    fs.readFile(`../logs/${r[0]}`, 'utf8', (e, data) => {
        if (e) throw e;
        res.setHeader('Content-type', 'application/json');
        res.send(data.toString());
    });
});

app.listen(3000, () => {
    console.log('Server started at port http://0.0.0.0:3000');
});
