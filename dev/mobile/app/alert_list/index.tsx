import AlertTile from '@/components/AlertList/AlertTile'
import AlertTileEnd from '@/components/AlertList/AlertTileEnd'
import React, { useState } from 'react'
import { SafeAreaView } from 'react-native'

export default function AlertListScreen() {
    const [alerts, setAlerts] = useState([
        {
            checked: false,
            name: "name_1",
            time: "2024/12/17 12:30",
        },
        {
            checked: true,
            name: "name_2",
            time: "2024/12/18 12:30",
        }
    ])
    return (
        <SafeAreaView>
            {alerts.map((alert, index) => {
                if (index+1 == alerts.length) {
                    return <AlertTileEnd 
                        key={index}
                        checked={alert.checked}
                        name={alert.name}
                        time={alert.time}
                    />
                } else {
                    return <AlertTile 
                        key={index}
                        checked={alert.checked}
                        name={alert.name}
                        time={alert.time}
                    />
                }
            })}
        </SafeAreaView>
    )
}

