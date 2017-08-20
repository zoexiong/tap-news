import express from 'express';
const app = express();

import cors from 'cors';

import bodyParser from 'body-parser';

// import mongoose from 'mongoose';

// Middleware!
app.use(cors());
app.use(bodyParser.urlencoded({ extended: false }));  //parse form
app.use(bodyParser.json()); //parse json
console.log(__dirname);
app.use(express.static(__dirname + '/public'));

// Api
app.get('/api/bittiger', (req, res) => {
    res.status(200).send(`hit: /api/bittiger`);
});

app.get('/api/bittiger/params_find/:courseID', (req, res) => {
    res.json( { courseID : req.params.courseID } );
});

app.get('/api/bittiger/query_find', (req, res) => {
    res.json( { courseID : req.query.courseID } );
});

app.post('/api/bittiger/addCourse', (req, res) => {
    res.json({ addedCourse: req.body.courseID });
});

// Error handler
app.use((err, req, res, next) => {
    if(err) {
        res.status(err.status || 500).send(err.message);
    }
    else {
        next();
    }
});

const serverPort = process.env.SERVER_PORT || 3001;
app.listen(serverPort, () => {
    console.log(`listening port ${serverPort}`);
});
