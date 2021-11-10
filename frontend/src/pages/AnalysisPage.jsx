import React, { useState } from 'react';
import '../App.css';

function DataInputPage({ location, history }) {
  console.log(history); 
  console.log(location); 
  return ( 
    <main className='main'> 
      <span class="inline-block">
        <strong>분석 결과 화면</strong>
        <ul>
          <br/>
          <VideoDetail />
          <li6>
          <AnalysisMessage />
          </li6>
          <li2> 
            <button className="btn" onClick={() => history.push('/')}>메인화면</button> 
          </li2> 
        </ul> 
      </span>
    </main> 
  ); 
}

function VideoDetail() {
  return (
    <video width="60%" controls autoplay muted>
      <source src="" type="video/mp4" />
    </video>
  )
}

function AnalysisMessage() {
  let randNum1 = Math.floor(Math.random() * 4)
  let randNum2 = Math.floor(Math.random() * 4)
  let roadType = {0:"아스팔트", 1:"시멘트", 2:"자갈", 3:"흙"}
  let text_color = ""
  if (randNum1 == randNum2){
    text_color = "#90EE90"
  }else{
    text_color = "#CD001A"
  }

  return (
    <div>
      <b>
      실제 도로 유형: <span style={{ color: "#90EE90" }}>{roadType[randNum1]}</span>
      <br/>
      <br/>
      예측 도로 유형: <span style={{ color: text_color}}>{roadType[randNum2]}</span>
      <br/>
      </b>
    </div>
  )
}

export default DataInputPage;