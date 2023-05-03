
import { Routes, Route, Link } from 'react-router-dom';

import { Home } from './components/Home';
import { Login } from './components/Login';
import { Register } from './components/Register';
import { Userdata } from './components/Userdata';
import { Visual } from './components/Visual';
import { AddData } from './components/AddData';
import { useAuth } from "./components/auth/index"


// const PrivateRoute = ({ component: Component, ...rest }) => {
//   const [logged] = useAuth();
//   const navigate = useNavigate();

//   return <Route {...rest} render={(props) => (
//     logged
//       ? <Component {...props} />
//       : <Navigate to="/login" />
//   )} />
// }

function App() {
  const [logged, session] = useAuth();
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
          {logged && (
            <>
              <li>
                <Link to="/userdata" > User Data </Link>
              </li>
              <li>
                <Link to="/visual" > Visual </Link>
              </li>
              <li>
                <Link to="/adddata" > Add Data </Link>
              </li>
            </>
          )}
          {/* <Link to="/adddata">Add data</Link> */}
          {/* <PrivateRoute path="/adddata" component={AddData} /> */}
        </ul>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        {/* <PrivateRoute path="/adddata" component={AddData} />
        <PrivateRoute path="/userdata" component={Userdata} />
        <PrivateRoute path="/visual" component={Visual} />
         */}

        {logged && (
          <>
            <Route path="/userdata" element={<Userdata />} />
            <Route path="/visual" element={<Visual />} />
            <Route path="/adddata" element={<AddData />} />
            {/* <Route path="/dashboard" component={Dashboard} exact /> */}
            {/* <Redirect to="/dashboard" /> */}
          </>
        )}

      </Routes>
    </>
  );
}

export default App;
