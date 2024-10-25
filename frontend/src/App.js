import React, { useState, useEffect, useReducer } from 'react';
import axios from 'axios';
import './App.css';
import NotificationCenter from './components/NotificationCenter/NotificationCenter';
import Header from './components/Header/Header';
import CommandTable from './components/CommandTable/CommandTable';
import Modal from './components/Modal/Modal';
import CommandForm from './components/CommandForm/CommandForm';

function App() {
  const [commands, setCommands] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const openModal = () => {
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  useEffect(() => {
    const apiUrl = process.env.REACT_APP_API_URL;
    // Запрос к FastAPI
    axios
      .get(`${apiUrl}/command`)
      .then((response) => {
        setCommands(response.data);
      })
      .catch((error) => {
        addNotification('error', error.response.data.detail);
        console.error('There was an error fetching the commands!', error);
      });
  }, [isModalOpen]);

  const notificationDuration = 3000;

  const notificationReducer = (state, action) => {
    switch (action.type) {
      case 'ADD_NOTIFICATION':
        return [...state, action.payload];
      case 'REMOVE_OLD_NOTIFICATIONS':
        const currentTime = Date.now();
        return state.filter(
          (notification) =>
            currentTime - notification.created_at < notificationDuration,
        );
      default:
        return state;
    }
  };

  const [notifications, dispatchNotification] = useReducer(
    notificationReducer,
    [],
  );

  // Функция для добавления уведомления
  const addNotification = (type, message) => {
    if (type === 'error' && typeof message !== 'string') {
      message = message[0].msg;
    }
    const newNotification = {
      id: Date.now(),
      type,
      message,
      created_at: Date.now(),
    };
    dispatchNotification({
      type: 'ADD_NOTIFICATION',
      payload: newNotification,
    });
  };

  useEffect(() => {
    // Удаляем устаревшие уведомления каждые 500 мс
    const timer = setInterval(() => {
      dispatchNotification({ type: 'REMOVE_OLD_NOTIFICATIONS' });
    }, 500);

    return () => clearInterval(timer); // Очищаем таймер при размонтировании компонента
  }, []);

  return (
    <div className="App">
      <Header
        addNotification={addNotification}
        openModal={openModal}
        setCommands={setCommands}
      />

      <CommandTable
        commands={commands}
        setCommands={setCommands}
        addNotification={addNotification}
        openModal={openModal}
      />
      <Modal isOpen={isModalOpen} onClose={closeModal}>
        <CommandForm onCreate={closeModal} addNotification={addNotification} />
      </Modal>
      <NotificationCenter notifications={notifications} />
    </div>
  );
}

export default App;
