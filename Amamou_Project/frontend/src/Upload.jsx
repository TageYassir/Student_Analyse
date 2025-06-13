import React, { useState } from 'react';
import axios from 'axios';
import Slider from 'react-slick';
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";

function Upload() {
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');
  const [plotUrls, setPlotUrls] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setUploadStatus(`Selected file: ${e.target.files[0].name}`);
      setPlotUrls([]); // reset plots on new file select
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setUploadStatus('Please select a file first');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      setIsUploading(true);
      setUploadStatus('Uploading file...');

      await axios.post('http://localhost:8000/upload-data', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setUploadStatus('Upload successful! You can now generate plots.');
    } catch (error) {
      setUploadStatus(`Error: ${error.response?.data?.detail || error.message}`);
      console.error('Upload error:', error);
    } finally {
      setIsUploading(false);
    }
  };

  const handleGeneratePlots = async () => {
    try {
      setIsGenerating(true);
      setUploadStatus('Generating plots...');

      const plotResponse = await axios.get('http://localhost:8000/generate-plots');
      setPlotUrls(plotResponse.data.plot_urls);
      setUploadStatus('Plot generation successful!');
    } catch (error) {
      setUploadStatus(`Error: ${error.response?.data?.detail || error.message}`);
      console.error('Generation error:', error);
    } finally {
      setIsGenerating(false);
    }
  };

  // Slider settings for react-slick
  const sliderSettings = {
    dots: true,
    infinite: false,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: true,
    adaptiveHeight: true,
  };

  return (
    <div className="upload-container">
      <h2>Upload Student Data</h2>
      <div className="upload-box">
        <div className="file-input-container">
          <label className="file-input-label" htmlFor="file-input">
            Choose CSV File
          </label>
          <input
            id="file-input"
            type="file"
            accept=".csv"
            onChange={handleFileChange}
            className="file-input"
            disabled={isUploading || isGenerating}
          />
          {file && <span className="file-name">{file.name}</span>}
        </div>

        <div className="buttons-row">
          <button
            onClick={handleUpload}
            disabled={!file || isUploading || isGenerating}
          >
            {isUploading ? 'Uploading...' : 'Upload'}
          </button>

          <button
            onClick={handleGeneratePlots}
            disabled={isUploading || isGenerating}
          >
            {isGenerating ? 'Generating...' : 'Plots'}
          </button>
        </div>

        {uploadStatus && (
          <p className={`upload-status ${uploadStatus.startsWith('Error') ? 'error' : ''}`}>
            {uploadStatus}
          </p>
        )}
      </div>

      {plotUrls.length > 0 && (
        <div className="plots-container">
          <h3>Generated Visualizations</h3>
          <Slider {...sliderSettings}>
            {plotUrls.map((url, index) => (
              <div key={index} className="plot-item">
                <img
                  src={`http://localhost:8000${url}`}
                  alt={`Data visualization ${index + 1}`}
                  className="plot-image"
                />
              </div>
            ))}
          </Slider>
        </div>
      )}
    </div>
  );
}

export default Upload;
