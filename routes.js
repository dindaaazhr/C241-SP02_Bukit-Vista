const Path = require("path");
const handler = require("./services/handler.js");

const routes = [
  {
    method: "GET",
    path: "/",
    handler: (request, h) => {
      return h.file(Path.join(__dirname, "templates", "index.html"));
    },
  },
  {
    method: "GET",
    path: "/static/{param*}",
    handler: {
      directory: {
        path: Path.join(__dirname, "static"),
        index: false,
      },
    },
  },
  {
    method: "POST",
    path: "/predict",
    handler: handler.predict,
  },
];

module.exports = routes;
