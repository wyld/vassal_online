var App = require('./App');
var Home = require('./Home');
var React = require('react');
var Router = require('react-router');
var {DefaultRoute, Route, Routes} = Router;

var routes = (
    <Route name="app" path="/" handler={App}>
        <DefaultRoute name="home" handler={Home} />
    </Route>
);

Router.run(routes, Router.HistoryLocation, function(Handler) {
    React.render(<Handler/>, document.body);
});
