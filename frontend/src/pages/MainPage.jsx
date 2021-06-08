import React from 'react'; 

function MainPage({ location, history }) { 
  console.log(history); 
  console.log(location); 
  return ( 
    <main className='main'> 
      <span class="main-inline-block">
        <strong className='mainstrong'>Road<br/>Classification<br/>Simulator</strong> 
        <ul>
          <li1> 
            <button className="btn" onClick={() => history.push('/datainput')}>실행</button>
          </li1> 
          <li2> 
            <button className="btn" onClick={() => history.push('/log')}>Log</button> 
          </li2> 
        </ul> 
      </span>
    </main> 
  ); 
} 

export default MainPage;