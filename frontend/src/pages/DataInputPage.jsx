import React from 'react'; 

function DataInputPage({ location, history }) {
  console.log(history); 
  console.log(location); 
  return ( 
    <main className='main'> 
      <span class="inline-block">
        <strong>데이터 입력 페이지</strong> 
        <strong><br/><input type="file" /></strong>
        <ul>
          <li1> 
            <button className="btn" onClick={() => history.push('/analysis')}>분석실행</button>
          </li1> 
          <li3> 
            <button className="btn" onClick={() => alert("미구현")}>실시간분석</button> 
          </li3> 
          <li2> 
            <button className="btn" onClick={() => history.push('/')}>메인화면</button> 
          </li2> 
        </ul> 
      </span>
    </main> 
  ); 
} 

export default DataInputPage;