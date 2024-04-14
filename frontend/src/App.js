import React from 'react';
import {BrowserRouter, Route, Routes} from 'react-router-dom'
import Home from './pages/home';
import Groups from './pages/groups';
import GroupIndiv from './pages/groupIndiv';

function App() {

  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path='/' Component={Home}/>
          <Route path='/groups/:userId' Component={Groups}/>
          <Route path='/group/:userId/:groupId' Component={GroupIndiv}/>
        </Routes>        
      </BrowserRouter>
    </div>
  );
}

export default App;
