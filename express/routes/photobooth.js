/**
 * GET photobooth status.
 */

exports.status = function(req, res, value) {
    res.setHeader('Content-Type', 'application/json');
    res.send(JSON.stringify({ status: value}));
};
