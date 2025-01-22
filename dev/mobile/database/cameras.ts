import axios from 'axios';
const API_BASE_URL = 'http://localhost:8000/api/cameras'; // FastAPIのベースURL


export class CamerasFloorCreate {
    camera_id: string = '';
    distance_p1_p2: number = 0;
    distance_p1_p3: number = 0;
    distance_p1_p4: number = 0;
    distance_p2_p3: number = 0;
    distance_p2_p4: number = 0;
    distance_p3_p4: number = 0;

    coordinate_p1: number = 0;
    coordinate_p2: number = 0;
    coordinate_p3: number = 0;
    coordinate_p4: number = 0;
}

export const allcameras = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/all_cameras`,{ params: { nursery_school_id: 'school1'  } });
        return response.data;
    } catch (error) {
        console.error('Error fetching alerts:', error);
        throw error;
    }
};

export const floorsetting = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/floor_setting`,{ params: { camera_id: 'camera1' } });
        return response.data;
    } catch (error) {
        console.error('Error fetching alerts:', error);
        throw error;
    }
};

export const pictures = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/picture`,{ params: { camera_id: 'camera1'} });
        return response.data;
    } catch (error) {
        console.error('Error fetching alerts:', error);
        throw error;
    }
};

export const addfloor = async (data: any) => {
    try {
        const response = await axios.post(
            `${API_BASE_URL}/add_floor`,
            data  // データを直接送信
        );
        return response.data;
    } catch (error) {
        console.error('Error adding floor:', error);
        throw error;
    }
};

export const getfloor = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/get_floor`,{ params: { camera_id: 'camera1'} });
        return response.data;
    } catch (error) {
        console.error('Error fetching alerts:', error);
        throw error;
    }
};