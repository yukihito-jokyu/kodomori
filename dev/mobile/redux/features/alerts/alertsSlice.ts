import { createSlice, PayloadAction } from "@reduxjs/toolkit";

// Stateの型定義
interface AlertsState {
    alert_id: string;
}

// 初期状態
const initialState: AlertsState = {
    alert_id: "",
};

// スライスの作成
const alertsSlice = createSlice({
    name: "cameras",
    initialState,
    reducers: {
        // 任意の値を追加するアクション
        changeAlertId(state, action: PayloadAction<string>) {
            state.alert_id = action.payload;
        },
    },
});

// アクションのエクスポート
export const { changeAlertId } = alertsSlice.actions;

// デフォルトエクスポートとしてリデューサー関数をエクスポート
export default alertsSlice.reducer;