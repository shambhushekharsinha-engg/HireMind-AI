import { useState } from "react";

function App() {

  const [file, setFile] = useState(null);

  const [resumeText, setResumeText] = useState("");

  const [skills, setSkills] = useState([]);

  const [score, setScore] = useState(0);

  const [missingSkills, setMissingSkills] = useState([]);
  
  const [suggestions, setSuggestions] = useState([]);

  const [message, setMessage] = useState("");

  const [matchScore, setMatchScore] = useState(0);

  const [strengths, setStrengths] = useState([]);

  const [careerSuggestions, setCareerSuggestions] = useState([]);

  const [rating, setRating] = useState("");

  const handleUpload = async () => {

    if (!file) {
      alert("Please select a PDF resume");
      return;
    }

    const formData = new FormData();

    formData.append("file", file);

    try {

      const response = await fetch(
        "http://localhost:8000/upload-resume/",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      setResumeText(data.resume_text);

      setSkills(data.skills_found);

      setScore(data.ats_score);

      setMatchScore(data.job_match_score);

      setStrengths(data.strengths);

      setMissingSkills(data.missing_skills);

      setSuggestions(data.suggestions);

      setCareerSuggestions(data.career_suggestions);

      setRating(data.rating);

      setMessage(data.message);

    } catch (error) {

      console.error(error);

      alert("Upload failed");
    }
  };

  return (

    <div style={{ padding: "40px", fontFamily: "Arial" }}>

      <h1>HireMind AI Resume Analyzer</h1>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <br /><br />

      <button onClick={handleUpload}>
        Upload Resume
      </button>

      <br /><br />
      <h3>{message}</h3>
     <div>
  <h2
    style={{
      color:
        score >= 80
          ? "green"
          : score >= 60
          ? "orange"
          : "red",
    }}
  >
    ATS Resume Score: {score}/100
  </h2>

  <progress
    value={score}
    max="100"
    style={{ width: "400px", height: "25px" }}
  />
</div>

<br />

<div>
  <h2>
    Job Match Score: {matchScore}%
  </h2>

  <progress
    value={matchScore}
    max="100"
    style={{ width: "400px", height: "25px" }}
  />
</div>

      <h2>Detected Skills</h2>

      <div>
  {skills.map((skill, index) => (
    <span
      key={index}
      style={{
        margin: "5px",
        padding: "8px",
        border: "1px solid black",
        borderRadius: "10px",
        display: "inline-block"
      }}
    >
      {skill}
    </span>
  ))}
</div>
      
      <h2>Missing Skills</h2>

      <ul>
        {missingSkills.map((skill, index) => (
           <li key={index}>{skill}</li>
      ))}
    </ul>

      <h2>Resume Suggestions</h2>

      <ul>
        {suggestions.map((item, index) => (
           <li key={index}>{item}</li>
      ))}
    </ul>

      <h2> Recommended Career Suggestions </h2>

      <ul>
        {careerSuggestions.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>

      <h2>{rating}</h2>

      <h2>Resume Strengths</h2>

      <ul>
        {strengths.map((item, index) => (
           <li key={index}>{item}</li>
      ))}
    </ul>

      <details>
    <summary>View Extracted Resume Text</summary>

    <textarea
    rows="20"
    cols="100"
    value={resumeText}
    readOnly
   />

  </details>

    </div>
  );
}

export default App;