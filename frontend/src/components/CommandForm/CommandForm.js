import React, { useState, useEffect } from 'react';
import axios from 'axios';
import classes from './CommandForm.module.css';

const CommandForm = ({ onCreate, addNotification }) => {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');

  useEffect(() => {
    const getCommand = async () => {
      const apiUrl = process.env.REACT_APP_API_URL;
      const token = localStorage.getItem('token');
      const headers = {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      };
      const commandId = localStorage.getItem('commandId');
      const params = {
        command_id: commandId,
      };
      const response = await axios({
        headers: headers,
        method: 'get',
        url: `${apiUrl}/command`,
        params: params,
      });

      setName(response.data.name);
      setDescription(response.data.description);
    };
    getCommand();
  }, []);

  const createCommand = async () => {
    const apiUrl = process.env.REACT_APP_API_URL;
    const token = localStorage.getItem('token');
    try {
      const headers = {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      };
      const body = {
        name: name,
        description: description,
      };
      const response = await axios({
        headers: headers,
        method: 'post',
        url: `${apiUrl}/command`,
        data: body,
      });
      addNotification(
        'info',
        `Command ${response.data.name} created successfully`,
      );
      onCreate();
    } catch (error) {
      addNotification('error', error.response.data.detail);
      console.error(
        'Create command failed:',
        error.response ? error.response.data : error.message,
      );
    }
  };

  const editCommand = async (commandId) => {
    const apiUrl = process.env.REACT_APP_API_URL;
    const token = localStorage.getItem('token');
    try {
      const headers = {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      };
      const body = {
        name: name,
        description: description,
      };
      const response = await axios({
        headers: headers,
        method: 'put',
        url: `${apiUrl}/command/${commandId}`,
        data: body,
      });
      addNotification(
        'info',
        `Command ${response.data.name} updated successfully`,
      );
      localStorage.removeItem('commandId');
      onCreate();
    } catch (error) {
      addNotification('error', error.response.data.detail);
      console.error(
        'Create command failed:',
        error.response ? error.response.data : error.message,
      );
    }
  };

  const handleCommand = async (e) => {
    e.preventDefault();
    const commandId = localStorage.getItem('commandId');
    if (commandId) {
      editCommand(commandId);
    } else {
      createCommand();
    }
  };

  return (
    <form className={classes.form} onSubmit={handleCommand}>
      <input
        type="text"
        className={classes.name}
        placeholder="name"
        value={name || ''}
        onChange={(e) => setName(e.target.value)}
        required
      />
      <input
        type="text"
        className={classes.description}
        placeholder="command"
        value={description || ''}
        onChange={(e) => setDescription(e.target.value)}
        required
      />
      <button className={classes.create_btn} type="submit">
        done
      </button>
    </form>
  );
};

export default CommandForm;
