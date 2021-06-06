import React from 'react'; 
import car from "../images/car.png";

function DataInputPage({ location, history }) {
  console.log(history); 
  console.log(location); 
  return ( 
    <main className='main'> 
      <span class="inline-block">
        <strong>분석 결과 화면</strong> 
        <img alt='car' className="carphoto" src={car}/>
        <div>입력데이터</div> 
        <div>현재 노면 상태</div> 
        <div>차량제어표시</div> 
        <ul>
          <li2> 
            <button className="btn" onClick={() => history.push('/')}>메인화면</button> 
          </li2> 
        </ul> 
      </span>
    </main> 
  ); 
} 

export default DataInputPage;