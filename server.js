"use strict";

const Hapi = require("@hapi/hapi");
const Inert = require("@hapi/inert");
const routes = require("./routes");
const Path = require("path");
const Nunjucks = require("nunjucks");

const init = async () => {
  const server = Hapi.server({
    port: process.env.PORT,
    host: '0.0.0.0',
    routes: {
      cors: {
        origin: ["*"],
      },
    },
  });
  
  Nunjucks.configure(Path.join(__dirname, "templates"), {
    autoescape: true,
    noCache: true,
  }).addGlobal('hideValues', true);

  await server.register(Inert);

  server.route(routes);

  await server.start();
  console.log(`Server berjalan pada ${server.info.uri}`);
};
process.on('unhandledRejection', (err) => {
    console.log(err);
});

init();
