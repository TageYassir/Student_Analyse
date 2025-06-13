import React, { useState } from 'react';
import axios from 'axios';

// School and specialty data
const schools = {
  "Euromed Polytechnic School (EPS)": {},
  "Ecole d'Ingénierie Digitale et d'Intelligence Artificielle (EIDIA)": {},
  "Ecole Euromed d'Architecture de Design et d'Urbanisme (EMADU)": {},
  "Faculté des Sciences Humaines et Sociales": {},
  "Euromed Business School": {},
  "Institut Euromed des Sciences Juridiques et Politiques": {},
  "Faculté Euromed de Pharmacie": {},
  "Ecole d'ingénieur BiomedTech": {},
  "Faculté Euromed de Médecine": {},
  "Faculté Euromed de Médecine Dentaire": {},
  "Faculté des Sciences Infirmières et Techniques de Santé": {}
};

const specialties = {
  "Euromed Polytechnic School (EPS)": [
    "Génie Civil", "Génie des Opérations et de la Logistique", "Génie des Procédés",
    "Génie Mécanique, Productique et Thermique", "Génie Électrique EEA",
    "Accompagnement Entrepreneurial et Management Technologique",
    "Transports et Mobilité Durable", "Génie Environnemental et Gestion de l'Eau",
    "Conception et Ingénierie de Bâtiments Verts", "Matériaux Fonctionnels et Fabrication Additive"
  ],
  "Ecole d'Ingénierie Digitale et d'Intelligence Artificielle (EIDIA)": [
    "Intelligence Artificielle", "Robotique et Cobotique", "Cyber-sécurité",
    "Ingénierie d'Applications Web & Mobile", "Big Data Analytics",
    "ICT Security and Artificial Intelligence"
  ],
  "Ecole Euromed d'Architecture de Design et d'Urbanisme (EMADU)": [
    "Architecture", "Design", "Urbanisme et ses Territoires"
  ],
  "Faculté des Sciences Humaines et Sociales": [
    "Traduction", "Méthodes et Métiers de l'Ingénierie Culturelle",
    "Sciences Sociales et Management de la Santé",
    "Communication des Entreprises et des Institutions", "Journalisme et Nouveaux Médias"
  ],
  "Euromed Business School": [
    "Management des Organisations", "Marketing et Communication",
    "Finance et Contrôle de Gestion", "Entrepreneuriat et Innovation"
  ],
  "Institut Euromed des Sciences Juridiques et Politiques": [
    "Droit Public", "Droit Privé", "Sciences Politiques",
    "Droit International", "Gouvernance et Politiques Publiques"
  ],
  "Faculté Euromed de Pharmacie": [
    "Docteur en Pharmacie (Officine)", "Docteur en Pharmacie (Biologie Médicale)",
    "Docteur en Pharmacie (Industrie Pharmaceutique)", "Docteur en Pharmacie (Produits de Santé)",
    "Docteur en Pharmacie (Secteur Public)"
  ],
  "Ecole d'ingénieur BiomedTech": [
    "Biotechnologie", "Sciences Biomédicales",
    "Génie Biologique", "Biotechnologie Appliquée"
  ],
  "Faculté Euromed de Médecine": [
    "Médecine Générale", "Spécialités Médicales",
    "Recherche Médicale", "Santé Publique"
  ],
  "Faculté Euromed de Médecine Dentaire": [
    "Chirurgie Dentaire", "Orthodontie",
    "Parodontologie", "Prothèses Dentaires"
  ],
  "Faculté des Sciences Infirmières et Techniques de Santé": [
    "Sciences Infirmières", "Sciences de Rééducation et Réhabilitation",
    "Sciences de la Nutrition", "Techniques de Santé"
  ]
};

function Prediction() {
  const [formData, setFormData] = useState({
    Mark: '',
    Scholarship: '',
    Gender: '',
    School: '',
    Specialty: '',
    Validated_Semesters: '',
    Repeated_Semesters: '',
    Failed_Semesters: ''
  });
  const [prediction, setPrediction] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [availableSpecialties, setAvailableSpecialties] = useState([]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSchoolChange = (e) => {
    const selectedSchool = e.target.value;
    setFormData(prev => ({
      ...prev,
      School: selectedSchool,
      Specialty: ''
    }));
    setAvailableSpecialties(specialties[selectedSchool] || []);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      const response = await axios.post('http://localhost:8000/predict', formData);
      setPrediction(response.data);
    } catch (error) {
      console.error('Prediction error:', error);
      setError('An error occurred while making the prediction. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
            Student Graduation Prediction
          </h1>
          <p className="mt-3 text-xl text-gray-600">
            Predict the likelihood of a student graduating based on academic performance
          </p>
        </div>

        <div className="bg-white shadow-xl rounded-lg overflow-hidden">
          <div className="p-6 sm:p-8">
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                {/* Mark */}
                <div className="sm:col-span-2">
                  <label htmlFor="Mark" className="block text-sm font-medium text-gray-700">
                    Average Mark
                  </label>
                  <div className="mt-1 relative rounded-md shadow-sm">
                    <input
                      type="number"
                      name="Mark"
                      id="Mark"
                      value={formData.Mark}
                      onChange={handleChange}
                      step="0.01"
                      min="0"
                      max="20"
                      required
                      className="block w-full pr-10 pl-3 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                      placeholder="0.00 - 20.00"
                    />
                    <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                      <span className="text-gray-500 sm:text-sm">/20</span>
                    </div>
                  </div>
                </div>

                {/* Scholarship */}
                <div>
                  <label htmlFor="Scholarship" className="block text-sm font-medium text-gray-700">
                    Scholarship
                  </label>
                  <select
                    id="Scholarship"
                    name="Scholarship"
                    value={formData.Scholarship}
                    onChange={handleChange}
                    required
                    className="mt-1 block w-full pl-3 pr-10 py-3 text-base border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
                  >
                    <option value="">Select an option</option>
                    <option value="1">Yes</option>
                    <option value="0">No</option>
                  </select>
                </div>

                {/* Gender */}
                <div>
                  <label htmlFor="Gender" className="block text-sm font-medium text-gray-700">
                    Gender
                  </label>
                  <select
                    id="Gender"
                    name="Gender"
                    value={formData.Gender}
                    onChange={handleChange}
                    required
                    className="mt-1 block w-full pl-3 pr-10 py-3 text-base border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
                  >
                    <option value="">Select an option</option>
                    <option value="M">Male</option>
                    <option value="F">Female</option>
                  </select>
                </div>

                {/* School */}
                <div className="sm:col-span-2">
                  <label htmlFor="School" className="block text-sm font-medium text-gray-700">
                    School
                  </label>
                  <select
                    id="School"
                    name="School"
                    value={formData.School}
                    onChange={handleSchoolChange}
                    required
                    className="mt-1 block w-full pl-3 pr-10 py-3 text-base border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
                  >
                    <option value="">Select a school</option>
                    {Object.keys(schools).map((school) => (
                      <option key={school} value={school}>
                        {school}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Specialty */}
                <div className="sm:col-span-2">
                  <label htmlFor="Specialty" className="block text-sm font-medium text-gray-700">
                    Specialty
                  </label>
                  <select
                    id="Specialty"
                    name="Specialty"
                    value={formData.Specialty}
                    onChange={handleChange}
                    required
                    disabled={!availableSpecialties.length}
                    className="mt-1 block w-full pl-3 pr-10 py-3 text-base border border-gray-300 bg-white disabled:bg-gray-100 disabled:text-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
                  >
                    <option value="">
                      {availableSpecialties.length ? 'Select a specialty' : 'Select a school first'}
                    </option>
                    {availableSpecialties.map((spec) => (
                      <option key={spec} value={spec}>
                        {spec}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Validated Semesters */}
                <div>
                  <label htmlFor="Validated_Semesters" className="block text-sm font-medium text-gray-700">
                    Validated Semesters
                  </label>
                  <input
                    type="number"
                    id="Validated_Semesters"
                    name="Validated_Semesters"
                    value={formData.Validated_Semesters}
                    onChange={handleChange}
                    min="0"
                    required
                    className="mt-1 block w-full pl-3 pr-3 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                    placeholder="Number of validated semesters"
                  />
                </div>

                {/* Repeated Semesters */}
                <div>
                  <label htmlFor="Repeated_Semesters" className="block text-sm font-medium text-gray-700">
                    Repeated Semesters
                  </label>
                  <input
                    type="number"
                    id="Repeated_Semesters"
                    name="Repeated_Semesters"
                    value={formData.Repeated_Semesters}
                    onChange={handleChange}
                    min="0"
                    required
                    className="mt-1 block w-full pl-3 pr-3 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                    placeholder="Number of repeated semesters"
                  />
                </div>

                {/* Failed Semesters */}
                <div>
                  <label htmlFor="Failed_Semesters" className="block text-sm font-medium text-gray-700">
                    Failed Semesters
                  </label>
                  <input
                    type="number"
                    id="Failed_Semesters"
                    name="Failed_Semesters"
                    value={formData.Failed_Semesters}
                    onChange={handleChange}
                    min="0"
                    required
                    className="mt-1 block w-full pl-3 pr-3 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                    placeholder="Number of failed semesters"
                  />
                </div>
              </div>

              <div className="pt-6">
                <button
                  type="submit"
                  disabled={isLoading}
                  className="group relative flex w-full justify-center rounded-md bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 px-6 py-3 text-lg font-semibold text-white shadow-lg ring-1 ring-indigo-600 ring-offset-2 ring-offset-indigo-100 hover:from-pink-600 hover:via-purple-600 hover:to-indigo-600 transition-all duration-300 overflow-hidden"
                >
                  <span className="absolute inset-0 animate-gradient bg-gradient-to-r from-pink-600 via-purple-600 to-indigo-600 opacity-20 blur-lg"></span>
                  {isLoading ? 'Predicting...' : 'Predict Graduation'}
                </button>
              </div>
            </form>

            {error && (
              <div className="mt-4 text-center text-red-600 font-medium">{error}</div>
            )}

            {prediction && !error && (
  <div className="mt-6 p-6 bg-indigo-50 rounded-md shadow-inner text-center">
    <h2 className="text-2xl font-semibold text-indigo-700 mb-4">Prediction Result</h2>
    <p className="text-lg">
      <span className="font-semibold">Graduation Status:</span>{' '}
      {prediction.Graduated_Prediction ? (
        <span className="text-green-600">Likely to Graduate 🎉</span>
      ) : (
        <span className="text-red-600">Unlikely to Graduate ⚠️</span>
      )}
    </p>
    <p className="mt-2 text-gray-700">
      <span className="font-semibold">Probability:</span>{' '}
      {(prediction.Probability * 100).toFixed(2)}%
    </p>
  </div>
)}

          </div>
        </div>
      </div>

      <style jsx>{`
        @keyframes gradient {
          0% {
            background-position: 0% 50%;
          }
          50% {
            background-position: 100% 50%;
          }
          100% {
            background-position: 0% 50%;
          }
        }
        .animate-gradient {
          background-size: 200% 200%;
          animation: gradient 5s ease infinite;
        }
      `}</style>
    </div>
  );
}

export default Prediction;
