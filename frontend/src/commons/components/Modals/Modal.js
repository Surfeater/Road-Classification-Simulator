import React from 'react';
import "../../../assets/css/modal.css";

const Modal = ( props ) => {
    const { open, confirm, cancel, header } = props;

    return (
        <div className={ open ? 'openModal modal' : 'modal' }>
            { open ? (  
                <section>
                    <header>
                        {header}
                    </header>
                    <main>
                        {props.children}
                    </main>
                    <footer>
                        <button className="confirm" onClick={confirm}> 확인 </button>
                        <button className="cancel" onClick={cancel}> 취소 </button>
                    </footer>
                </section>
            ) : null }
        </div>
    )
}

export default Modal