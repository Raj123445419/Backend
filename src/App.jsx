import { Routes, Route } from "react-router-dom";

import "./App.css";

import Employ_list from "./components/Employ_list";
import Edite_Page from "./components/Edite_Page";
import Employ_attendance from "./components/Employ_attendance";
import Edite_attendance from "./components/Edite_attendance";
import Employ_Sallery from "./components/Employ_Sallery";

function App() {

  return (

    <Routes>

      <Route
        path="/"
        element={<Employ_list />}
      />

      <Route
        path="/edit"
        element={<Edite_Page />}
      />

      <Route
        path="/attendance"
        element={<Employ_attendance />}
      />

      <Route
        path="/edit-attendance/:id"
        element={<Edite_attendance />}
      />

      <Route
        path="/salary"
        element={<Employ_Sallery />}
      />

    </Routes>

  );

}

export default App;