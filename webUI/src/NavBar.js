import 'bootstrap/dist/css/bootstrap.min.css';

export function NavBar() {


    function searchMovie(title) {
        console.log(title)
        const { href } = window.location;
        window.location.href = `/search/${title}`;
    }

    return (
        <div className="container-fluid pb-5">
            <nav className="navbar navbar-expand-sm navbar-dark bg-dark fixed-top">
                <div className="container-fluid">
                    <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#collapse_target" aria-expanded="false" aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon"></span>
                    </button>
                    <div className="collapse navbar-collapse" id="collapse_target">
                        <form className="mx-auto d-inline w-50 mt-1 mb-1"
                            onSubmit={(e) => {
                                e.preventDefault()
                                searchMovie(e.target[0].value)
                            }}>
                            <input type="text" className="form-control" placeholder="Search Movie" />
                        </form>
                    </div>
                </div>
            </nav>
        </div>
    );
}

export default NavBar;