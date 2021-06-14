import React from 'react';
import { useMemo, useEffect, useState, useRef } from "react";
import Table from "./Table";
import axios from "axios";

function LogPage({ location, history }) {
  console.log(history); 
  console.log(location); 

  /*let indexNum = useRef(-1);*/
  const [data, setData] = useState([]);
  
  useEffect(() =>{
		async function fetchData(){
		const result = await axios.get('http://localhost:5000/requests/');
    const newResult = result.data.map((item) => {
      /*const index = <button calssName ="btn" onClick={() => history.push('/analysis/')} >{indexNum.current += 1}</button>;*/
      item.request_number = <button calssName ="btn" onClick={() => history.push('/analysis/')} >{item.request_number}</button>;
      /*const updateItem = {...item, index};*/
      const updateItem = item;
      return updateItem;
    });
    setData(newResult);
		}
		fetchData();
	},[]);

  const columns = useMemo(
    () => [
      {
        accessor: "request_number",
        Header: "Request_Number",
      },
      {
        accessor: "ip",
        Header: "IP",
      },
      {
        accessor: "time",
        Header: "Time",
      },
      {
        accessor: "filepath",
        Header: "Filepath",
      },
    ],
    []
  );
  console.log(data);
  return ( 
    <main className='main'>
      <span class="inline-block">
        <strong>로그 페이지</strong> 
        <Table columns={columns} data={data} />
        <ul>
          <li2> 
            <button className="btn" onClick={() => history.push('/')}>메인화면</button> 
          </li2> 
        </ul> 
      </span>
    </main> 
  ); 
} 

export default LogPage;