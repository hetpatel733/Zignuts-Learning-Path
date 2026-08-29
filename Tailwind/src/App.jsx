import { useState } from "react";
import "./App.css";
import "./index.css";

function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <div className="grid place-content-center">
        <h1 className="text-4xl text-white text-center mb-5">Tailwind Trial</h1>
        <div className="p-3 max-w-sm mx-auto bg-white rounded-3xl shadow-2xl flex items-center">
          <div className="m-4">
            <div>
              <img
                className="rounded-2xl"
                src="https://picsum.photos/75"
                alt=""
              />
            </div>
          </div>
          <div>
            <div className="text-3xl font-medium">
              Het Patel
              <p className="text-base text-slate-600">is learning Tailwind</p>
            </div>
          </div>
        </div>
        <button className="bg-green-700 p-2 mt-4 rounded-xl text-base text-white hover:bg-green-900">
          Click Me
        </button>
        <div className="text-center my-4">
          <p className="text-white sm:text-green-700 md:text-yellow-300">
            Lorem, ipsum dolor.
          </p>
        </div>
        <div>
          <div className="max-w-sm mx-auto bg-white rounded-xl md:max-w-2xl overflow-hidden">
            <div className="md:flex">
              <div>
                <img
                  className="h-48 w-full object-cover md:h-full md:w-48"
                  src="https://images.pexels.com/photos/38440480/pexels-photo-38440480.jpeg"
                  alt=""
                />
              </div>
              <div className="p-5 text-indigo-500 text-center">Content</div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default App;
