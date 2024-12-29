import { createSlice, PayloadAction } from "@reduxjs/toolkit";

// Stateの型定義
interface CamerasState {
    camera_id: string;
}

// 初期状態
const initialState: CamerasState = {
    camera_id: "",
};

// スライスの作成
const camerasSlice = createSlice({
    name: "cameras",
    initialState,
    reducers: {
        // 任意の値を追加するアクション
        changeCameraId(state, action: PayloadAction<string>) {
            state.camera_id = action.payload;
        },
    },
});

// アクションのエクスポート
export const { changeCameraId } = camerasSlice.actions;

// デフォルトエクスポートとしてリデューサー関数をエクスポート
export default camerasSlice.reducer;