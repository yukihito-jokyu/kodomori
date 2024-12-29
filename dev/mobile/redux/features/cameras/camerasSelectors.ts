import { RootState } from "../../store";

// camera_idの値を取得するセレクタ
export const selectCameraId = (state: RootState) => state.cameras.camera_id;