import './App.css';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [responseData, setResponseData] = useState({});
  const [isProcessing, setIsProcessing] = useState(false);
  const [processingText, setProcessingText] = useState('Processing');

  useEffect(() => {
    if (isProcessing) {
      const id = setInterval(() => {
        setProcessingText((text) => {
          return text.length < 15 ? text + '.' : 'Processing.';
        });
      }, 500);
      return () => clearInterval(id);
    } else {
      setProcessingText('Processing');
    }
  }, [isProcessing]);

  const submitFile = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append('file', file);
    setIsProcessing(true);

    try {
      const res = await axios.post('http://localhost:8000/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      const parsedData = JSON.parse(res.data.content);
      console.log(parsedData);

      setResponseData(parsedData);
    } catch (error) {
      console.error(error);
    } finally {
      setIsProcessing(false);
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
        {isProcessing && <p style={{ color: 'blue' }}>{processingText}</p>}

        <p className='attributes'>
          Here are the insights discovered from the transcript
        </p>
        {responseData.delivery_days && (
          <p className='attributes'>
            Delivery Days: {responseData.delivery_days}
          </p>
        )}
        {responseData.price_value && (
          <p className='attributes'>Price Value: {responseData.price_value}</p>
        )}
        {responseData.customer_negative_feedback && (
          <p className='attributes'>
            Customer Negative Feedback:{' '}
            {responseData.customer_negative_feedback}
          </p>
        )}
        {responseData.feature_requests && (
          <p className='attributes'>
            Feature Requests: {responseData.feature_requests}
          </p>
        )}
        {responseData.competitor_mentions && (
          <p className='attributes'>
            Competitor Mentions: {responseData.competitor_mentions}
          </p>
        )}
      </form>
    </div>
  );
};

export default FileUpload;
