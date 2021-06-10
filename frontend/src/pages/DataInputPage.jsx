import React, { useMemo, useState } from 'react';
import Modal from '../commons/components/Modals/Modal';
import {useDropzone} from 'react-dropzone';

function DataInputPage({ location, history }) {
  console.log(history); 
  console.log(location);

  const [ modalOpen, setModalOpen ] = useState(false);

  const openModal = () => {
    setModalOpen(true);
  }

  const confirmModal = () => {
    setModalOpen(false);
    history.push('/analysis');
  }

  const cancelModal = () => {
    setModalOpen(false);
  }

  return ( 
    <main className='main'> 
      <span class="inline-block">
        <strong>데이터 입력 페이지</strong> 
        <ul>
          <li5> 
            <button className="btn2" onClick={() => alert("미구현")}>실시간분석</button> 
          </li5> 
          <li2> 
            <button className="btn" onClick={() => history.push('/')}>메인화면</button> 
          </li2> 
          <li4> 
            <button className="btn2" onClick={ openModal }>파일분석</button>
            <Modal open={ modalOpen } confirm = { confirmModal } cancel={ cancelModal } header="파일분석">
              <Dropzone />
            </Modal>  
          </li4> 
        </ul> 
      </span>
    </main> 
  ); 
}

const baseStyle = {
  flex: 1,
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  padding: '20px',
  borderWidth: 4,
  borderRadius: 10,
  borderColor: '#eeeeee',
  borderStyle: 'dashed',
  backgroundColor: '#fafafa',
  color: '#bdbdbd',
  outline: 'none',
  transition: 'border .24s ease-in-out'
};

const activeStyle = {
  borderColor: '#2196f3'
};

const acceptStyle = {
  borderColor: '#00e676'
};

const rejectStyle = {
  borderColor: '#00e676'
};

function Dropzone(props) {
  const {
    getRootProps,
    getInputProps,
    isDragActive,
    isDragAccept,
    isDragReject,
    acceptedFiles
  } = useDropzone({accept: '.csv', maxFiles:1});

  const style = useMemo(() => ({
    ...baseStyle,
    ...(isDragActive ? activeStyle : {}),
    ...(isDragAccept ? acceptStyle : {}),
    ...(isDragReject ? rejectStyle : {})
  }), [
    isDragActive,
    isDragReject,
    isDragAccept
  ]);

  const files = acceptedFiles.map(file => (
    <li key={file.path}>
      {file.path} - {file.size} bytes
    </li>
  ));

  return (
    <div className="container">
      <div {...getRootProps({style})}>
        <input {...getInputProps()} />
        <p>이곳에 파일을 끌어놓거나 클릭해서 파일을 선택하세요.</p>
      </div>
      <aside>
        <h4>선택된 파일</h4>
        <ul>{files}</ul>
      </aside>
    </div>
  );
}

export default DataInputPage;