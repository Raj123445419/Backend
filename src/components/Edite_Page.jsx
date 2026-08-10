
import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

// =====================================================
// DJANGO BACKEND URL
// =====================================================

const API_URL = "https://backend-z4sf.onrender.com";

// =====================================================
// EDIT EMPLOYEE COMPONENT
// =====================================================

const Edite_Page = () => {

  const location = useLocation();
  const navigate = useNavigate();

  // Employ_list.jsx se employee ka data aa raha hai
  const employee = location.state?.employee;

  const [formData, setFormData] = useState({
    Employname: employee?.Employname || "",
    Address: employee?.Address || "",
    Employrole: employee?.Employrole || "",
    Designation: employee?.Designation || "",
    Experince: employee?.Experince || "",
    Salary: employee?.Salary || ""
  });

  const [loading, setLoading] = useState(false);

  // ================= INPUT CHANGE =================

  const handleChange = (e) => {

    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });

  };

  // ================= UPDATE EMPLOYEE =================

  const handleSubmit = async (e) => {

    e.preventDefault();

    if (!employee?.EmployId) {

      alert("Employee ID not found");

      return;
    }

    setLoading(true);

    try {

      const response = await fetch(
        `${API_URL}/Edite/${employee.EmployId}/`,
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
          "Employee Updated Successfully"
        );

        // Update ke baad Employee List par
        navigate("/");

      } else {

        const data =
          await response.json().catch(() => ({}));

        alert(
          data.error ||
          "Employee Update Failed"
        );

      }

    } catch (error) {

      console.log(error);

      alert(
        "Backend connection error"
      );

    } finally {

      setLoading(false);

    }

  };

  // ================= EMPLOYEE DATA NOT FOUND =================

  if (!employee) {

    return (

      <div className="container mt-5">

        <div className="alert alert-danger text-center">

          Employee data not found.

          <br />

          <button
            className="btn btn-primary mt-3"
            onClick={() => navigate("/")}
          >
            Go To Employee List
          </button>

        </div>

      </div>

    );

  }

  return (

    <div className="container">

      <div className="row justify-content-center">

        <div className="col-md-8">

          <div className="card edit-employee-card">

            {/* ================= HEADER ================= */}

            <div className="card-header edit-employee-header">

              Edit Employee

            </div>

            {/* ================= BODY ================= */}

            <div className="card-body">

              <form onSubmit={handleSubmit}>

                {/* ================= EMPLOYEE NAME ================= */}

                <div className="mb-3">

                  <label className="form-label">
                    Employee Name
                  </label>

                  <input
                    type="text"
                    name="Employname"
                    className="form-control"
                    value={formData.Employname}
                    onChange={handleChange}
                    required
                  />

                </div>

                {/* ================= ADDRESS ================= */}

                <div className="mb-3">

                  <label className="form-label">
                    Address
                  </label>

                  <textarea
                    name="Address"
                    className="form-control"
                    rows="3"
                    value={formData.Address}
                    onChange={handleChange}
                    required
                  />

                </div>

                {/* ================= EMPLOYEE ROLE ================= */}

                <div className="mb-3">

                  <label className="form-label">
                    Employee Role
                  </label>

                  <input
                    type="text"
                    name="Employrole"
                    className="form-control"
                    value={formData.Employrole}
                    onChange={handleChange}
                    required
                  />

                </div>

                {/* ================= DESIGNATION ================= */}

                <div className="mb-3">

                  <label className="form-label">
                    Designation
                  </label>

                  <input
                    type="text"
                    name="Designation"
                    className="form-control"
                    value={formData.Designation}
                    onChange={handleChange}
                    required
                  />

                </div>

                {/* ================= EXPERIENCE ================= */}

                <div className="mb-3">

                  <label className="form-label">
                    Experience
                  </label>

                  <input
                    type="text"
                    name="Experince"
                    className="form-control"
                    value={formData.Experince}
                    onChange={handleChange}
                    required
                  />

                </div>

                {/* ================= SALARY ================= */}

                <div className="mb-3">

                  <label className="form-label">
                    Salary
                  </label>

                  <input
                    type="number"
                    name="Salary"
                    className="form-control"
                    value={formData.Salary}
                    onChange={handleChange}
                    required
                  />

                </div>

                {/* ================= BUTTONS ================= */}

                <div className="text-center">

                  <button
                    type="submit"
                    className="btn btn-success me-2"
                    disabled={loading}
                  >

                    {loading
                      ? "Updating..."
                      : "Update Employee"
                    }

                  </button>

                  <button
                    type="button"
                    className="btn btn-secondary"
                    onClick={() => navigate("/")}
                  >
                    Cancel
                  </button>

                </div>

              </form>

            </div>

          </div>

        </div>

      </div>

    </div>

  );

};

export default Edite_Page;

