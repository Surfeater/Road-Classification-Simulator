import React from 'react';
import { useMemo } from "react";
import faker from "faker";
import Table from "./Table";

faker.seed(100);

function LogPage({ location, history }) {
  console.log(history); 
  console.log(location); 

  const columns = useMemo(
    () => [
      {
        accessor: "index",
        Header: "Index",
      },
      {
        accessor: "ip",
        Header: "IP",
      },
      {
        accessor: "time",
        Header: "Time",
      },
    ],
    []
  );

  let no = 0;
  const aab = useMemo(
    () =>
      Array(20)
        .fill()
        .map(() => ({
          ip: faker.internet.ip(),
          time: Date(),
          index: <button calssName ="btn" onClick={() => history.push('/analysis/')} >{no++}</button>,
        })),
    []
  );
  return ( 
    <main className='main'>
      <span class="inline-block">
        <strong>로그 페이지</strong> 
        <Table columns={columns} data={aab} />
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