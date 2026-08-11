
import React, { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import "../App.css";


// =====================================================
// DJANGO BACKEND URL
// =====================================================

const API_URL = "https://backend-z4sf.onrender.com";


// =====================================================
// EMPLOY LIST COMPONENT
// =====================================================

const Employ_list = () => {

  const [employees, setEmployees] = useState([]);

  const [showModal, setShowModal] = useState(false);

  const [loading, setLoading] = useState(true);

  const [formData, setFormData] = useState({
    Employname: "",
    Address: "",
    Employrole: "",
    Designation: "",
    Experince: "",
    Salary: ""
  });


  const navigate = useNavigate();


  // =====================================================
  // GET EMPLOYEE DATA
  // =====================================================

  const getEmployees = async () => {

    try {

      setLoading(true);

      const response = await fetch(
        `${API_URL}/`,
        {
          method: "GET",

          headers: {
            "Accept": "application/json"
          }
        }
      );


      if (!response.ok) {

        throw new Error(
          `Server Error: ${response.status}`
        );

      }


      const data = await response.json();


      console.log(
        "Employees from Django:",
        data
      );


      setEmployees(data);


    } catch (error) {

      console.error(
        "GET Employee Error:",
        error
      );

      alert(
        "Backend connection error"
      );


    } finally {

      setLoading(false);

    }

  };


  // =====================================================
  // LOAD EMPLOYEES
  // =====================================================

  useEffect(() => {

    getEmployees();

  }, []);


  // =====================================================
  // INPUT CHANGE
  // =====================================================

  const handleChange = (e) => {

    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });

  };


  // =====================================================
  // ADD EMPLOYEE
  // =====================================================

  const handleSubmit = async (e) => {

    e.preventDefault();


    try {

      const response = await fetch(
        `${API_URL}/`,
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/x-www-form-urlencoded",

            "Accept":
              "application/json"
          },

          body:
            new URLSearchParams(formData)
        }
      );


      const data =
        await response.json();


      if (response.ok) {

        alert(
          "Employee Added Successfully"
        );


        setShowModal(false);


        setFormData({
          Employname: "",
          Address: "",
          Employrole: "",
          Designation: "",
          Experince: "",
          Salary: ""
        });


        getEmployees();


      } else {

        console.error(
          "Add Employee Error:",
          data
        );


        alert(
          data.error ||
          "Employee add failed"
        );

      }


    } catch (error) {

      console.error(
        "POST Employee Error:",
        error
      );


      alert(
        "Backend connection error"
      );

    }

  };


  // =====================================================
  // EDIT EMPLOYEE
  // =====================================================

  const handleEdit = (employee) => {

    navigate(
      "/edit",
      {
        state: {
          employee: employee
        }
      }
    );

  };


  // =====================================================
  // DELETE EMPLOYEE
  // =====================================================

  const handleDelete = async (id) => {

    const confirmDelete =
      window.confirm(
        "Are you sure you want to delete this employee?"
      );


    if (!confirmDelete) {

      return;

    }


    try {

      const response = await fetch(
        `${API_URL}/Delete/${id}/`,
        {
          method: "DELETE",

          headers: {
            "Accept":
              "application/json"
          }
        }
      );


      const data =
        await response.json();


      if (response.ok) {

        alert(
          "Employee Deleted Successfully"
        );


        getEmployees();


      } else {

        console.error(
          "Delete Error:",
          data
        );


        alert(
          data.error ||
          "Delete failed"
        );

      }


    } catch (error) {

      console.error(
        "DELETE Employee Error:",
        error
      );


      alert(
        "Backend connection error"
      );

    }

  };




  // =====================================================
  // UI
  // =====================================================

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


              {/* EMPLOYEE LIST */}

              <li className="nav-item">

                <Link
                  className="nav-link px-2 px-md-3 cl1"
                  to="/"
                >
                  Employ List
                </Link>

              </li>


              {/* ATTENDANCE */}

              <li className="nav-item">

                <Link
                  className="nav-link px-2 px-md-3 cl1"
                  to="/attendance"
                >
                  Employ Attendance
                </Link>

              </li>


              {/* SALARY */}

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
          ADD BUTTON
      ====================================================== */}

      <div className="col-md-12 d-flex justify-content-end p-2">

        <button
          className="btn add"
          onClick={() =>
            setShowModal(true)
          }
        >
          + Add Employ
        </button>

      </div>


      {/* =====================================================
          TITLE
      ====================================================== */}

      <main>

        <div className="col-md-12">

          <center>

            <h1 className="alltext">
              Employ Details
            </h1>

          </center>

        </div>


        {/* ===================================================
            TABLE
        ==================================================== */}

        <div className="employee-table-box">

          <table
            className="table table-bordered table-hover align-middle employee-table"
          >

            <thead
              className="table-dark text-center alltext"
            >

              <tr>

                <th>
                  Employ Id
                </th>

                <th>
                  Employ Name
                </th>

                <th>
                  Address
                </th>

                <th>
                  Employ Role
                </th>

                <th>
                  Designation
                </th>

                <th>
                  Experience
                </th>

                <th>
                  Salary
                </th>

                <th colSpan="2">
                  Manage
                </th>

              </tr>

            </thead>


            <tbody>


              {employees.length === 0 ? (

                <tr>

                  <td
                    colSpan="9"
                    className="text-center"
                  >
                    No Employee Data Found
                  </td>

                </tr>

              ) : (

                employees.map((i) => (

                  <tr
                    key={i.EmployId}
                  >


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
                        {i.Address}
                      </div>

                    </td>


                    <td>

                      <div className="cell-scroll">
                        {i.Employrole}
                      </div>

                    </td>


                    <td>

                      <div className="cell-scroll">
                        {i.Designation}
                      </div>

                    </td>


                    <td>

                      <div className="cell-scroll">
                        {i.Experince}
                      </div>

                    </td>


                    <td>

                      <div className="cell-scroll">
                        {i.Salary}
                      </div>

                    </td>


                    {/* EDIT */}

                    <td className="text-center">

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

                    <td className="text-center">

                      <button
                        className="btn btn-delete btn-sm"
                        onClick={() =>
                          handleDelete(
                            i.EmployId
                          )
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

      </main>


      {/* =====================================================
          ADD EMPLOYEE MODAL
      ====================================================== */}

      {showModal && (

        <div className="custom-modal">

          <div className="modal-box">


            {/* HEADER */}

            <div className="modal-header">

              <h5>
                Employee Details
              </h5>


              <button
                className="close-btn"
                onClick={() =>
                  setShowModal(false)
                }
              >
                ×
              </button>

            </div>


            {/* FORM */}

            <form
              onSubmit={handleSubmit}
            >

              <div className="modal-body">

                <div className="row g-3">


                  {/* NAME */}

                  <div className="col-12">

                    <label
                      className="form-label fw-semibold"
                    >
                      Employ Name
                    </label>


                    <input
                      type="text"
                      name="Employname"
                      className="form-control"
                      placeholder="Full Name"
                      value={
                        formData.Employname
                      }
                      onChange={
                        handleChange
                      }
                      required
                    />

                  </div>


                  {/* ADDRESS */}

                  <div className="col-12">

                    <label
                      className="form-label fw-semibold"
                    >
                      Address
                    </label>


                    <textarea
                      name="Address"
                      className="form-control"
                      rows="3"
                      placeholder="Enter complete address"
                      value={
                        formData.Address
                      }
                      onChange={
                        handleChange
                      }
                      required
                    />

                  </div>


                  {/* ROLE */}

                  <div className="col-12 col-md-6">

                    <label
                      className="form-label fw-semibold"
                    >
                      Employ Role
                    </label>


                    <input
                      type="text"
                      name="Employrole"
                      className="form-control"
                      placeholder="Employee Role"
                      value={
                        formData.Employrole
                      }
                      onChange={
                        handleChange
                      }
                      required
                    />

                  </div>


                  {/* DESIGNATION */}

                  <div className="col-12 col-md-6">

                    <label
                      className="form-label fw-semibold"
                    >
                      Designation
                    </label>


                    <input
                      type="text"
                      name="Designation"
                      className="form-control"
                      placeholder="Designation"
                      value={
                        formData.Designation
                      }
                      onChange={
                        handleChange
                      }
                      required
                    />

                  </div>


                  {/* EXPERIENCE */}

                  <div className="col-12 col-md-6">

                    <label
                      className="form-label fw-semibold"
                    >
                      Experince
                    </label>


                    <input
                      type="text"
                      name="Experince"
                      className="form-control"
                      placeholder="Experince"
                      value={
                        formData.Experince
                      }
                      onChange={
                        handleChange
                      }
                      required
                    />

                  </div>


                  {/* SALARY */}

                  <div className="col-12 col-md-6">

                    <label
                      className="form-label fw-semibold"
                    >
                      Salary
                    </label>


                    <input
                      type="number"
                      name="Salary"
                      className="form-control"
                      value={
                        formData.Salary
                      }
                      onChange={
                        handleChange
                      }
                      required
                    />

                  </div>


                </div>

              </div>


              {/* FOOTER */}

              <div className="modal-footer">


                <button
                  type="button"
                  className="btn btn-secondary px-4"
                  onClick={() =>
                    setShowModal(false)
                  }
                >
                  Close
                </button>


                <button
                  type="submit"
                  className="btn btn-primary px-4"
                >
                  Save Details
                </button>


              </div>


            </form>


          </div>

        </div>

      )}


    </>

  );

};


export default Employ_list;
