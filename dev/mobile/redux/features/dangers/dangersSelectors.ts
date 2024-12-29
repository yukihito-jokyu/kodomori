import { RootState } from "../../store";

// danger_idの値を取得するセレクタ
export const selectDangerId = (state: RootState) => state.dangers.danger_id;