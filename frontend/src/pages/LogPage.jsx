import React from 'react';
import { useMemo } from "react";
import faker from "faker/locale/ko";
import Table from "./Table";

faker.seed(100);

function LogPage({ location, history }) {
  console.log(history); 
  console.log(location); 
  const columns = useMemo(
    () => [
      {
        accessor: "name",
        Header: "Name",
      },
      {
        accessor: "email",
        Header: "Email",
      },
      {
        accessor: "phone",
        Header: "Phone",
      },
    ],
    []
  );

  const data = useMemo(
    () =>
      Array(530)
        .fill()
        .map(() => ({
          name: faker.name.lastName() + faker.name.firstName(),
          email: faker.internet.email(),
          phone: faker.phone.phoneNumber(),
        })),
    []
  );
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