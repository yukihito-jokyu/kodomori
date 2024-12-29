import { RootState } from "../../store";

// user_idの値を取得するセレクタ
export const selectUserId = (state: RootState) => state.users.user_id;

// is_adminの値を取得するセレクタ
export const selectIsAdmin = (state: RootState) => state.users.is_admin;

// nursery_school_idの値を取得するセレクタ
export const selectNurserySchoolId = (state: RootState) => state.users.nursery_school_id;