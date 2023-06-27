import './App.css';
import React, { useState } from 'react';
import axios from 'axios';

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [responseData, setResponseData] = useState({});

  const submitFile = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post('http://localhost:8000/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log(res.data.content);
      setResponseData(res.data.content);
    } catch (error) {
      console.error(error);
    }
  };

  const handleFileUpload = (event) => {
    setFile(event.target.files[0]);
  };

  return (
    <div>
      <form
        onSubmit={submitFile}
        className='file-upload'>
        <label
          htmlFor='file-upload'
          style={{
            fontFamily: 'Fantasy',
            color: 'white',
            fontSize: '50px',
            textAlign: 'center',
          }}>
          Upload Transcription for Product Analysis
        </label>
        <input
          type='file'
          onChange={handleFileUpload}
        />
        <button type='submit'>Submit</button>
      </form>
      <div>
        {responseData.delivery_days ? 
          <p>Delivery Days: {responseData.delivery_days}</p> : null}
        {responseData.price_value ?
          <p>Price Value: {responseData.price_value}</p> : null}
        {responseData.customer_negative_feedback ? 
          <p>Customer Negative Feedback: {responseData.customer_negative_feedback}</p> : null}
        {responseData.feature_requests ? 
          <p>Feature Requests: {responseData.feature_requests}</p> : null}
        {responseData.competitor_mentions ? 
          <p>Competitor Mentions: {responseData.competitor_mentions}</p> : null}
      </div>
    </div>
  );
};

export default FileUpload;
