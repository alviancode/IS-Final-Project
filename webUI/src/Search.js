import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom'

function Gallery(link) {
  const [items, setItems] = useState([]);

  useEffect(() => {
    fetchItems();
  }, []);

  const fetchItems = async () => {
    const data = await fetch(link, {
      method: "GET",
      headers: {
        "Content-Type": "application/json"
      },
    });
    const items = await data.json();
    setItems(items.movies);
  }



  return (
    <div>
      <div className="container-md">
        <div className="row mt-5">
          {items.map(item => (
            <div className="col-md-2" key={item.index}>
              <div className="card card-style bg-dark text-white mb-2" >
                <img src={item.poster} className="card-img-top image-style" />
                <div className="card-body">
                  <p className="card-title"><small><strong>
                    {item.title} </strong></small></p>
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






export function Search() {
  const { title } = useParams();
  return (
    <div>
      {Gallery(`/search/${title}`)}

    </div>
  );
}

export default Search;
