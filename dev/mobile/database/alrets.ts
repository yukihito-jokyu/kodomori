import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/alerts'; // FastAPIのベースURL

export const getAlertid = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/get_alert_id`,{ params: { nursery_school_id: 'school1'} });
        return response.data;
    } catch (error) {
        console.error('Full Error:', error);
        throw error;
    }
};

export const getAlerts = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/get_alert`,{ params: { alert_id: 'alert1' } });
        return response.data;
    } catch (error) {
        console.error('Error fetching alerts:', error);
        throw error;
    }
}