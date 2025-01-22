 import axios from 'axios';
 const API_BASE_URL = 'http://localhost:8000/api/dangers'; // FastAPIのベースURL

// APIのレスポンスの型定義
export class DangersCreate {
    danger_id: number=0;
    coordinate_p1: number=0;
    coordinate_p2: number=0;
    coordinate_p3: number=0;
    coordinate_p4: number=0;
    }

export const getdangerid = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/get_danger_id`, { params: { camera_id: 'camera1' } });
        return response.data;
    } catch (error) {
        console.error('Error fetching alerts:', error);
        throw error;
    }
};

export const adddanger = async (data:any) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/add_danger`, data);
        return response.data;
    } catch (error) {
        console.error('Error fetching alerts:', error);
        throw error;
    }
};

export const getdangerarea = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/get_danger_area`,{ params: { danger_id: 'danger1' } });
        return response.data;
    } catch (error) {
        console.error('Error fetching alerts:', error);
        throw error;
    }
};

