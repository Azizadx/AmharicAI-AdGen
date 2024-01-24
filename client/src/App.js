import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dropdown from './components/Dropdown';
import Button from './components/Button';
import './styles.css';

const Home = () => <h2>Welcome To AiQEM</h2>;

const App = () => {
  const [selectedOption, setSelectedOption] = useState('Option 1');

  const handleDropdownChange = (value) => {
    setSelectedOption(value);
  };

  const handleButtonClick = () => {
    alert(`Selected option: ${selectedOption}`);
  };

  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <Link to="/">AiQEM</Link>
            </li>
            <li>
              <Link to="/dropdown">Select Channel</Link>
            </li>
            <li>
              <Link to="/button">Button</Link>
            </li>
          </ul>
        </nav>

        <hr />

        <Routes>
          <Route path="/" element={<Home />} />
          <Route
            path="/dropdown"
            element={
              <Dropdown
                options={['Option 1', 'Option 2', 'Option 3']}
                selectedOption={selectedOption}
                onSelect={handleDropdownChange}
              />
            }
          />
          <Route
            path="/button"
            element={<Button onClick={handleButtonClick} label="Click me" />}
          />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
