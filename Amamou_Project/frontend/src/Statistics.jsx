// Statistics.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';

function Statistics() {
  const [plotUrls, setPlotUrls] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('academic'); // Default to academic performance

  useEffect(() => {
    const fetchPlots = async () => {
      try {
        setIsLoading(true);
        const response = await axios.get('http://localhost:8000/generate-plots');
        setPlotUrls(response.data.plot_urls || []);
        setError(null);
      } catch (err) {
        setError(err.response?.data?.detail || err.message);
        console.error('Error fetching plots:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchPlots();
  }, []);

  const groupPlotsByCategory = () => {
    const categories = {
      academic: [],
      performance: [],
      demographics: [],
      trends: []
    };

    plotUrls.forEach(url => {
      if (url.includes('Mark') || url.includes('Semesters') || url.includes('Duration')) {
        categories.academic.push(url);
      } else if (url.includes('Gender') || url.includes('Nationality') || url.includes('Scholarship')) {
        categories.demographics.push(url);
      } else if (url.includes('School') || url.includes('Specialty')) {
        categories.performance.push(url);
      } else if (url.includes('performance') || url.includes('trend')) {
        categories.trends.push(url);
      } else {
        categories.performance.push(url);
      }
    });

    return categories;
  };

  // Slick carousel settings
  const carouselSettings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    adaptiveHeight: true,
    autoplay: true,
    autoplaySpeed: 5000,
    arrows: true,
    responsive: [
      {
        breakpoint: 768,
        settings: {
          arrows: false
        }
      }
    ]
  };

  const plotCategories = groupPlotsByCategory();

  const renderTabContent = () => {
    switch (activeTab) {
      case 'academic':
        return plotCategories.academic.length > 0 ? (
          <Slider {...carouselSettings}>
            {plotCategories.academic.map((url, index) => (
              <div key={`academic-${index}`} className="plot-card">
                <img
                  src={`http://localhost:8000${url}`}
                  alt={`Academic performance visualization ${index + 1}`}
                  className="plot-image"
                />
              </div>
            ))}
          </Slider>
        ) : (
          <div className="no-plots-message">No academic performance visualizations available</div>
        );
      case 'demographics':
        return plotCategories.demographics.length > 0 ? (
          <Slider {...carouselSettings}>
            {plotCategories.demographics.map((url, index) => (
              <div key={`demographics-${index}`} className="plot-card">
                <img
                  src={`http://localhost:8000${url}`}
                  alt={`Demographics visualization ${index + 1}`}
                  className="plot-image"
                />
              </div>
            ))}
          </Slider>
        ) : (
          <div className="no-plots-message">No demographics visualizations available</div>
        );
      case 'performance':
        return plotCategories.performance.length > 0 ? (
          <Slider {...carouselSettings}>
            {plotCategories.performance.map((url, index) => (
              <div key={`performance-${index}`} className="plot-card">
                <img
                  src={`http://localhost:8000${url}`}
                  alt={`Institutional performance visualization ${index + 1}`}
                  className="plot-image"
                />
              </div>
            ))}
          </Slider>
        ) : (
          <div className="no-plots-message">No institutional performance visualizations available</div>
        );
      case 'trends':
        return plotCategories.trends.length > 0 ? (
          <Slider {...carouselSettings}>
            {plotCategories.trends.map((url, index) => (
              <div key={`trends-${index}`} className="plot-card">
                <img
                  src={`http://localhost:8000${url}`}
                  alt={`Performance trend visualization ${index + 1}`}
                  className="plot-image"
                />
              </div>
            ))}
          </Slider>
        ) : (
          <div className="no-plots-message">No performance trends visualizations available</div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="statistics-container" style={{ overflow: 'hidden' }}>
      <h1>Student Performance Statistics</h1>

      <div className="plot-tabs">
        <button
          className={`tab-button ${activeTab === 'academic' ? 'active' : ''}`}
          onClick={() => setActiveTab('academic')}
        >
          Academic Performance
        </button>
        <button
          className={`tab-button ${activeTab === 'demographics' ? 'active' : ''}`}
          onClick={() => setActiveTab('demographics')}
        >
          Student Demographics
        </button>
        <button
          className={`tab-button ${activeTab === 'performance' ? 'active' : ''}`}
          onClick={() => setActiveTab('performance')}
        >
          Institutional Performance
        </button>
        <button
          className={`tab-button ${activeTab === 'trends' ? 'active' : ''}`}
          onClick={() => setActiveTab('trends')}
        >
          Performance Trends
        </button>
      </div>

      {isLoading ? (
        <div className="loading-spinner"></div>
      ) : error ? (
        <div className="error-message">Error loading visualizations: {error}</div>
      ) : (
        <div className="tab-content">
          {renderTabContent()}
        </div>
      )}
    </div>
  );
}

export default Statistics;