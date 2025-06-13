import { FaInstagram, FaWhatsapp, FaLinkedin, FaGithub } from "react-icons/fa";
import axios from "axios";
import { useState } from "react";

function App() {
  const [preview, setPreview] = useState([]);
  const [tripPlotUrl, setTripPlotUrl] = useState("");
  const [pricePlotUrl, setPricePlotUrl] = useState("");
  const [bestHourMessage, setBestHourMessage] = useState("");
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);
  const [file, setFile] = useState(null);


  const callBackend = async (path, formData) => {
    setLoading(true);
    setStatus("");
    try {
      const res = await axios.post(`http://localhost:8000${path}`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      return res.data;
    } catch (error) {
      setStatus(`Error: ${error.response?.data?.message || error.message}`);
      return null;
    } finally {
      setLoading(false);
    }
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setPreview([]);
      setTripPlotUrl("");
      setPricePlotUrl("");
      setBestHourMessage("");
      setStatus(`Selected file: ${selectedFile.name}`);
    }
  };

  const handleAction = async (action) => {
    if (!file) {
      setStatus("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const result = await callBackend(`/${action}`, formData);

    if (result) {
      if (
        action === "generate-plottrips" ||
        action === "generate-plotprice" ||
        action === "best-hour-work" ||
          action === "load-preview"
      ) {
        setTripPlotUrl("");
        setPricePlotUrl("");
        setBestHourMessage("");
        setPreview([]);
      }

      switch (action) {
        case "load-preview":
          setPreview(result);
          setStatus("Preview Loaded Successfully!");
          break;
        case "generate-plottrips":
          if (result.plot_url) {
            setTripPlotUrl(result.plot_url);
            setStatus("Trip Plot Generated Successfully!");
          }
          break;
        case "generate-plotprice":
          if (result.plot_url) {
            setPricePlotUrl(result.plot_url);
            setStatus("Price Plot Generated Successfully!");
          }
          break;
        case "best-hour-work":
          if (result.message) {
            setBestHourMessage(result.message);
            setStatus("");
          }
          break;
        default:
          setStatus(
            `Data ${action.charAt(0).toUpperCase() + action.slice(1)} Successfully!`
          );
      }
    }
  };

  return (
    <div className="app-container">
      <div className="content-box">

        {/* 1. Header Section */}
        <section className="header-section">
          <h1>🚖 NY Taxi Data Analyzer</h1>
          <p>Upload, clean, enrich & visualize your NYC taxi data effortlessly.</p>
        </section>

        {/* 2. File & Status Section */}
        <section className="file-section">
          <label>Choose a file:</label>
          <input type="file" onChange={handleFileChange} accept=".parquet" />
          {status && <div className="status-message">{status}</div>}
        </section>

        {/* 3. Buttons Section */}
<section className="button-section">
  {[
    ["Load Preview", "load-preview"],
    ["Clean Data", "clean"],
    ["Enrich Data", "enrich"],
    ["Generate Trips Plot", "generate-plottrips"],
    ["Generate Price Plot", "generate-plotprice"],
    ["BHP", "best-hour-work"],
  ].map(([label, action]) => (
      <button key={action} onClick={() => handleAction(action)} disabled={loading}>
        {label}
      </button>
  ))}
</section>


        {/* 4. Plots Section */}
        <section className="plot-section">
          {tripPlotUrl && (
              <div>
                <img src={tripPlotUrl} alt="Trips Plot"/>
              </div>
          )}
          {pricePlotUrl && (
              <div>
                <img src={pricePlotUrl} alt="Price Plot"/>
              </div>
          )}
          {bestHourMessage && (
            <div className="bhp-message">
              <h3>BHP:</h3>
              <p>{bestHourMessage}</p>
            </div>
          )}
          {preview.length > 0 && (
  <div className="preview-section">
    <table>
      <thead>
        <tr>
          {Object.keys(preview[0]).map((col, index) => (
            <th key={index}>{col}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {preview.map((row, idx) => (
          <tr key={idx}>
            {Object.values(row).map((val, i) => (
              <td key={i}>{val}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  </div>
)}
          {loading && <p className="loading">Processing...</p>}
        </section>
        {/* 5. Social Section */}
        <section className="social-section">
          <a href="https://www.instagram.com/yassir_tage/" target="_blank"><FaInstagram /></a>
          <a href="https://wa.me/+212675630026" target="_blank"><FaWhatsapp /></a>
          <a href="https://www.linkedin.com/in/yassir-tagemouati-471a6a2a2/" target="_blank"><FaLinkedin /></a>
          <a href="https://github.com/TageYassir" target="_blank"><FaGithub /></a>
        </section>
      </div>
    </div>


  );
}

export default App;
