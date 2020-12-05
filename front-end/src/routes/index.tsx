import React from "react";
import { Switch } from "react-router-dom";

import SignIn from "../pages/SignIn";
import SignUp from "../pages/SignUp";
import Genres from "../pages/Genres";
import Bands from "../pages/Bands";
import Albums from "../pages/Albums";

import Route from "./Route";

const Routes: React.FC = () => (
  <Switch>
    <Route path="/" exact isPrivate component={Genres} />
    <Route path="/bands/:genre_id" exact isPrivate component={Bands} />
    <Route path="/albums/:band_id" exact isPrivate component={Albums} />
    <Route path="/signin" exact component={SignIn} />
    <Route path="/signup" exact component={SignUp} />
  </Switch>
);

export default Routes;
