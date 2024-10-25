import React from 'react';
import classes from './Modal.module.css';

const Modal = ({ isOpen, onClose, children }) => {
  if (!isOpen) return null; // Не отображаем модал, если он закрыт

  const handleOutsideClick = (event) => {
    // Проверяем, если кликнули вне модального окна
    if (event.target.className === classes.overlay) {
      onClose();
    }
  };

  return (
    <div className={classes.overlay} onClick={handleOutsideClick}>
      <div className={classes.content}>
        {children} {/* Контент модального окна */}
      </div>
    </div>
  );
};

export default Modal;
