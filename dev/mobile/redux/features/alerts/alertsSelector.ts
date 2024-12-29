import { RootState } from "../../store";

// alert_idの値を取得するセレクタ
export const selectAlertId = (state: RootState) => state.alerts.alert_id;