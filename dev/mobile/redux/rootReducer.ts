import { combineReducers } from "@reduxjs/toolkit";
import usersReducer from "./features/users/usersSlice";
import camerasReducer from "./features/cameras/camerasSlice"
import dangersReducer from "./features/dangers/dangersSlice"
import alertReducer from "./features/alerts/alertsSlice"

const rootReducer = combineReducers({
    users: usersReducer,
    cameras: camerasReducer,
    dangers: dangersReducer,
    alerts: alertReducer,
});

export default rootReducer;