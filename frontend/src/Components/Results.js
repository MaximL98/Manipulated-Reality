import React, { useEffect, useState } from "react";

function Results() {
    const [data, setData] = useState("");

    useEffect(() => {
        fetch("/api/upload")
            .then(res => res.json())
            .then(data => setData(data)); // Update entire data state
    }, []);

    return (
        <div>
            <h1>{data}</h1>
            <h2>Results</h2>
        </div>
    );
}

export default Results;