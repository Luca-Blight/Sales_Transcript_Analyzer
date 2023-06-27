import logo from './logo.svg';
import './App.css';
import FileUpload from './FileUpload';

function App() {
  return (
    <div className='App'>
      <header className='App-header'>
        <div className='logo-container'>
          <img
            src={logo}
            className='App-logo'
            alt='logo'
          />
          <a
            className='App-link'
            href='https://github.com/Luca-Blight/zelta-challenge'
            target='_blank'
            rel='noopener noreferrer'>
            Source Code
          </a>
        </div>
      </header>
      <div className='App-body'>
        <FileUpload />
      </div>
    </div>
  );
}

export default App;
