import './App.css';
import React, { useState } from 'react';
import axios from 'axios';

const FileUpload = () => {
  const [file, setFile] = useState(null);

  const submitFile = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post('http://localhost:8000/analyze/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log(res.data); 
    } catch (error) {
      console.error(error);
    }
  };

  const handleFileUpload = (event) => {
    setFile(event.target.files[0]);
  };

  return (
    <form
      onSubmit={submitFile}
      className='file-upload'>
      <input
        type='file'
        onChange={handleFileUpload}
      />
      <button type='submit'>Submit</button>
    </form>
  );
};

export default FileUpload;
