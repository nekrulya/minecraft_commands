import React from 'react';
import axios from 'axios';
import classes from './CommandsSelect.module.css';

const CommandsSelect = ({ setCommands, username, addNotification }) => {
  const fetchCommands = async () => {
    const apiUrl = process.env.REACT_APP_API_URL;
    await axios
      .get(`${apiUrl}/command`)
      .then((response) => {
        setCommands(response.data);
      })
      .catch((error) => {
        addNotification('error', error.response.data.detail);
        console.error('There was an error fetching the commands!', error);
      });
  };

  const fetchMyCommands = async () => {
    const apiUrl = process.env.REACT_APP_API_URL;
    await axios
      .get(`${apiUrl}/user/commands`, {
        params: {
          username: username,
        },
      })
      .then((response) => {
        setCommands(response.data);
      })
      .catch((error) => {
        addNotification('error', error.response.data.detail);
        console.error('There was an error fetching the commands!', error);
      });
  };

  return (
    <div className={classes.btns}>
      <button className={classes.btn} onClick={fetchCommands}>
        ALL
      </button>
      <button className={classes.btn} onClick={fetchMyCommands}>
        MY
      </button>
    </div>
  );
};

export default CommandsSelect;
