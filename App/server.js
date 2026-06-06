const express = require("express");
const fs = require("fs");

const app = express();

app.use(express.json());
app.use(express.static("public"));

app.post("/login", (req, res) => {
    const { email, password } = req.body;

    const users = JSON.parse(
        fs.readFileSync("users.json", "utf8")
    );

    const user = users.find(
        u => u.email === email && u.password === password
    );

    if (user) {
        res.json({
            success: true,
            redirect: "/dashboard.html"
        });
    } else {
        res.json({
            success: false,
            message: "Invalid email or password"
        });
    }
});

app.listen(3000, () => {
    console.log("Server running on http://localhost:3000");
});