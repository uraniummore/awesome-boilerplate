require("./config/dotenv");
const express = require("express");
const next = require("next");
const nextI18NextMiddleware = require("next-i18next/middleware").default;

const i18n = require("./src/i18n");
const RoutesPrettifier = require("./src/routes/urlPrettifier").Router;
const serverEndpoints = require("./src/routes/serverEndpoints").default;

const port = process.env.PORT || 3000;
const dev = process.env.NODE_ENV !== "production";
const app = next({
    dev,
    dir: "./src",
});
const requestHandler = app.getRequestHandler();

app.prepare().then(async () => {
    const server = express();

    server.use(serverEndpoints);

    await i18n.initPromise;
    server.use(nextI18NextMiddleware(i18n));

    RoutesPrettifier.forEachPrettyPattern((page, pattern, defaultParams) => server.get(pattern, (req, res) => {
        app.render(
            req,
            res,
            `/${page}`,
            Object.assign(
                {},
                defaultParams,
                req.query,
                req.params
            )
        );
    }));

    server.get("*", (req, res) => requestHandler(req, res));

    server.listen(port);
    console.log(`> Ready on http://localhost:${port}`);
});
