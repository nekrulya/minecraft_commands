import React, { useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import classes from './Header.module.css';
import AuthForm from '../AuthForm/AuthForm';
import CommandsSelect from '../CommandsSelect/CommandsSelect';
import axios from 'axios';

const Header = ({ addNotification, openModal, setCommands }) => {
  const apiUrl = process.env.REACT_APP_API_URL;

  const [username, setUsername] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogOut = async () => {
    localStorage.removeItem('token');
    setIsLoggedIn(false);
  };

  const isTokenExpired = (token) => {
    if (!token) return true;
    const decoded = jwtDecode(token);
    const currentTime = Date.now() / 1000;
    setUsername(decoded.username);
    return decoded.exp < currentTime;
  };

  useEffect(() => {
    const token = localStorage.getItem('token'); // Получите токен из локального хранилища или где он хранится
    if (!isTokenExpired(token)) {
      setIsLoggedIn(true);
    }
  }, [apiUrl]);

  const addCommand = () => {
    localStorage.removeItem('commandId');
    openModal();
  };

  const handleCopy = (text) => {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard
        .writeText(text)
        .then(() => {})
        .catch((err) => {
          console.error('Failed to copy text: ', err);
        });
    } else {
      // Фолбэк для старых браузеров
      const textArea = document.createElement('textarea');
      textArea.value = text;
      document.body.appendChild(textArea);
      textArea.select();
      try {
        document.execCommand('copy');
      } catch (err) {
        console.error('Fallback: Oops, unable to copy', err);
      }
      document.body.removeChild(textArea);
    }
  };

  const handleDownload = async () => {
    const apiUrl = process.env.REACT_APP_API_URL;
    const token = localStorage.getItem('token');
    const headers = {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    };

    const response = await axios({
      headers: headers,
      method: 'get',
      url: `${apiUrl}/command/file`,
    });
    handleCopy(response.data);
    addNotification('info', 'Commands copied to clipboard');
  };

  const handleSendingCommands = async () => {
    const apiUrl = process.env.REACT_APP_API_URL;
    const token = localStorage.getItem('token');
    const headers = {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    };

    const response = await axios({
      headers: headers,
      method: 'get',
      url: `${apiUrl}/command/send`,
    });
    addNotification('info', 'Commands were sent to the server');
    console.log(response.data);
  };

  return (
    <header className={classes.header}>
      <h1 className={classes.title}>List of Commands</h1>
      {isLoggedIn ? (
        <div className={classes.username}>
          <span>{username}</span>
          <button className={classes.btn} onClick={addCommand}>
            Add command
          </button>
          <button className={classes.btn} onClick={handleLogOut}>
            Log Out
          </button>
          <button className={classes.btn} onClick={handleDownload}>
            copy commands
          </button>
          <button className={classes.btn} onClick={handleSendingCommands}>
            send commands
          </button>
        </div>
      ) : (
        <AuthForm
          username={username}
          setUsername={setUsername}
          setIsLoggedIn={setIsLoggedIn}
          addNotification={addNotification}
        />
      )}
      <CommandsSelect
        username={username}
        setCommands={setCommands}
        addNotification={addNotification}
      ></CommandsSelect>
    </header>
  );
};

export default Header;
