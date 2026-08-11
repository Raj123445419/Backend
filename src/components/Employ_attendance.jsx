
import React, { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";

// =====================================================
// DJANGO BACKEND URL
// =====================================================
const API_URL = "https://backend-z4sf.onrender.com";

// =====================================================
// EMPLOYEE ATTENDANCE COMPONENT
// =====================================================

const Employ_attendance = () => {

  const navigate = useNavigate();

  const [attendance, setAttendance] = useState([]);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");

  const [formData, setFormData] = useState({
    EmployId: "",
    Date: "",
    Status: ""
  });

  // ================= GET ATTENDANCE =================

  const getAttendance = async () => {

    try {

      setLoading(true);

      const response = await fetch(
        `${API_URL}/Employ_attendance/`,
        {
          method: "GET",

          headers: {
            "Accept": "application/json"
          }
        }
      );

      if (!response.ok) {

        throw new Error(
          "Failed to fetch attendance"
        );

      }

      const data = await response.json();

      console.log(
        "Attendance from Django:",
        data
      );

      setAttendance(data);

    } catch (error) {

      console.log(error);

      setError(
        "Failed to load attendance"
      );

    } finally {

      setLoading(false);

    }

  };

  useEffect(() => {

    getAttendance();

  }, []);

  // ================= INPUT CHANGE =================

  const handleChange = (e) => {

    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });

  };

  // ================= SAVE ATTENDANCE =================

  const handleSubmit = async (e) => {

    e.preventDefault();

    setError("");

    try {

      const response = await fetch(
        `${API_URL}/Employ_attendance/`,
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/x-www-form-urlencoded",

            "Accept":
              "application/json"
          },

          body: new URLSearchParams(formData)
        }
      );

      if (response.ok) {

        alert(
          "Attendance Saved Successfully"
        );

        setFormData({
          EmployId: "",
          Date: "",
          Status: ""
        });

        getAttendance();

      } else {

        let data = {};

        try {

          data = await response.json();

        } catch {

          // Response JSON nahi hai

        }

        alert(
          data.error ||
          "Attendance Save Failed"
        );

      }

    } catch (error) {

      console.log(error);

      alert(
        "Backend connection error"
      );

    }

  };

  // ================= RESET =================

  const handleReset = () => {

    setFormData({
      EmployId: "",
      Date: "",
      Status: ""
    });

    setError("");

  };

  // ================= EDIT =================

  const handleEdit = (item) => {

    navigate(`/edit-attendance/${item.id}`, {
      state: {
        attendance: item
      }
    });

  };

  // ================= DELETE =================

  const handleDelete = async (id) => {

    const confirmDelete =
      window.confirm(
        "Are you sure you want to delete this attendance?"
      );

    if (!confirmDelete) {

      return;

    }

    try {

      const response = await fetch(
        `${API_URL}/Delete_attendance/${id}/`,
        {
          method: "DELETE",

          headers: {
            "Accept":
              "application/json"
          }
        }
      );

      if (response.ok) {

        alert(
          "Attendance Deleted Successfully"
        );

        getAttendance();

      } else {

        let data = {};

        try {

          data = await response.json();

        } catch {

          // Response JSON nahi hai

        }

        alert(
          data.error ||
          "Delete Failed"
        );

      }

    } catch (error) {

      console.log(error);

      alert(
        "Backend connection error"
      );

    }

  };



  return (
    <>

      {/* =====================================================
          NAVBAR
      ====================================================== */}
<div className="all">
      <nav className="navbar navbar-expand-sm">

        <div className="container-fluid">

          <Link
            className="navbar-brand fontnav px-2 px-md-3 cl1"
            to="/"
          >
            Employ Management System
          </Link>

          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#collapsibleNavbar"
          >

            <span className="navbar-toggler-icon"></span>

          </button>

          <div
            className="collapse navbar-collapse"
            id="collapsibleNavbar"
          >

            <ul className="navbar-nav ms-auto">

              {/* Employ List */}

              <li className="nav-item">

                <Link
                  className="nav-link px-2 px-md-3 cl1"
                  to="/"
                >
                  Employ List
                </Link>

              </li>

              {/* Employ Attendance */}

              <li className="nav-item">

                <Link
                  className="nav-link px-2 px-md-3 cl1"
                  to="/attendance"
                >
                  Employ Attendance
                </Link>

              </li>

              {/* Employ Salary */}

              <li className="nav-item">

                <Link
                  className="nav-link px-2 px-md-3 cl1"
                  to="/salary"
                >
                  Employ Sallery Count
                </Link>

              </li>

            </ul>

          </div>

        </div>

      </nav>
</div>
      {/* =====================================================
          MAIN CONTAINER
      ====================================================== */}

      <div className="container alltext">

        <div className="col-md-12 text-dark mt-5">

          <h1 className="text-center">
            Employee Attendance
          </h1>

        </div>

        {/* ================= ATTENDANCE FORM ================= */}

        <div className="card mt-5">

          <div className="card-body">

            <form onSubmit={handleSubmit}>

              <div className="container mt-4">

                <div className="card shadow">

                  <div className="card-body">

                    <div className="row">

                      {/* EMPLOYEE ID */}

                      <div className="col-md-6 mb-3">

                        <label className="form-label">
                          Employee ID
                        </label>

                        <input
                          type="number"
                          name="EmployId"
                          className="form-control"
                          placeholder="Enter Employee ID"
                          value={formData.EmployId}
                          onChange={handleChange}
                          required
                        />

                      </div>

                      {/* DATE */}

                      <div className="col-md-6 mb-3">

                        <label className="form-label">
                          Attendance Date
                        </label>

                        <input
                          type="date"
                          name="Date"
                          className="form-control"
                          value={formData.Date}
                          onChange={handleChange}
                          required
                        />

                      </div>

                      {/* STATUS */}

                      <div className="col-md-6 mb-3">

                        <label className="form-label">
                          Attendance Status
                        </label>

                        <select
                          name="Status"
                          className="form-select"
                          value={formData.Status}
                          onChange={handleChange}
                          required
                        >

                          <option value="">
                            Select Status
                          </option>

                          <option value="Present">
                            Present
                          </option>

                          <option value="Absent">
                            Absent
                          </option>

                          <option value="Half Day">
                            Half Day
                          </option>

                        </select>

                      </div>

                    </div>

                  </div>

                  {/* ================= FOOTER BUTTONS ================= */}

                  <div className="card-footer text-center">

                    <button
                      type="submit"
                      className="btn btn-save me-2"
                    >
                      Save Attendance
                    </button>

                    <button
                      type="button"
                      className="btn btn-reset"
                      onClick={handleReset}
                    >
                      Reset
                    </button>

                  </div>

                </div>

              </div>

            </form>

          </div>

        </div>

        {/* ================= ERROR ================= */}

        {error && (

          <div className="alert alert-danger mt-3 text-center">

            {error}

          </div>

        )}

        {/* ================= ATTENDANCE LIST ================= */}

        <div className="card mt-4">

          <div className="card-header">

            <h4>
              Attendance List
            </h4>

          </div>

          <div className="card-body">

            <div className="attendance-table-box">

              <table className="table table-bordered table-striped attendance-table">

                <thead>

                  <tr className="table-dark">

                    <th>ID</th>

                    <th>
                      Employee Name
                    </th>

                    <th>
                      Date
                    </th>

                    <th>
                      Status
                    </th>

                    <th>
                      Edit
                    </th>

                    <th>
                      Delete
                    </th>

                  </tr>

                </thead>

                <tbody>

                  {attendance.length === 0 ? (

                    <tr>

                      <td
                        colSpan="6"
                        className="text-center"
                      >
                        No Attendance Data Found
                      </td>

                    </tr>

                  ) : (

                    attendance.map((i) => (

                      <tr key={i.id}>

                        <td>
                          {i.EmployId}
                        </td>

                        <td>

                          <div className="cell-scroll">
                            {i.Employname}
                          </div>

                        </td>

                        <td>

                          <div className="cell-scroll">
                            {i.Date ? i.Date.split("-").reverse().join("-") : ""}
                          </div>

                        </td>

                        <td>

                          <div className="cell-scroll">
                            {i.Status}
                          </div>

                        </td>

                        {/* EDIT */}

                        <td className="text-center manage-btn">

                          <button
                            className="btn btn-edit btn-sm"
                            onClick={() =>
                              handleEdit(i)
                            }
                          >
                            Edit
                          </button>

                        </td>

                        {/* DELETE */}

                        <td className="text-center manage-btn">

                          <button
                            className="btn btn-delete btn-sm"
                            onClick={() =>
                              handleDelete(i.id)
                            }
                          >
                            Delete
                          </button>

                        </td>

                      </tr>

                    ))

                  )}

                </tbody>

              </table>

            </div>

          </div>

        </div>

      </div>

    </>
  );

};

export default Employ_attendance;
