import React, { useEffect, useState } from 'react';
import { View, Text ,TouchableOpacity} from 'react-native';

import { getAlerts , getAlertid} from '@/database/alrets';
import { allcameras,floorsetting ,pictures,getfloor,addfloor,CamerasFloorCreate} from '@/database/cameras';
import {getdangerid, getdangerarea,adddanger,DangersCreate}from '@/database/dangers';
import {login}from '@/database/users';

export default function HomeScreen() {
    //get,usestate
    const [alertsid, setAlertsid] = useState([]);
    const [alerts, setAlerts] = useState([]);

    const [cameras, setCameras] = useState([]);
    const [floorset, setFloorset] = useState([]);
    const [picture, setPicture] = useState([]);
    const [floor, setFloor] = useState([]);

    const [dangerid, setDangerid] = useState([]);
    const [dangerarea, setDangerarea] = useState([]);

    //post,usestate
    const [floorData, setFloorData] = useState([]);
    const [dangerResult, setDangerResult] = useState([]);
    const [loginData, setLoginData] = useState([]);

    useEffect(() => {
        //getAPItest
        const fetchAlerts = async () => {
            try {
                const data = await getAlertid();
                setAlertsid(data);
                const data2 = await getAlerts();
                setAlerts(data2);
            } catch (error) {
                console.error('Error fetching alerts:', error);
            }
        };

        const fetchCameras = async () => {
            try {
                const data = await allcameras();
                setCameras(data);
                const data2 = await floorsetting();
                setFloorset(data2);
                const data3 = await pictures();
                setPicture(data3);
                const data4 = await getfloor();
                setFloor(data4);
            } catch (error) {
                console.error('Error fetching alerts:', error);
            }
        };

        const fetchDanger = async () => {
            try {
                const data = await getdangerid();
                setDangerid(data);
                const data2 = await getdangerarea();
                setDangerarea(data2);
            } catch (error) {
                console.error('Error fetching alerts:', error);
            }
        };

        fetchAlerts();
        fetchCameras();
        fetchDanger();

        //postAPItest
        // 床データのテスト
        

    }, []);

    const testFloorApi = async () => {
        try {
            // リクエストデータを直接オブジェクトとして構築
            const floorData = {
                camera_id: `camera_${Date.now()}`,
                distance_p1_p2: 10,
                distance_p1_p3: 15,
                distance_p1_p4: 20,
                distance_p2_p3: 25,
                distance_p2_p4: 30,
                distance_p3_p4: 35,
                coordinate_p1: 1,
                coordinate_p2: 2,
                coordinate_p3: 3,
                coordinate_p4: 4
            };

            const response = await addfloor(floorData);
            setFloorData(prev => ({...prev, floorApi: true}));
            console.log('Floor API test succeeded:', response);
            return true;
        } catch (error) {
            setFloorData(prev => ({...prev, floorApi: false}));
            console.error('Floor API test failed:', error);
            return false;
        }
    };

    // 危険エリアのテスト
    const testDangerApi = async () => {
        try {
        const dangerData = {
        danger_id : `danger_${Date.now()}`,
        coordinate_p1 : 10,
        coordinate_p2 : 20,
        coordinate_p3 : 30,
        coordinate_p4 : 40,
    }

        const response = await adddanger(dangerData);
        setDangerResult(prev => ({...prev, dangerApi: true}));
        console.log('Danger API test succeeded:', response);
        return true;
        } catch (error) {
        setDangerResult(prev => ({...prev, dangerApi: false}));
        console.error('Danger API test failed:', error);
        return false;
        }
    };

    const fetchLogin = async () => {
        try {
            const loginData = {
                user_id: 'school1'
            };
            const data = await login(loginData);
            setLoginData(data);
            console.log('Login response:', data);
            return true;
        } catch (error) {
            console.error('Error fetching alerts:', error);
        }
    };

    return (
        <View>
            <Text>GETTest</Text>
            {/* <Text>userId: {userId}</Text> */}
            <Text>Alertsid: {JSON.stringify(alertsid)}</Text>
            <Text>Alerts: {JSON.stringify(alerts)}</Text>
            <Text>Cameras: {JSON.stringify(cameras)}</Text>
            <Text>Floorset: {JSON.stringify(floorset)}</Text>
            <Text>Picture: {JSON.stringify(picture)}</Text>
            <Text>Floor: {JSON.stringify(floor)}</Text>
            <Text>Dangerid: {JSON.stringify(dangerid)}</Text>
            <Text>Dangerarea: {JSON.stringify(dangerarea)}</Text>

            <Text>POSTTest</Text>
            <TouchableOpacity  onPress={testFloorApi} >
                <Text>FloorDataBotton: {JSON.stringify(floorData)}</Text>
            </TouchableOpacity>
            <TouchableOpacity  onPress={testDangerApi} >
                <Text>DangerResultBotton: {JSON.stringify(dangerResult)}</Text>
            </TouchableOpacity>
            <TouchableOpacity onPress={fetchLogin} >
                <Text>LoginBotton: {JSON.stringify(loginData)}</Text>
            </TouchableOpacity>
            <Text>FloorData: {JSON.stringify(floorData)}</Text>
            <Text>DangerResult: {JSON.stringify(dangerResult)}</Text>
            <Text>Login: {JSON.stringify(loginData)}</Text>
        </View>
    );
}