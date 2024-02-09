const express=require('express');
const bodyParser = require('body-parser');
const mysql=require("mysql2")
const {spawn} = require('child_process');
const multer = require('multer');
const path = require('path');


const app=express();


app.use(express.static(__dirname+'/assets'));
app.set('view engine', 'ejs')
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({
    extended:false
}));


// Set up Multer storage
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
      // Set the destination folder where the uploaded file will be stored
      cb(null, 'uploads/');
    },
    filename: function (req, file, cb) {
      // Set the filename for the uploaded file
      cb(null, file.fieldname +  path.extname(file.originalname));
    }
  });

// Create a Multer instance with the storage configuration
const upload = multer({ storage: storage });






app.get("/",function(req,res){
    res.sendFile(__dirname+"/views/homepage.html")
})

app.post('/csvUpload', upload.single('myCSV'), async function (req, res) {
    const filePath = req.file.path;
  
    try {
      // Use async/await to wait for the child process to finish
      const python = spawn('python3', ['python-work/parseData.py', filePath]);
  
      // Collect data from script
      const dataToSend = await new Promise((resolve, reject) => {
        let dataBuffer = '';
  
        python.stdout.on('data', function (data) {
          console.log('Pipe data from python script ...');
          dataBuffer += data.toString();
        });
  
        python.on('close', (code) => {
          console.log(`child process close all stdio with code ${code}`);
          resolve(dataBuffer);
        });
  
        python.on('error', (err) => {
          console.error(`Error in child process: ${err}`);
          reject(err);
        });
      });
  
      console.log(dataToSend);
  
      // You can send the response or perform additional actions here
      res.sendFile(__dirname+"/views/query.html");
    } 
    
    
    catch (error) {
      console.error(`Error during file processing: ${error}`);
      res.status(500).send('Internal Server Error');
    }

  });


app.post("/query",async function(req,res){
  const type=req.body.type;
  const input=req.body.input;
  console.log(type,input);


  try {
    // Use async/await to wait for the child process to finish
    const python_new = spawn('python3', ['python-work/main-wrok.py', type, input]);

    // Collect data from script
    const dataToSend = await new Promise((resolve, reject) => {
      let dataBuffer = '';

      python_new.stdout.on('data', function (data) {
        console.log('Pipe data from python script ...');
        dataBuffer += data.toString();
      });

      python_new.on('close', (code) => {
        console.log(`child process close all stdio with code ${code}`);
        resolve(dataBuffer);
      });

      python_new.on('error', (err) => {
        console.error(`Error in child process: ${err}`);
        reject(err);
      });
    });

    console.log(dataToSend);
    // You can send the response or perform additional actions here
    res.render("requery",{type:type,queryResponse:dataToSend});
  } 

  catch (error) {
    console.error(`Error during searching: ${error}`);
    res.status(500).send('Internal Server Error');
  }
  

})
  


app.listen(3003,function(){
    console.log("Server started on port 3003");
});
