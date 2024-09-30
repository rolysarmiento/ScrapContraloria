import React from 'react';

import {Routes, Route, BrowserRouter} from 'react-router-dom';
import Inicio from './components/Pages/inicio';
import Config from './components/Pages/config';
import Resultados from './components/Pages/resultados';

function App() {
  
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" exact element={<Inicio />}> </Route>
          <Route path="/config" exact element={<Config />}> </Route>  
          <Route path="/resultados" exact element={<Resultados />}> </Route>
        </Routes>
      </BrowserRouter>
    </>

  );
}

export default App;
