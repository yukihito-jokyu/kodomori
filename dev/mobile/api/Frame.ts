import axios from "axios";

interface pinAndDistance {
    p1_p2: number;
    p1_p3: number;
    p1_p4: number;
    p2_p3: number;
    p2_p4: number;
    p3_p4: number;
    pin_1_x: number;
    pin_1_y: number;
    pin_2_x: number;
    pin_2_y: number;
    pin_3_x: number;
    pin_3_y: number;
    pin_4_x: number;
    pin_4_y: number;
}

interface pin {
    pin_1_x: number;
    pin_1_y: number;
    pin_2_x: number;
    pin_2_y: number;
    pin_3_x: number;
    pin_3_y: number;
    pin_4_x: number;
    pin_4_y: number;
}

export const fetchFrame = async (): Promise<{ frame_base64: string }> => {
    // カメラ映像を取得する
    try {
        const response = await axios.post("http://localhost:8000/frame/get_frame");
        return response.data;
    } catch (error) {
        console.error("Error:", error);
        throw new Error("データ取得に失敗しました");
    }
}

export const fetchWrap = async (): Promise<{ wrap_base64: string, height: number, width: number }> => {
    // 床エリアの映像を取得する
    try {
        const response = await axios.get("http://localhost:8000/frame/get_wrap");
        return response.data;
    } catch (error) {
        console.error("Error:", error);
        throw new Error("データ取得に失敗しました");
    }
}

export const postPinAndDistance = async (pinAndDistance: pinAndDistance): Promise<{ warped_base64: string }> => {
    try {
        const response = await axios.post(
            "http://localhost:8000/frame/floor_setting",
            pinAndDistance
        );
        return response.data;
    } catch (error) {
        console.error("Error:", error);
        throw new Error("データ取得に失敗しました");
    }
}

export const postPin = async (pin: pin): Promise<{ warped_with_zone: string }> => {
    try {
        const response = await axios.post(
            "http://localhost:8000/frame/zone_setting",
            pin
        );
        return response.data;
    } catch (error) {
        console.error("Error:", error);
        throw new Error("データ取得に失敗しました");
    }
}