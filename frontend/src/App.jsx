import React, { useState } from "react";
import axios from "axios";
import "./App.css";

/**
 * App component for AI Resume Analyzer.
 * Allows users to upload a PDF or TXT file and analyzes it to extract keywords.
 */
function App() {
    // State to store the selected file
    const [selectedFile, setSelectedFile] = useState(null);
    // State to store the extracted keywords from the file
    const [extractedKeywords, setExtractedKeywords] = useState([]);
    // State to store any error messages
    const [errorMessage, setErrorMessage] = useState("");

    /**
     * Handles the file input change event.
     * Validates the file type and updates the selected file state.
     * @param {Object} event - The file input change event
     */
    const handleFileChange = (event) => {
        const file = event.target.files[0];
        // Check if the file type is either PDF or TXT
        if (file && !["application/pdf", "text/plain"].includes(file.type)) {
            setErrorMessage("Invalid file type. Please upload a PDF or TXT file.");
            setSelectedFile(null);
        } else {
            setErrorMessage("");
            setSelectedFile(file);
        }
    };

    /**
     * Initiates the file analysis process.
     * Validates if a file is selected and then calls the analyzeFile function.
     */
    const handleAnalyze = async () => {
        if (!selectedFile) {
            setErrorMessage("Please upload a file.");
            return;
        }

        setErrorMessage("");
        setExtractedKeywords([]);

        try {
            // Call the analyzeFile function and update the extracted keywords state
            const keywords = await analyzeFile(selectedFile);
            setExtractedKeywords(keywords);
        } catch (error) {
            setErrorMessage("Failed to analyze the resume. Please try again later.");
        }
    };

    /**
     * Sends the selected file to the backend for analysis.
     * @param {File} file - The file to be analyzed
     * @returns {Array} - An array of extracted keywords
     */
    const analyzeFile = async (file) => {
        const formData = new FormData();
        formData.append("file", file);

        // Send a POST request to the backend with the file
        const response = await axios.post("http://127.0.0.1:5000/analyze", formData, {
            headers: { "Content-Type": "multipart/form-data" },
        });
        // Return the keywords from the response or an empty array if none
        return response.data.keywords || [];
    };

    return (
        <div className="app-container">
            <h1>AI Resume Analyzer</h1>
            {/* File input for uploading PDF or TXT files */}
            <input type="file" onChange={handleFileChange} accept=".pdf,.txt" />
            {/* Button to trigger the analysis */}
            <button onClick={handleAnalyze} className="analyze-button">
                Analyze Resume
            </button>
            {/* Display error message if any */}
            {errorMessage && <p className="error-message">{errorMessage}</p>}
            {/* Display extracted keywords if any */}
            {extractedKeywords.length > 0 && (
                <div className="keywords-container">
                    <h3>Extracted Keywords:</h3>
                    <ul>
                        {extractedKeywords.map((keyword, index) => (
                            <li key={index}>{keyword}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}

export default App;
