const express = require('express');
const mongoose = require('mongoose');
const path = require('path');

const app = express();
const port = 3020;

// Middleware
app.use(express.urlencoded({ extended: true })); // Parse form data
app.use(express.static(path.join(__dirname))); // Serve static files

// MongoDB Connection
mongoose.connect('mongodb://127.0.0.1:27017/students', {
    useNewUrlParser: true,
    useUnifiedTopology: true,
});

const db = mongoose.connection;
db.on('error', console.error.bind(console, 'MongoDB connection error:'));
db.once('open', () => {
    console.log('Connected to MongoDB successfully');
});

// Schema and Model
const userSchema = new mongoose.Schema({
    roll_no: { type: String, required: true },
    name: { type: String, required: true },
    gender: { type: String, required: true },
    dob: { type: Date, required: true },
    address: { type: String, required: true },
    city: { type: String, required: true },
    pincode: { type: String, required: true },
    district: { type: String, required: true },
    father_name: { type: String, required: true },
    father_phone: { type: String, required: true },
    father_occupation: { type: String, required: true },
    mother_name: { type: String, required: true },
    mother_phone: { type: String, required: true },
    mother_occupation: { type: String, required: true },
    religion: { type: String, required: true },
    mother_tongue: { type: String, required: true },
});

const User = mongoose.model('User', userSchema);

// Routes
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'form.html'));
});

app.post('/post', async (req, res) => {
    try {
        const newUser = new User(req.body);
        await newUser.save();

        console.log('Data saved:', newUser);
        res.sendFile(path.join(__dirname, 'dashboard.html'));
    } catch (error) {
        console.error('Error saving data:', error);
        res.status(500).send('Failed to save data.');
    }
});

app.get('/dashboard', (req, res) => {
    res.sendFile(path.join(__dirname, 'dashboard.html'));
});

// Start the server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
