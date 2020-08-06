const tesseract = require('tesseractocr')
const path = require('path')
var fs = require('fs')
var file = process.argv[2]

tesseract.recognize(file, (err, text) => {console.log(text)} )

exports.handle = function(request, respond) {
    text = new Promise((resolve, reject) => {
        let text = recognize('pitontable.jpg', (err, text) => {
	    if (err) {
                var response = {
                    statusCode: 500,
                    body: "Error!"
                };
			console.log('error')
	        resolve(response);
	    } else {
                var response = {
                    statusCode: 200,
                    body: text
                };
	        resolve(response);
			console.log('success')
	    }
	});
    });
    return text;
}
