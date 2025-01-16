import { createSlice, PayloadAction } from "@reduxjs/toolkit";

// Stateの型定義
interface UsersState {
    user_id: string;
    is_admin: boolean;
    nursery_school_id: string;
}

// 初期状態
const initialState: UsersState = {
    user_id: "",
    is_admin: false,
    nursery_school_id: "",
};

// スライスの作成
const usersSlice = createSlice({
    name: "users",
    initialState,
    reducers: {
        // user_idの値を変更するアクション
        changeUserId(state: UsersState, action: PayloadAction<string>) {
            state.user_id = action.payload;
        },
        // is_adminの値を変更するアクション
        changeIsAdmin(state: UsersState, action: PayloadAction<boolean>) {
            state.is_admin = action.payload;
        },
        // nursery_school_idの値を変更するアクション
        changeNurserySchoolId(state: UsersState, action: PayloadAction<string>) {
            state.nursery_school_id = action.payload;
        },
    },
});

// アクションのエクスポート
export const {
    changeUserId,
    changeIsAdmin,
    changeNurserySchoolId,
} = usersSlice.actions;

// デフォルトエクスポートとしてリデューサー関数をエクスポート
export default usersSlice.reducer;