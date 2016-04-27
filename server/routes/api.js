var request = require("request");

module.exports = function(app, express) {

	var apiRouter = express.Router();

	// route to generate sample user
	apiRouter.get('/getAIMove', function(req, res) {
    console.log("hit")
    request({
        uri: "http://127.0.0.1:5000/getAIMove",
        method: "GET",
				json: req.body,
        timeout: 10000
      }, function(error, response, body) {
      console.log(body);
      // return the information  as JSON
      res.json({
        board: body
      });
	  });
	});

	// route to generate sample user
	apiRouter.get('/getBoard', function(req, res) {
    request({
        uri: "http://127.0.0.1:5000/getBoard",
        method: "GET",
				json: req.body,
        timeout: 10000
      }, function(error, response, body) {
      res.json({
        board: body
      });
    });
	});

	// route verify move
	apiRouter.post('/verify', function(req, res) {

    console.log(req.body);

    request({
        uri: "http://127.0.0.1:5000/verify",
        method: "POST",
        json: req.body,
        timeout: 10000
      }, function(error, response, body) {
	      // return the information  as JSON
				res.json({
	        works: body
	      });
	    });
		});

	return apiRouter;
};
