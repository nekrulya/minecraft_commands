import React from 'react';
import classNames from 'classnames';

import classes from './NotificationCenter.module.css';

const NotificationCenter = ({ notifications }) => {
  return (
    <div className={classes.list}>
      {notifications.map((notification) => (
        <p
          key={notification.id}
          className={classNames(
            classes.item,
            notification.type === 'info' && classes.info,
            notification.type === 'error' && classes.error,
          )}
        >
          {notification.message}
        </p>
      ))}
    </div>
  );
};

export default NotificationCenter;
