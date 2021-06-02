import React, { useEffect, useState } from 'react';


export function Gallery(link = "/search") {
    const [items, setItems] = useState([]);

    useEffect(() => {
        fetchItems();
    }, []);

    const fetchItems = async () => {
        const data = await fetch(link, {
            method: "get",
            headers: {
                "Content-Type": "application/json",
                "title": "killer"
            },
        });
        const items = await data.json();
        setItems(items);
        console.log("HEHEHE", items)
    }



    return (
        <div className="body-color"> Hi udh ke load
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
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default Gallery;
