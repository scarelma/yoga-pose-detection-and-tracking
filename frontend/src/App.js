
import { Routes, Route } from 'react-router-dom';

import { Home } from './components/Home';
import {Login} from './components/Login';
import {Register} from './components/Register';
import {Userdata} from './components/Userdata';
import {Visual} from './components/Visual';
import {AddData} from './components/AddData';



function App() {
  return (
    <>
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
