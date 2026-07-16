import { useEffect, useState } from "react";

function App() {

  const [about, setAbout] = useState(null);

  useEffect(() => {

    fetch("http://127.0.0.1:8000/about")
      .then((response) => response.json())
      .then((data) => {
        setAbout(data);
      });

  }, []);

  if (!about) {

    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-950 text-white text-2xl">
        Loading...
      </div>
    );

  }

  return (

    <div className="min-h-screen bg-slate-950 text-white">

      <div className="max-w-5xl mx-auto py-20">

        <h1 className="text-6xl font-bold">
          {about.name}
        </h1>

        <h2 className="text-2xl text-blue-400 mt-5">
          {about.title}
        </h2>

        <p className="text-gray-400 mt-3">
          📍 {about.location}
        </p>

        <p className="mt-10 text-lg leading-8 text-gray-300">
          {about.description}
        </p>

      </div>

    </div>

  );

}

export default App;