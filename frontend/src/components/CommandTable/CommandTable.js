import React from 'react';
import { FaClipboard, FaTrash, FaEdit } from 'react-icons/fa'; // Используем react-icons для иконки копирования
import axios from 'axios';
import classNames from 'classnames';
import classes from './CommandTable.module.css';

const CommandTable = ({
  commands,
  setCommands,
  addNotification,
  openModal,
}) => {
  const apiUrl = process.env.REACT_APP_API_URL;
  const token = localStorage.getItem('token');

  // Функция для копирования текста в буфер обмена
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

  const fetchCommands = async () => {
    await axios
      .get(`${apiUrl}/command`)
      .then((response) => {
        setCommands(response.data);
      })
      .catch((error) => {
        console.error('There was an error fetching the commands!', error);
      });
  };

  const deleteCommand = async (command_id) => {
    try {
      const headers = {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      };
      const response = await axios({
        headers: headers,
        method: 'delete',
        url: `${apiUrl}/command/${command_id}`,
      });
      addNotification(
        'info',
        `Command ${response.data.name} deleted successfully`,
      );
      fetchCommands();
    } catch (error) {
      addNotification('error', error.response.data.detail);
      console.error(
        'Delete command failed:',
        error.response ? error.response.data : error.message,
      );
    }
  };

  const editCommand = async (commandId) => {
    localStorage.setItem('commandId', commandId);
    openModal();
  };

  return (
    <table className={classes.table}>
      <thead>
        <tr className={classes.heading}>
          <th className={classes.heading}>name</th>
          <th className={classes.heading}>command</th>
          <th className={classes.heading}>user</th>
          <th className={classes.heading}>manage</th>
        </tr>
      </thead>
      <tbody>
        {commands.map((command) => (
          <tr className={classes.cells} key={command.id}>
            <td className={classNames(classes.cell, classes.cell_break_word)}>
              {command.name}
            </td>
            <td
              className={classNames(classes.cell, classes.cell_break_word)}
              style={{ paddingRight: '35px' }}
            >
              {command.description}
              <FaClipboard
                className={classes.copy_icon}
                onClick={() => handleCopy(command.description)}
              />
            </td>
            <td className={classes.cell}>{command.created_by}</td>
            <td className={classNames(classes.cell, classes.manage_btns)}>
              <FaEdit
                className={classes.edit_icon}
                onClick={() => {
                  editCommand(command.id);
                }}
              />
              <FaTrash
                className={classes.delete_icon}
                onClick={() => deleteCommand(command.id)}
              />
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default CommandTable;
