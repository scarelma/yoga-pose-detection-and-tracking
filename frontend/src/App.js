
import { Routes, Route, Link } from 'react-router-dom';

import { Home } from './components/Home';
import { Login } from './components/Login';
import { Register } from './components/Register';
import { Userdata } from './components/Userdata';
import { Visual } from './components/Visual';
import { AddData } from './components/AddData';



function App() {
  return (
    <>
      <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/login">Login</Link>
            </li>
            <li>
              <Link to="/adddata">Add data</Link>
            </li>
          </ul>
        </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/userdata" element={<Userdata />} />
        <Route path="/visual" element={<Visual />} />
        <Route path="/adddata" element={<AddData />} />
      </Routes>
    </>
  );
}

export default App;
