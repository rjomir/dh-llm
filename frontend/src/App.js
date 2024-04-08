import React from 'react';
import { Layout } from "./components/Layout"
import { Home } from "./components/Home"
import { Fallback } from "./components/Fallback"
import { Benchmarks } from "./components/Benchmarks"
import { Settings } from "./components/Settings"

import {
  RouterProvider,
  createBrowserRouter
} from "react-router-dom";

import 'primereact/resources/themes/mdc-light-indigo/theme.css';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
import 'primeflex/primeflex.css';

function App() {
    let router = createBrowserRouter([
      {
        path: "/",
        Component: Layout,
        children: [
          {
            index: true,
            Component: Home,
          },
          {
            path: "benchmarks",
            Component: Benchmarks,
          },
          {
            path: "settings",
            Component: Settings,
          },
        ],
      },
    ]);

    return <RouterProvider router={router} fallbackElement={<Fallback />} />;

}

export default App;
