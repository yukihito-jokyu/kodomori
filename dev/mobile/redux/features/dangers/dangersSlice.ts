import { createSlice, PayloadAction } from "@reduxjs/toolkit";

// Stateの型定義
interface DangersState {
    danger_id: string;
}

// 初期状態
const initialState: DangersState = {
    danger_id: "",
};

// スライスの作成
const dangersSlice = createSlice({
    name: "cameras",
    initialState,
    reducers: {
        // 任意の値を追加するアクション
        changeDangerId(state, action: PayloadAction<string>) {
            state.danger_id = action.payload;
        },
    },
});

// アクションのエクスポート
export const { changeDangerId } = dangersSlice.actions;

// デフォルトエクスポートとしてリデューサー関数をエクスポート
export default dangersSlice.reducer;