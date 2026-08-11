  import React, { useEffect, useState } from "react";
  import { Link } from "react-router-dom";



  const API_URL = "https://backend-z4sf.onrender.com";


  const Employ_Sallery = () => {

    const [salaryData, setSalaryData] = useState([]);

    const [loading, setLoading] = useState(true);

    // ================= GET SALARY DATA =================

    const getSalaryData = async () => {

      try {

        setLoading(true);

        const response = await fetch(
          `${API_URL}/Employ_Sallery/`,
          {
            method: "GET",

            headers: {
              "Accept": "application/json"
            }
          }
        );

        if (!response.ok) {

          throw new Error(
            "Failed to fetch salary data"
          );

        }

        const data = await response.json();

        console.log(
          "Salary data from Django:",
          data
        );

        setSalaryData(data);

      } catch (error) {

        console.log(error);

      } finally {

        setLoading(false);

      }

    };

    useEffect(() => {

      getSalaryData();

    }, []);



    return (

      <>

        {/* ================= NAVBAR ================= */}

        <header>

          <div className="all">

            <nav className="navbar navbar-expand-sm">

              <div className="container-fluid">


                {/* LOGO */}

                <Link
                  className="navbar-brand fontnav px-2 px-md-3 cl1"
                  to="/"
                >
                  Employ Management System
                </Link>


                {/* TOGGLER */}

                <button
                  className="navbar-toggler"
                  style={{
                    backgroundColor: "#018c8c90",
                    color: "#FFFFFF"
                  }}
                  type="button"
                  data-bs-toggle="collapse"
                  data-bs-target="#collapsibleNavbar"
                >

                  <span className="navbar-toggler-icon"></span>

                </button>


                {/* NAV LINKS */}

                <div
                  className="collapse navbar-collapse"
                  style={{
                    justifyContent: "end"
                  }}
                  id="collapsibleNavbar"
                >

                  <ul className="navbar-nav">


                    {/* EMPLOY LIST */}

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

        </header>


        {/* ================= PAGE TITLE ================= */}

        <div
          className="col-md-12 mt-4 alltext"
          style={{
            textAlign: "center"
          }}
        >

          <h1>
            Employ Sallery Count
          </h1>

        </div>


        {/* ================= SALARY TABLE ================= */}

        <div className="w-100 overflow-hidden">

          <table
            className="table table-bordered table-striped alltext salary-table"
          >


            {/* TABLE HEADER */}

            <thead className="table-dark">

              <tr>

                <th>
                  Employee ID
                </th>

                <th>
                  Employee Name
                </th>

                <th>
                  Monthly Salary
                </th>

                <th>
                  Present
                </th>

                <th>
                  Half Day
                </th>

                <th>
                  Absent
                </th>

                <th>
                  Total Salary
                </th>

              </tr>

            </thead>


            {/* TABLE BODY */}

            <tbody>

              {salaryData.length === 0 ? (

                <tr>

                  <td
                    colSpan="7"
                    className="text-center"
                  >
                    No Salary Data Found
                  </td>

                </tr>

              ) : (

                salaryData.map((p) => (

                  <tr key={p.EmployId}>


                    {/* EMPLOYEE ID */}

                    <td>
                      {p.EmployId}
                    </td>


                    {/* EMPLOYEE NAME */}

                    <td>

                      <div className="cell-scroll">

                        {p.Employname}

                      </div>

                    </td>


                    {/* MONTHLY SALARY */}

                    <td>

                      <div className="cell-scroll">

                        ₹ {p.Salary}

                      </div>

                    </td>


                    {/* PRESENT */}

                    <td>
                      {p.Present}
                    </td>


                    {/* HALF DAY */}

                    <td>
                      {p.HalfDay}
                    </td>


                    {/* ABSENT */}

                    <td>
                      {p.Absent}
                    </td>


                    {/* TOTAL SALARY */}

                    <td>

                      <div className="cell-scroll">

                        <b>
                          ₹ {p.TotalSalary}
                        </b>

                      </div>

                    </td>


                  </tr>

                ))

              )}

            </tbody>


          </table>

        </div>

      </>

    );

  };

  export default Employ_Sallery;