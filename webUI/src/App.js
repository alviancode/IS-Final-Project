import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useEffect, useState } from 'react';
import { Switch, Route, BrowserRouter } from 'react-router-dom';
import { Search } from './Search'
import { NavBar } from './NavBar'


function GalleryAllBest() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    fetchItems();
  }, []);

  const fetchItems = async () => {
    const data = await fetch("/allbest", {
      method: "get",
      headers: {
        "Content-Type": "application/json"
      },
    });
    const items = await data.json();
    setItems(items.movies);
  }

  return (
    <div>
      <div className="container-md  mt-5">
        <h3>All-time Popular</h3>
        <div className="row">
          {items.map(item => (
            <div className="col-md-2" key={item.index}>
              <div className="card card-style bg-dark text-white mb-2" >
                <img src={item.poster} className="card-img-top image-style" />
                <div className="card-body">
                  <p className="card-title"><small><strong>{item.title}</strong></small></p>
                </div>
                <button className="btn btn-sm btn-outline-light" onClick={
                  () => localStorage.setItem("watched", item.title)
                }>Watch</button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}


function GalleryRecommend() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    fetchItems();
  }, []);

  const fetchItems = async () => {
    const data = await fetch("/recommend", {
      method: "get",
      headers: {
        "Content-Type": "application/json",
        "watched": localStorage.getItem("watched")
      },
    });
    const items = await data.json();
    setItems(items.movies);
  }

  return (
    <div>
      <div className="container-md  mt-5">
        <h3>Because you have watched {localStorage.getItem("watched")}</h3>
        <div className="row">
          {items.map(item => (
            <div className="col-md-2" key={item.index}>
              <div className="card card-style bg-dark text-white mb-2" >
                <img src={item.poster} className="card-img-top image-style" />
                <div className="card-body">
                  <p className="card-title"><small><strong>{item.title}</strong></small></p>
                </div>
                <button className="btn btn-sm btn-outline-light" onClick={
                  () => localStorage.setItem("watched", item.title)
                }>Watch</button>
              </div>
            </div>
          ))}
        </div>
      </div>
      {GalleryAllBest()}
    </div>
  );
}


function App() {
  return (
    <div>
      <NavBar />
      <Switch>
        <Route path="/" exact component={localStorage.getItem("watched") != null
          ?
          GalleryRecommend
          :
          GalleryAllBest
        } />
        <Route path="/search/:title" component={Search} />
        <Search />
      </Switch>
    </div>
  );
}

export default App;
