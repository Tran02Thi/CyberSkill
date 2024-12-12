const express = require('express')
const app = express()
const port = 8000


app.get('/', (req, res) => {
	res.send('Hello World Cyberskill')
})

app.get('/user', (req, res) => {
	res.send('Tran Thi')
})

app.listen(port, () => {
 	console.log("Listening on port 4000 ...")//
})
