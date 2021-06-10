import React from 'react'; 
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'; 
import MainPage from './pages/MainPage';
import DataInputPage from './pages/DataInputPage';
import LogPage from './pages/LogPage';
import AnalysisPage from './pages/AnalysisPage';

function App() { 
  return ( 
    <> 
      <Router> 
        <Switch> 
          <Route exact path='/' component={MainPage} />
          <Route path='/datainput' component={DataInputPage} /> 
          <Route path='/log' component={LogPage} /> 
          <Route path='/analysis' component={AnalysisPage} /> 
          <Route render={() => <div className='error'>에러 페이지</div>} /> 
        </Switch> 
      </Router> 
    </> 
  ); 
} 

export default App;