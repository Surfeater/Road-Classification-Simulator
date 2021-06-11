import React, { useState } from 'react';
import '../App.css';
import { Timeline } from "react-beautiful-horizontal-timeline";

function DataInputPage({ location, history }) {
  console.log(history); 
  console.log(location); 
  return ( 
    <main className='main'> 
      <span class="inline-block">
        <strong>분석 결과 화면</strong> 
        <MyTimeline />
        <ul>
          <li2> 
            <button className="btn" onClick={() => history.push('/')}>메인화면</button> 
          </li2> 
        </ul> 
      </span>
    </main> 
  ); 
} 

function MyTimeline() {

  const myList = [
    {
      date: "00:00",
      name: "아스팔트길"
    },
    {
      date: "00:01",
      name: "흙길"
    },
    {
      date: "00:02",
      name: "자갈길"
    }
  ];

  const [labelWidth, setlabelWidth] = useState(300);
  const [amountMove, setamountMove] = useState(800);
  const [lineColor, setlineColor] = useState("#61dafb");
  const [darkMode, setdarkMode] = useState(false);
  const [eventTextAlignCenter, seteventTextAlignCenter] = useState(true);
  const [showSlider, setshowSlider] = useState(true);
  const [arrowsSize, setarrowsSize] = useState(false);

  return (
    <div className="App">
      <Timeline
        myList={myList}
        labelWidth={labelWidth}
        amountMove={amountMove}
        lineColor={lineColor}
        darkMode={darkMode}
        eventTextAlignCenter={eventTextAlignCenter}
        showSlider={showSlider}
        arrowsSize={arrowsSize}
      />
    </div>
  );
}

export default DataInputPage;